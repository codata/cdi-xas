# CDIF Service prototype

Cross-disciplinary Interoperability Framework is a service designed to deliver AI-ready DDI-CDI variable cascades, enabling seamless integration with leading data repositories such as Dataverse, Kaggle, Zenodo, as well as compatibility with emerging machine learning standards like Croissant ML. It provides a structured foundation for connecting diverse datasets across domains, ensuring interoperability, reusability, and readiness for advanced AI and ML applications.

Quick start:

```
cp .env_sample .env
docker-compose build
docker-compose up -d
```

## API Overview

All endpoints are exposed by the FastAPI application in `api/api.py`. By default the service runs on port `8012` in Docker Compose, or port `80` inside the container image.

Base URL examples:

- **Local (docker-compose)**: `http://localhost:8012`
- **Deployed dev**: `https://cdif-4-xas.dev.codata.org`

Below `GET /path` and `POST /path` are relative to the chosen base URL.

## Core CDI endpoints

### `GET /`

Health/info endpoint, returns a simple JSON banner:

- **Response**: `{"message": "DDI-CDI Service v.0.1"}`

### `GET /cdi`

Generate a CDI graph for a dataset and return JSON-LD, enriched with:

- a framed/compacted CDI `@graph` using schema.org-style context,
- `xdiCdifMapping`: JSON-LD representation of the XDI–CDIF spreadsheet mapping,
- `CDIGenerated`: the original CDI graph as JSON-LD (schema.org rich).

**Query parameters**:

- **url** (optional): direct URL to a data file (e.g. Dataverse access URL).
- **fileid** (optional): Dataverse file ID.
- **siteUrl** (optional): Dataverse base URL (e.g. `https://dataverse.dev.codata.org`).
- **format** (default: `json-ld`): CDI export format (`json-ld` or `turtle` – internally CDI is always serialized to JSON-LD for wrapping).
- **resources** (optional): custom resources directory path.
- **type** (default: `xas`): dataset type key.
- **datasetid**, **datasetversion**, **locale**: passed through for downstream enrichment and compatibility.

If both `fileid` and `siteUrl` are provided, the service constructs:

```text
<siteUrl>/api/access/datafile/<fileid>
```

and uses it as the `url`.

### `GET /cdi-intermidiate`

Low-level CDI generator used mainly for debugging.

**Query parameters**:

- **url** (required): source URL for the dataset (e.g. Dataverse access URL).
- **format** (default: `turtle`): either `turtle` or `json-ld`.

**Response**:

- `text/turtle` when `format=turtle`.
- `application/json` when `format=json-ld`.

### `GET /datapoints`

Expose CDI datapoints directly.

**Query parameters**:

- **url** (required): dataset URL (e.g. Dataverse file URL).
- **format** (default: `turtle`): `turtle` or `json-ld`.

## XDI–CDIF mapping endpoints

### `GET /mapping/xdi-cdif`

Return the XDI–CDIF mapping derived from the Excel spreadsheet as JSON-LD or RML (Turtle).

**Query parameters**:

- **spreadsheet_url** (optional): URL or file path to an `.xlsx` mapping file.
- **export** (optional): `"json-ld"` or `"rml"`.
  - If missing and **fileid** is provided → defaults to `"rml"`.
  - Otherwise → defaults to `"json-ld"`.
- **fileid**, **siteUrl**, **datasetid**, **datasetversion**, **locale**:
  - If `spreadsheet_url` is **not** given and both `fileid` and `siteUrl` are set, the service builds:
    - `spreadsheet_url = <siteUrl>/api/access/datafile/<fileid>`
  - Other parameters are accepted for symmetry with `/cdi` and future extension.

**Behaviour**:

- When a (derived) spreadsheet URL is available:
  - Reads the Excel via `pandas.read_excel`.
  - If `export=rml` → returns `text/turtle` with RML TriplesMaps.
  - Else → returns JSON-LD with `@graph` of mapping entries.
- When no URL is available:
  - Falls back to the built‑in mapping in `resources/XDI-CDIF-Mapping.xlsx` (or the GitHub URL) using `utils.load_xdi_cdif_mapping(_jsonld|_to_rml)`.

Example (JSON-LD mapping for a Dataverse file):

```text
GET /mapping/xdi-cdif?fileid=41&siteUrl=https://dataverse.dev.codata.org
```

Example (RML mapping from GitHub-hosted spreadsheet [`https://github.com/codata/cdi-xas/raw/refs/heads/ai/resources/XDI-CDIF-Mapping.xlsx`](https://github.com/codata/cdi-xas/raw/refs/heads/ai/resources/XDI-CDIF-Mapping.xlsx)):

```text
GET /mapping/xdi-cdif?spreadsheet_url=https://github.com/codata/cdi-xas/raw/refs/heads/ai/resources/XDI-CDIF-Mapping.xlsx&export=rml
```

## Data-learning / inspection endpoints

These endpoints use the `DataLearning` class to introspect and expose a CDI‑encoded dataset configuration.

### `GET /data`

Return the full loaded data as a Pandas‑like JSON table (for debugging).

### `GET /data/example`

Load and return an example CDI dataset.

**Query parameters**:

- **configurationfile** (optional): path or filename of a configuration file.
  - If not provided, uses the default `datafile` from `config.py`.

**Response**:

- JSON-LD with:
  - `@context` for DDI-CDI and SKOS.
  - `DDICDIModels`: list of models exported from `DataLearning`.

### `GET /data/dataset`

Generate data + CDI graph for a particular dataset configuration.

**Query parameters**:

- **url** (required): path/URL of a JSON-LD configuration file.

**Response**:

- JSON with:
  - `DDICDIModels`: exported `DataLearning` models.
  - `CDIGenerated`: CDI graph generated by `generate_cdi`.

### `GET /data/serialize`

Return the entire loaded data as serialized JSON-LD from `DataLearning`.

### `GET /data/type`

**Query parameters**:

- **subject** (required): IRI/identifier of a node.

Returns the RDF type(s) of the subject from the full graph.

### `GET /data/properties`

**Query parameters**:

- **subject** (required): IRI/identifier of a node.

Returns all related triples for that subject.

### `GET /data/triple_by_triple`

**Query parameters**:

- **subject** (required).

Returns triples related to the subject in a “triple by triple” view.

### Lookup helpers

- **`GET /data/lookup?subject=...`** – lookup a subject.
- **`GET /data/lookup/predicate?predicate=...`** – lookup triples by predicate.
- **`GET /data/lookup/object?object=...`** – lookup triples by object.
- **`GET /data/lookup/subject?subject=...`** – alias for subject lookup.

## DVN webhook endpoint

### `POST /dvn`

Intended as a Dataverse webhook/receiver.

- If a file is uploaded as `multipart/form-data` (`file` field):
  - Tries to parse it as JSON, otherwise returns the raw text.
- If no file is uploaded:
  - Tries to parse JSON body expecting Dataverse dataset metadata (e.g. `datasetFileDetails`).
  - Extracts `dataVariables`, spawns parallel SKOS & Ollama lookups, and returns an enriched JSON payload.

## Ollama / AI endpoint

### `GET /ollama`

Proxy to an Ollama‑compatible text generation service for variable descriptions.

**Query parameters**:

- **term** (required): variable name / concept to describe.
- **model** (optional; default from `DEFAULTMODEL` env var): model identifier.

**Response**:

- JSON with `{"name": <term>, "ollama": <parsed_or_raw_response>}`.

## Utility endpoint

### `GET /routes`

Return a JSON list of all registered FastAPI routes (path, methods, name). Useful for quick inspection and debugging. ***!
