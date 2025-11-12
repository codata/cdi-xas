from fastapi import FastAPI, Response, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn
from fastapi.responses import JSONResponse, PlainTextResponse
from datalearning import DataLearning
from config import datadir, datafile
from datapoints import CDI_DDI
from cdi import CDI_DDI
import json
app = FastAPI()

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
def read_data_dataset():
    data.add_permanent_schema('dataset')
    #return Response(content=data.serialize_data(format="json-ld"), media_type="application/json")
    datajson = data.export(format="json-ld")
    dataexport = json.dumps({
        "@context": [
            "https://docs.ddialliance.org/DDI-CDI/1.0/model/encoding/json-ld/ddi-cdi.jsonld",
            {"skos": "http://www.w3.org/2004/02/skos/core#"}
        ],      
        "DDICDIModels": [json.loads(datajson)]
    })
    return Response(content=dataexport, media_type="application/json")

@app.get("/datapoints")
def read_datapoints(url: str, format: str = "turtle"):
    cdi = CDI_DDI(url, "cdi.jsonld", format, type='xas')
    if format == "turtle":
        return Response(content=cdi.parse_cdi().serialize(format=format), media_type="text/turtle")
    else:
        return Response(content=cdi.parse_cdi().serialize(format=format), media_type="application/json")

@app.get("/data/serialize")
def read_data_serialize():
    return Response(content=data.serialize_data(format="json-ld"), media_type="application/json")

@app.get("/data/type")
def read_data_type(subject: str):
    return data.get_type(subject, data.fullgraph)

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8012) 