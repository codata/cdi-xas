#!/usr/bin/env python3
import argparse
import os
import sys
from typing import Optional


def resolve_api_path() -> None:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    api_path = os.path.join(repo_root, "api")
    if api_path not in sys.path:
        sys.path.insert(0, api_path)


def generate_cdi(source_url: str, export_path: str, export_format: str, resources_dir: Optional[str], dataset_type: Optional[str]) -> None:
    from cdi import CDI_DDI

    resources_dir_final = resources_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
    generator = CDI_DDI(
        url=source_url,
        export_file=export_path,
        export_format=export_format,
        resources_dir=resources_dir_final,
        type=dataset_type,
    )
    graph = generator.parse_cdi()
    if export_path and export_format:
        graph.serialize(destination=export_path, format=export_format)
        print("Exported CDI graph to %s (%s)" % (export_path, export_format))


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

