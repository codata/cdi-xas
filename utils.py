#!/usr/bin/env python3
"""
Utility functions shared across the CDI-XAS project.

Includes helpers for loading the XDI–CDIF mapping spreadsheet that
is stored in this repository under ``resources/XDI-CDIF-Mapping.xlsx``
and published via GitHub at:
`https://github.com/codata/cdi-xas/raw/refs/heads/ai/resources/XDI-CDIF-Mapping.xlsx`.
"""

import json
import os
from io import BytesIO
from typing import Any, Dict, Optional

import pandas as pd
import requests


def get_repo_root() -> str:
    """
    Return the absolute path to the repository root (directory that
    contains this ``utils.py`` module).
    """
    return os.path.dirname(os.path.abspath(__file__))


def get_resources_dir(resources_dir: Optional[str] = None) -> str:
    """
    Resolve the resources directory.

    - If ``resources_dir`` is provided, it is returned unchanged.
    - Otherwise, ``<repo_root>/resources`` is used.
    """
    if resources_dir:
        return resources_dir
    return os.path.join(get_repo_root(), "resources")


def load_xdi_cdif_mapping(
    resources_dir: Optional[str] = None,
    use_remote_fallback: bool = True,
    mapping_url: str = "https://github.com/codata/cdi-xas/raw/refs/heads/ai/resources/XDI-CDIF-Mapping.xlsx",
) -> pd.DataFrame:
    """
    Load the XDI–CDIF mapping spreadsheet as a :class:`pandas.DataFrame`.

    The function first tries to read the local copy at
    ``<resources_dir>/XDI-CDIF-Mapping.xlsx``. If that file is not found
    and ``use_remote_fallback`` is ``True``, it downloads the spreadsheet
    from the provided ``mapping_url`` (by default the public GitHub URL).

    Parameters
    ----------
    resources_dir:
        Optional path to a resources directory. If ``None``, the default
        ``<repo_root>/resources`` directory is used.
    use_remote_fallback:
        If ``True`` (default) and the local file does not exist, attempt to
        download the spreadsheet from ``mapping_url``.
    mapping_url:
        URL to download the spreadsheet from if the local file is missing
        and remote fallback is enabled. Defaults to the public GitHub raw URL.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the spreadsheet contents.

    Raises
    ------
    FileNotFoundError
        If the local file is missing and ``use_remote_fallback`` is ``False``.
    requests.HTTPError
        If the remote download fails (non-2xx response).
    """
    resources_path = get_resources_dir(resources_dir)
    local_path = os.path.join(resources_path, "XDI-CDIF-Mapping.xlsx")

    # Prefer local copy if available
    if os.path.exists(local_path):
        return pd.read_excel(local_path)

    if not use_remote_fallback:
        raise FileNotFoundError(
            f"XDI–CDIF mapping not found at {local_path} and remote fallback disabled."
        )

    # Fallback: fetch from the provided URL
    response = requests.get(mapping_url, timeout=30)
    response.raise_for_status()
    return pd.read_excel(BytesIO(response.content))


def _parse_json_like_fragment(fragment: str) -> Any:
    """
    Try to interpret a JSON-like fragment such as::

        "prop": [ { ... ],

    as a proper JSON object. On success returns the parsed Python
    structure (typically a dict); on failure returns the original
    fragment string.
    """
    # Normalise whitespace and trailing commas
    fragment = fragment.strip().rstrip(",")

    def _balance_brackets(text: str) -> str:
        """
        Heuristically close unbalanced brackets/braces in a
        JSON-like fragment.
        """
        open_sq = text.count("[")
        close_sq = text.count("]")
        open_curly = text.count("{")
        close_curly = text.count("}")

        extra = ""
        # If both braces and brackets are unbalanced, we assume the
        # pattern is `[ { ...` and close the object first, then the
        # array: `}]`.
        if open_curly > close_curly and open_sq > close_sq:
            extra += "}" * (open_curly - close_curly)
            extra += "]" * (open_sq - close_sq)
        else:
            # Otherwise, just close any remaining brackets/braces
            if open_sq > close_sq:
                extra += "]" * (open_sq - close_sq)
            if open_curly > close_curly:
                extra += "}" * (open_curly - close_curly)
        return text + extra

    candidates = []
    balanced = _balance_brackets(fragment)
    candidates.append("{" + balanced + "}")
    # Also try the simpler case (only wrapping, no balancing)
    if balanced != fragment:
        candidates.append("{" + fragment + "}")

    for wrapped in candidates:
        try:
            return json.loads(wrapped)
        except Exception:
            continue

    return fragment


def xdi_cdif_mapping_to_jsonld(
    df: pd.DataFrame,
    base_uri: str = "https://w3id.org/cdi-xas/mapping/",
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Convert a DataFrame containing the XDI–CDIF mapping into a JSON-LD structure.

    Each row becomes a node in the ``@graph``. Columns are turned into JSON
    properties using the column names as keys; empty/NaN values are omitted.

    Parameters
    ----------
    df:
        DataFrame as returned by :func:`load_xdi_cdif_mapping`.
    base_uri:
        Base URI used to mint simple ``@id`` values for each mapping row,
        e.g. ``<base_uri>0``, ``<base_uri>1``.
    context:
        Optional JSON-LD ``@context`` dictionary to include in the result.

    Returns
    -------
    dict
        A JSON-LD document of the form ``{\"@graph\": [...]}``, optionally
        including an ``\"@context\"``.
    """
    graph = []
    for idx, row in df.iterrows():
        node: Dict[str, Any] = {"@id": f"{base_uri}{idx}"}
        for col, value in row.items():
            # Skip entirely empty cells
            if pd.isna(value):
                continue
            col_name = str(col)
            # Normalise Excel auto-generated headers like "Unnamed: 2" to a
            # more stable form such as "Column2"
            if col_name.startswith("Unnamed:"):
                _, _, suffix = col_name.partition(":")
                suffix = suffix.strip()
                # e.g. "Unnamed: 2" -> "Column 2"
                col_name = f"Column {suffix}" if suffix else "Column"

            # Try to interpret string values that look like JSON fragments
            # (e.g. `"schema:additionalProperty": [ {...} ]`) as structured
            # objects, otherwise keep the original value.
            if isinstance(value, str):
                stripped = value.strip()
                parsed_value: Any = value

                # Case 1: complete JSON string (starts with { or [)
                if stripped.startswith("{") or stripped.startswith("["):
                    try:
                        parsed_value = json.loads(stripped)
                    except Exception:
                        parsed_value = value
                # Case 2: JSON-like fragment starting with a quoted key
                elif stripped.startswith('"') and '":' in stripped:
                    maybe_parsed = _parse_json_like_fragment(stripped)
                    # Accept only if we actually got a structured value back
                    if not isinstance(maybe_parsed, str):
                        parsed_value = maybe_parsed

                node[col_name] = parsed_value
            else:
                node[col_name] = value
        graph.append(node)

    jsonld: Dict[str, Any] = {"@graph": graph}
    if context is not None:
        jsonld["@context"] = context
    return jsonld


def load_xdi_cdif_mapping_jsonld(
    resources_dir: Optional[str] = None,
    use_remote_fallback: bool = True,
    mapping_url: str = "https://github.com/codata/cdi-xas/raw/refs/heads/ai/resources/XDI-CDIF-Mapping.xlsx",
    base_uri: str = "https://w3id.org/cdi-xas/mapping/",
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Convenience helper that loads the XDI–CDIF mapping and returns it as JSON-LD.

    Parameters mirror :func:`load_xdi_cdif_mapping` and
    :func:`xdi_cdif_mapping_to_jsonld`.
    """
    df = load_xdi_cdif_mapping(
        resources_dir=resources_dir,
        use_remote_fallback=use_remote_fallback,
        mapping_url=mapping_url,
    )
    return xdi_cdif_mapping_to_jsonld(df, base_uri=base_uri, context=context)


__all__ = [
    "get_repo_root",
    "get_resources_dir",
    "load_xdi_cdif_mapping",
    "xdi_cdif_mapping_to_jsonld",
    "load_xdi_cdif_mapping_jsonld",
]


