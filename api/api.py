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
app = FastAPI()

# Ensure repo root is importable to access top-level cdi_generator.py
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
from cdi_generator import generate_cdi

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
    graph = generate_cdi(source_url, None, format, resources, type)
    serialized = graph.serialize(format=format)
    if format == "turtle":
        return Response(content=serialized, media_type="text/turtle")
    return Response(content=serialized, media_type="application/json")

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