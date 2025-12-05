from fastapi import FastAPI, Response, Request, UploadFile, File, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn
from fastapi.responses import JSONResponse, PlainTextResponse
import asyncio
from functools import partial
from concurrent.futures import ThreadPoolExecutor
import requests
import re
from datalearning import DataLearning
from config import datadir, datafile
from datapoints import CDI_DDI
from cdi import CDI_DDI
import sys
import os
import os
import json
import pandas as pd
app = FastAPI()

# Ensure repo root is importable to access top-level modules
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
from cdi_generator import generate_cdi
from utils import (
    load_xdi_cdif_mapping,
    xdi_cdif_mapping_to_jsonld,
    load_xdi_cdif_mapping_jsonld,
    xdi_cdif_mapping_to_rml,
)

# Helper: blocking fetch to be executed in thread pool
def fetch_wikilink(term: str, context: str):
    base_url = os.environ.get("SPARQLMUSE", "https://sparqlmuse.now.museum") + "/wikilink/"
    headers = {"accept": "application/json"}
    params = {
        "term": term,
        "context": context,
        "language": "en",
        "format": "json",
    }
    try:
        resp = requests.get(base_url, params=params, headers=headers, timeout=15)
        try:
            wikilink = resp.json()
        except ValueError:
            wikilink = resp.text
    except requests.RequestException as e:
        wikilink = {"error": str(e)}
    return {"name": term, "wikilink": wikilink}

def fetch_skosmos(term: str, context: str):
    base_url = os.environ.get("CESSDAURL", "https://thesauri.cessda.eu")
    context = "elsst-6"
    url = base_url + f"/rest/v1/search?query={term}&vocab={context}"
    headers = {"accept": "application/json"}
    params = {
        "query": term,
        "vocab": context,
    }
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        try:
            skosmos = resp.json()
        except ValueError:
            skosmos = resp.text
    except requests.RequestException as e:
        skosmos = {"error": str(e)}
    result = []
    if 'results' in skosmos:
        result = skosmos['results']
    return {"name": term, "skosmos": result}

def fetch_remote_ollama(term: str):
    base_url = os.environ.get("CDIFSERVICE", "https://cdif-4-xas.dev.codata.org/ollama")
    headers = {"accept": "application/json"}
    params = {"term": term}
    try:
        resp = requests.get(base_url, params=params, headers=headers, timeout=int(os.environ.get("TIMEOUT", 20)))
        try:
            data = resp.json()
        except ValueError:
            data = resp.text
    except requests.RequestException as e:
        data = {"error": str(e)}
    return {"name": term, "ollama_remote": data}

def run_ollama(term: str, model):
    base_url = os.environ.get("OLLAMASERVICE", "http://10.147.18.82:8093")
    if not 'http' in base_url:
        base_url = "http://172.27.39.69:11434"
    url = base_url + f"/api/generate"
    headers = {"accept": "application/json", "content-type": "application/json"}
    prompt = f"create description of variable (definition, units of measurements, properties, attributes) and provide result in json: {term}"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        try:
            data = resp.json()
            raw = data.get("response", data)
        except ValueError:
            raw = resp.text
    except requests.RequestException as e:
        return {"name": term, "ollama": {"error": str(e)}}
    # Parse fenced JSON from response if present
    if isinstance(raw, str):
        text = raw.strip()
        match = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text, re.IGNORECASE)
        parsed = None
        if match:
            candidate = match.group(1)
            try:
                parsed = json.loads(candidate)
            except Exception:
                parsed = None
        if parsed is None:
            try:
                parsed = json.loads(text)
            except Exception:
                parsed = None
        if parsed is None:
            # Fallback: try to find a JSON object anywhere in the text
            m2 = re.search(r"(\{[\s\S]*\})", text)
            if m2:
                candidate2 = m2.group(1)
                try:
                    parsed = json.loads(candidate2)
                except Exception:
                    parsed = None
        ollama = parsed if parsed is not None else raw
    else:
        ollama = raw
    return {"name": term, "ollama": ollama}

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

data = DataLearning(datadir, datafile, format="json-ld")
data.load_data()
data.get_data()

@app.get("/")
def read_root():
    return {"message": "DDI-CDI Service v.0.1"}

@app.get("/cdi-intermidiate")
def read_cdi(url: str, format: str = "turtle"):
    cdi = CDI_DDI(url, "cdi.jsonld", format, type='xas')
    if format == "turtle":
        return Response(content=cdi.parse_cdi().serialize(format=format), media_type="text/turtle")
    else:
        return Response(content=cdi.parse_cdi().serialize(format=format), media_type="application/json")


@app.get("/mapping/xdi-cdif")
def xdi_cdif_mapping_from_url(
    spreadsheet_url: Optional[str] = Query(
        None,
        description="Optional URL or path to the XDI–CDIF mapping spreadsheet (Excel).",
    ),
    export: Optional[str] = Query(
        None,
        description="Export format: 'json-ld' or 'rml' (RML Turtle). "
        "If omitted and fileid is provided, defaults to 'rml', otherwise 'json-ld'.",
    ),
    fileid: Optional[str] = Query(None),
    siteUrl: Optional[str] = Query(None),
    datasetid: Optional[str] = Query(None),
    datasetversion: Optional[str] = Query(None),
    locale: Optional[str] = Query(None),
):
    """
    Load an XDI–CDIF mapping spreadsheet from a given URL or local path
    and return either a JSON-LD or RML (Turtle) representation of the
    mappings.

    If ``spreadsheet_url`` is not provided but other parameters such as
    ``fileid`` / ``siteUrl`` / ``datasetid`` / ``datasetversion`` are
    present (for example when mirroring the `/cdi` API signature), the
    endpoint falls back to the default mapping spreadsheet configured
    in the backend (local `resources` / GitHub URL).
    """
    # Determine export type: if not provided but fileid is set, default to RML,
    # otherwise default to JSON-LD.
    if not export:
        export = "rml" if fileid else "json-ld"
    export = export.lower()

    # Derive spreadsheet URL if not explicitly provided, mirroring the /cdi logic:
    #   <siteUrl>/api/access/datafile/<fileid>
    effective_url = spreadsheet_url
    if not effective_url and fileid and siteUrl:
        base = siteUrl.rstrip("/")
        effective_url = base + "/api/access/datafile/" + str(fileid)

    # Case 1: we have an explicit or derived spreadsheet URL/path
    if effective_url:
        try:
            df = pd.read_excel(effective_url)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to load spreadsheet from '{effective_url}': {e}",
            )
        if export == "rml":
            rml_mapping = xdi_cdif_mapping_to_rml(df)
            return Response(content=rml_mapping, media_type="text/turtle")
        jsonld = xdi_cdif_mapping_to_jsonld(df)
        return JSONResponse(content=jsonld)

    # Case 2: no URL at all – use default mapping from utils
    if export == "rml":
        df = load_xdi_cdif_mapping()
        rml_mapping = xdi_cdif_mapping_to_rml(df)
        return Response(content=rml_mapping, media_type="text/turtle")

    jsonld = load_xdi_cdif_mapping_jsonld()
    return JSONResponse(content=jsonld)

@app.get("/data")
def read_data():
    return data.get_data_as_pandas()

@app.get("/data/example")
def read_data_example(configurationfile: Optional[str] = None):
    if configurationfile is None:
        configurationfile = datafile
    else:
        if not '/' in configurationfile:
            configurationfile = datadir + "/" + configurationfile
        else:
            configurationfile = configurationfile
    data = DataLearning(datadir, configurationfile, format="json-ld")
    data.load_data()
    data.get_data()
    data.add_permanent_schema('dataset')
    #return Response(content=data.serialize_data(format="json-ld"), media_type="application/json")
    datajson = data.export(format="json-ld")
    dataexport = json.dumps({
        "@context": [
            "https://docs.ddialliance.org/DDI-CDI/1.0/model/encoding/json-ld/ddi-cdi.jsonld",
            {"skos": "http://www.w3.org/2004/02/skos/core#", "xdi": "http://www.w3.org/2004/02/skos/core#",
             "cdi": "https://docs.ddialliance.org/DDI-CDI/1.0/model/encoding/json-ld/ddi-cdi.jsonld"}
        ],      
        "DDICDIModels": json.loads(datajson)
    })
    return Response(content=dataexport, media_type="application/json")

@app.get("/data/dataset")
def read_data_dataset(url: str):
    data = DataLearning(datadir, url, format="json-ld")
    data.load_data()
    data.get_data()
    data.add_permanent_schema('dataset')
    #return Response(content=data.serialize_data(format="json-ld"), media_type="application/json")
    datajson = data.export(format="json-ld")
    # Generate CDI graph using shared generator
    cdi_graph = generate_cdi(url, None, "json-ld", None, 'xas')
    cdi_jsonld = cdi_graph.serialize(format="json-ld")
    dataexport = json.dumps({
        "@context": [
            "https://docs.ddialliance.org/DDI-CDI/1.0/model/encoding/json-ld/ddi-cdi.jsonld",
            {"skos": "http://www.w3.org/2004/02/skos/core#"}
        ],      
        "DDICDIModels": [json.loads(datajson)],
        "CDIGenerated": json.loads(cdi_jsonld)
    })
    return Response(content=dataexport, media_type="application/json")

@app.get("/datapoints")
def read_datapoints(url: str, format: str = "turtle"):
    cdi = CDI_DDI(url, "cdi.jsonld", format, type='xas')
    if format == "turtle":
        return Response(content=cdi.parse_cdi().serialize(format=format), media_type="text/turtle")
    else:
        return Response(content=cdi.parse_cdi().serialize(format=format), media_type="application/json")

@app.get("/cdi")
def cdi_generate(
    url: Optional[str] = Query(None),
    format: str = "json-ld",
    resources: Optional[str] = None,
    type: str = "xas",
    fileid: Optional[str] = Query(None),
    siteUrl: Optional[str] = Query(None),
    datasetid: Optional[str] = Query(None),
    datasetversion: Optional[str] = Query(None),
    locale: Optional[str] = Query(None),
):
    # If fileid and siteUrl are provided, construct Dataverse access URL:
    #   <siteUrl>/api/access/datafile/<fileid>
    if fileid and siteUrl:
        base = siteUrl.rstrip("/")
        source_url = base + "/api/access/datafile/" + str(fileid)
    else:
        source_url = url
    if not source_url:
        raise HTTPException(status_code=400, detail="Provide either 'url' or both 'fileid' and 'siteUrl'.")
    graph = generate_cdi(source_url, None, format, resources, type, datasetid, datasetversion)
    cdi_jsonld = graph.serialize(format="json-ld")
    datajson = cdi_jsonld
    # Try to embed distribution nodes instead of blank-node references using JSON-LD framing
    #print("DEBUG: " + str(datajson))
    try:
        from pyld import jsonld as jsonldlib
        doc = json.loads(datajson)
        # Use a rich context so keys compact to prefixes like schema:, spdx:, dcterms:, etc.
        frame_context = {
            "@vocab": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "schema": "https://schema.org/",
            "dcterms": "http://purl.org/dc/terms/",
            "geosparql": "http://www.opengis.net/ont/geosparql#",
            "spdx": "http://spdx.org/rdf/terms#",
            "cdi": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "time": "http://www.w3.org/2006/time#",
            "skos": "http://www.w3.org/2004/02/skos/core#",
            "nx": "https://xas.org/dictionary/",
            "cdifq": "https://cdif.codata.org/concept/",
            "prov": "http://www.w3.org/ns/prov#"
        }
        frame = {
            "@context": frame_context,
            "@type": "schema:Dataset",
            "@embed": "@always",
            "@explicit": False
        }
        framed = jsonldlib.frame(doc, frame)
        compacted = jsonldlib.compact(framed, frame_context)
        # Post-process: inline blank-node references {"@id": "_:b..."} with their full node objects
        def collect_nodes(obj, store):
            if isinstance(obj, dict):
                node_id = obj.get("@id")
                if node_id and node_id.startswith("_:"):
                    store[node_id] = obj
                for v in obj.values():
                    collect_nodes(v, store)
            elif isinstance(obj, list):
                for v in obj:
                    collect_nodes(v, store)
        def deep_clone(o):
            try:
                return json.loads(json.dumps(o))
            except Exception:
                return o
        def inline_refs(obj, node_map, seen_ids):
            if isinstance(obj, dict):
                # If this is a bare reference to a blank node, inline it
                if set(obj.keys()) == {"@id"} and isinstance(obj.get("@id"), str) and obj["@id"].startswith("_:"):
                    ref_id = obj["@id"]
                    target = node_map.get(ref_id)
                    if target and ref_id not in seen_ids:
                        seen_ids.add(ref_id)
                        inlined = inline_refs(deep_clone(target), node_map, seen_ids)
                        seen_ids.discard(ref_id)
                        return inlined
                    return obj
                # Otherwise recursively inline children
                return {k: inline_refs(v, node_map, seen_ids) for k, v in obj.items()}
            if isinstance(obj, list):
                return [inline_refs(v, node_map, seen_ids) for v in obj]
            return obj
        node_map = {}
        collect_nodes(compacted, node_map)
        ddicdi_models = inline_refs(compacted, node_map, set())
    except Exception:
        ddicdi_models = json.loads(datajson)
    # Wrap output with requested top-level @context and @graph
    if isinstance(ddicdi_models, dict) and "@graph" in ddicdi_models:
        graph_nodes = ddicdi_models.get("@graph", [])
    elif isinstance(ddicdi_models, list):
        graph_nodes = ddicdi_models
    else:
        graph_nodes = [ddicdi_models]
    top_context = {
        "@vocab": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
        "schema": "https://schema.org/",
        "dcterms": "http://purl.org/dc/terms/",
        "geosparql": "http://www.opengis.net/ont/geosparql#",
        "spdx": "http://spdx.org/rdf/terms#",
        "cdi": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
        "time": "http://www.w3.org/2006/time#",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "nx": "https://xas.org/dictionary/",
        "cdifq": "https://cdif.codata.org/concept/",
        "prov": "http://www.w3.org/ns/prov#"
    }

    # Also include the XDI–CDIF mapping JSON-LD generated from the
    # spreadsheet resources, using the same logic as in the notebook.
    try:
        xdi_cdif_mapping = load_xdi_cdif_mapping_jsonld()
    except Exception:
        xdi_cdif_mapping = None

    payload = {
        "@context": top_context,
        "@graph": graph_nodes,
    }

    # Attach the XDI–CDIF mapping JSON-LD derived from the spreadsheet
    if xdi_cdif_mapping is not None:
        payload["xdiCdifMapping"] = xdi_cdif_mapping

    # Also attach the original CDI JSON-LD graph (schema.org-rich) so
    # clients can access the full generated CDI, just like in the
    # `test_cdi_generate.ipynb` notebook.
    try:
        payload["CDIGenerated"] = json.loads(cdi_jsonld)
    except Exception:
        # Fallback: keep raw string if parsing fails for any reason
        payload["CDIGenerated"] = cdi_jsonld

    dataexport = json.dumps(payload)
    return Response(content=dataexport, media_type="application/json")

@app.get("/data/serialize")
def read_data_serialize():
    return Response(content=data.serialize_data(format="json-ld"), media_type="application/json")

@app.get("/data/type")
def read_data_type(subject: str):
    return data.get_type(subject, data.fullgraph)

@app.get("/routes")
def list_routes():
    routes = []
    for r in app.router.routes:
        try:
            routes.append({
                "path": r.path,
                "methods": sorted(list(getattr(r, "methods", set()))),
                "name": getattr(r, "name", None),
            })
        except Exception:
            pass
    return routes

@app.get("/data/properties")
def read_data_properties(subject: str):
    return data.get_related_triples(data.fullgraph, subject)

@app.get("/data/triple_by_triple")
def read_data_triple_by_triple(subject: str):
    return data.triple_by_triple(data.fullgraph, subject)

@app.get("/data/lookup")
def read_data_lookup(subject: str):
    return data.lookup_subject(subject)

@app.get("/data/lookup/predicate")
def read_data_lookup_predicate(predicate: str):
    return data.lookup_predicate(predicate)

@app.get("/data/lookup/object")
def read_data_lookup_object(object: str):
    return data.lookup_object(object)

@app.get("/data/lookup/subject")
def read_data_lookup_subject(subject: str):
    return data.lookup_subject(subject)

@app.post("/dvn")
async def receive_dvn(request: Request, file: Optional[UploadFile] = File(None)):
    # If a file is uploaded via multipart/form-data
    if file is not None:
        content_bytes = await file.read()
        text = content_bytes.decode("utf-8", errors="replace")
        try:
            data = json.loads(text)
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return JSONResponse(content=data)
        except json.JSONDecodeError:
            print(text)
            return PlainTextResponse(content=text)

    # Otherwise, try to read JSON from the request body
    try:
        data = await request.json()
        variables = []
        context = []
        file_details = data.get("datasetFileDetails")
        if isinstance(file_details, list):
            for file_detail in file_details:
                data_tables = file_detail.get("dataTables", [])
                if isinstance(data_tables, list):
                    for table in data_tables:
                        for variable in table.get("dataVariables", []):
                            name = variable.get("name")
                            if name is not None:
                                print(variable)
                                print(name)
                                variables.append(variable)
                                context.append(variable.get("name"))
            output = { "variables": variables, "context": context }
            fullcontext = " ".join(context)
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor(max_workers=min(10, len(variables) or 1)) as executor:
                tasks = []
                for variable in variables:
                    term = variable.get("name")
                    if not term:
                        continue
#                    tasks.append(loop.run_in_executor(executor, partial(fetch_wikilink, term, fullcontext)))
                    tasks.append(loop.run_in_executor(executor, partial(fetch_skosmos, term, fullcontext)))
                    tasks.append(loop.run_in_executor(executor, partial(fetch_remote_ollama, term)))
                results = await asyncio.gather(*tasks)
            output["results"] = list(results)
            return Response(content=json.dumps(output, indent=2, ensure_ascii=False), media_type="application/json")
        else:
            print(json.dumps(variables, indent=2, ensure_ascii=False))
            return JSONResponse(content=variables)
    except json.JSONDecodeError:
        # Fallback: treat body as plain text
        body = await request.body()
        text = body.decode("utf-8", errors="replace")
        print(text)
        return PlainTextResponse(content=text)

@app.get("/ollama")
async def receive_ollama(term: str, model: Optional[str] = os.environ.get("DEFAULTMODEL", "gpt-oss:latest")):
    return run_ollama(term, model)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8012) 
