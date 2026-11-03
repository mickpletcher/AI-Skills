#!/usr/bin/env python3
"""Offline, read-only graph checks. Not an n8n schema validator or security scanner."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def inspect_export(value):
    """Return limited structural findings without executing or echoing payload values."""
    findings = []

    def add(code, path, message, severity="error"):
        findings.append({"code": code, "path": path, "severity": severity, "message": message})

    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())

    if not isinstance(value, dict):
        add("workflow_object", "$", "Expected one workflow object, not an array or request body.")
        return report(findings)
    nodes = value.get("nodes")
    connections = value.get("connections")
    if not isinstance(nodes, list):
        add("nodes_array", "$.nodes", "Expected a nodes array.")
        nodes = []
    elif not nodes:
        add("empty_graph", "$.nodes", "Graph has no nodes; inspect the intended artifact.", "review")
    names, ids = set(), set()
    for index, node in enumerate(nodes):
        path = f"$.nodes[{index}]"
        if not isinstance(node, dict):
            add("node_object", path, "Expected a node object.")
            continue
        name = node.get("name")
        if not nonempty(name):
            add("node_name", path + ".name", "Expected a nonempty node name.")
        elif name in names:
            add("duplicate_name", path + ".name", "Node names must be unique for name-based connections.")
        else:
            names.add(name)
        ident = node.get("id")
        if ident is None:
            add("missing_id", path + ".id", "Node ID absent; verify target import behavior.", "review")
        elif not nonempty(ident):
            add("node_id", path + ".id", "Expected a nonempty string node ID.")
        elif ident in ids:
            add("duplicate_id", path + ".id", "Duplicate node ID.")
        else:
            ids.add(ident)
        if not nonempty(node.get("type")):
            add("node_type", path + ".type", "Expected a node type; availability is not checked.")
        version = node.get("typeVersion")
        if type(version) not in (int, float) or (type(version) is float and not math.isfinite(version)) or version <= 0:
            add("node_version", path + ".typeVersion", "Expected a positive finite node type version.")
        if not isinstance(node.get("parameters"), dict):
            add("node_parameters", path + ".parameters", "Expected a parameters object; parameter schemas are not checked.")
        if node.get("credentials"):
            add("credential_binding", path + ".credentials", "Credential references need local mapping and disclosure review.", "review")
        if node.get("retryOnFail"):
            add("native_retry", path + ".retryOnFail", "Compare native retries with the supplied retry contract and any outer loops.", "review")
        if node.get("onError") or node.get("continueOnFail"):
            add("error_routing", path, "Inspect node-specific handled-error routing and payloads.", "review")
    if not isinstance(connections, dict):
        add("connections_object", "$.connections", "Expected a connections object.")
    else:
        for source_index, (source, kinds) in enumerate(connections.items()):
            # Use ordinal paths rather than copying node names or arbitrary values into reports.
            path = f"$.connections[source#{source_index}]"
            if source not in names:
                add("unknown_source", path, "Connection source is not a declared node.")
            if not isinstance(kinds, dict):
                add("connection_types", path, "Expected connection-type mapping.")
                continue
            for kind_index, (kind, outputs) in enumerate(kinds.items()):
                typed = path + f"[type#{kind_index}]"
                if not nonempty(kind) or not isinstance(outputs, list):
                    add("connection_outputs", typed, "Expected a named connection type with an array of outputs.")
                    continue
                for output_index, edges in enumerate(outputs):
                    output = typed + f"[{output_index}]"
                    if not isinstance(edges, list):
                        add("output_edges", output, "Each output must be an array of edges.")
                        continue
                    for edge_index, edge in enumerate(edges):
                        location = output + f"[{edge_index}]"
                        if not isinstance(edge, dict):
                            add("edge_object", location, "Expected a connection edge object.")
                            continue
                        if not isinstance(edge.get("node"), str) or edge["node"] not in names:
                            add("unknown_target", location, "Connection target is not a declared node.")
                        if edge.get("type") != kind:
                            add("edge_type", location, "Edge type does not match its connection group.")
                        if type(edge.get("index")) is not int or edge["index"] < 0:
                            add("edge_index", location, "Input index must be a nonnegative integer; port availability is not checked.")
    if value.get("active") is True:
        add("active_export", "$.active", "Export is marked active; do not infer safe import or execution state.", "review")
    if value.get("pinData"):
        add("pinned_data", "$.pinData", "Pinned data needs private-data review and is not production isolation.", "review")
    if value.get("staticData"):
        add("static_data", "$.staticData", "Persistent workflow state needs private-data and replay review.", "review")
    return report(findings)


def report(findings):
    return {
        "verification_level": "static",
        "structural_errors": sum(f["severity"] == "error" for f in findings),
        "review_signals": sum(f["severity"] == "review" for f in findings),
        "findings": findings,
        "limits": "No execution, node registry/schema validation, expression evaluation, secret detection, authorization, import, compatibility or runtime verification. Zero findings is not approval or proof of safety.",
    }


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def reject_constant(_value):
    raise ValueError("Non-finite JSON number")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path, help="Path to one already-sanitized workflow JSON object")
    args = parser.parse_args(argv)
    try:
        value = json.loads(args.export.read_text(encoding="utf-8-sig"),
                           object_pairs_hook=reject_duplicate_keys, parse_constant=reject_constant)
    except (OSError, UnicodeError, ValueError, RecursionError):
        # Never echo input, parser excerpts, filenames or secret-bearing payload values.
        print(json.dumps({"verification_level": "static", "error": "Unreadable or invalid JSON input; no workflow was executed."}))
        return 2
    result = inspect_export(value)
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 1 if result["structural_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
