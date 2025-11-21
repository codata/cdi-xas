#!/usr/bin/env python3
import argparse
import os
import sys
import json
from typing import Optional
import rdflib


def resolve_api_path() -> None:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    api_path = os.path.join(repo_root, "api")
    if api_path not in sys.path:
        sys.path.insert(0, api_path)


def generate_cdi(source_url: str, export_path: str, export_format: str, resources_dir: Optional[str], dataset_type: Optional[str], datasetid: Optional[str] = None, datasetversion: Optional[str] = None) -> None:
    resolve_api_path()
    from cdi import CDI_DDI

    resources_dir_final = resources_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
    generator = CDI_DDI(
        url=source_url,
        export_file=export_path,
        export_format=export_format,
        resources_dir=resources_dir_final,
        type=dataset_type,
    )
    cdi_graph = generator.parse_cdi()
    # Quick sanity/compatibility check of the CDI graph
    try:
        _ = cdi_graph.serialize(format="json-ld")
    except Exception:
        print("Warning: CDI graph serialization failed; using empty graph as fallback.")
        cdi_graph = rdflib.Graph()
    # Also enrich the graph with schema.org JSON-LD from Dataverse
    schema_url = None
    if datasetid:
        # Try to infer base site from source_url; fallback to dev codata
        try:
            from urlparse import urlparse  # Python2 compat if needed
        except Exception:
            from urllib.parse import urlparse
        try:
            parsed = urlparse(source_url)
            base = parsed.scheme + "://" + parsed.netloc if parsed.scheme and parsed.netloc else "https://dataverse.dev.codata.org"
        except Exception:
            base = "https://dataverse.dev.codata.org"
        schema_url = base.rstrip("/") + "/api/datasets/export?exporter=schema.org&persistentId=" + datasetid
    else:
        # Default example fallback if no datasetid provided
        schema_url = "https://dataverse.dev.codata.org/api/datasets/export?exporter=schema.org&persistentId=doi%3A10.5072/FK2/8MODGT"
    try:
        schema_graph = rdflib.Graph()
        schema_graph.parse(schema_url, format="json-ld")
        # Merge schema_graph into cdi_graph
        for triple in schema_graph:
            cdi_graph.add(triple)
    except Exception:
        # Ignore enrichment errors to not block core generation
        pass
    if export_path and export_format:
        if export_format == "json-ld":
            raw_jsonld = cdi_graph.serialize(format="json-ld")
            try:
                parsed = json.loads(raw_jsonld)
            except Exception:
                parsed = {"@graph": []}
            if isinstance(parsed, dict) and "@graph" in parsed:
                graph_nodes = parsed["@graph"]
            elif isinstance(parsed, list):
                graph_nodes = parsed
            else:
                graph_nodes = [parsed]
            wrapped = {
                "@graph": graph_nodes
            }
            with open(export_path, "w") as f:
                f.write(json.dumps(wrapped, indent=2, ensure_ascii=False))
        elif export_format == "flattened":
            raw_jsonld = cdi_graph.serialize(format="json-ld")
            try:
                from pyld import jsonld as jsonldlib
                doc = json.loads(raw_jsonld)
                flattened = jsonldlib.flatten(doc)
                with open(export_path, "w") as f:
                    f.write(json.dumps(flattened, indent=2, ensure_ascii=False))
            except Exception:
                # Fallback to raw JSON-LD if pyld not available
                with open(export_path, "w") as f:
                    f.write(raw_jsonld)
        else:
            cdi_graph.serialize(destination=export_path, format=export_format)
        print("Exported CDI graph to %s (%s)" % (export_path, export_format))
    return cdi_graph


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate CDI graph from a source URL and export to JSON-LD/Turtle.")
    parser.add_argument("--url", required=True, help="Source URL containing text representation to parse into CDI.")
    parser.add_argument("--out", default="cdi.jsonld", help="Output file path. Default: cdi.jsonld")
    parser.add_argument("--format", dest="fmt", default="json-ld", choices=["json-ld", "turtle"], help="Export format. Default: json-ld")
    parser.add_argument("--resources", default=None, help="Path to resources directory (defaults to ./resources).")
    parser.add_argument("--type", dest="dataset_type", default="xas", help="Dataset type key to load resources for. Default: xas")
    args = parser.parse_args(argv)

    resolve_api_path()
    generate_cdi(args.url, args.out, args.fmt, args.resources, args.dataset_type)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

