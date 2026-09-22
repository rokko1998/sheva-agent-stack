"""Live synthetic Graphify-delta → official Jev acceptance cases. No esc source edits."""

from __future__ import annotations

import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile

import networkx as nx
from networkx.readwrite import json_graph

ROOT = Path(__file__).resolve().parent.parent
review = runpy.run_path(str(ROOT / "scripts/architecture-review"))


def base_graph() -> nx.DiGraph:
    graph = nx.DiGraph()
    for node, file, community in (("api", "api.py", 0), ("service", "service.py", 0),
                                   ("repo", "repo.py", 1)):
        graph.add_node(node, label={"api": "API", "service": "Service", "repo": "Repository"}[node],
                       source_file=file, source_location="L1", community=community, file_type="code")
    graph.add_edge("api", "service", relation="imports_from", confidence="EXTRACTED",
                   source_file="api.py", source_location="L2", source_verified=True)
    return graph


def add_edge(graph, source, target, confidence="EXTRACTED", verified=True):
    graph.add_edge(source, target, relation="imports_from", confidence=confidence,
                   source_file=f"{source}.py", source_location="L3", source_verified=verified)


def write_graph(path: Path, graph: nx.DiGraph) -> None:
    path.write_text(json.dumps(json_graph.node_link_data(graph, edges="links")))


def decide(state: dict) -> tuple[str, str, str, list]:
    process = subprocess.run([shutil.which("python3") or sys.executable,
                              str(ROOT / "scripts/jev-architecture-choice")],
                             input=json.dumps(state), text=True, capture_output=True, check=True)
    raw = json.loads(process.stdout)
    result = review["outcome"](state, raw)
    return (raw["answers"]["structural_assessment"]["choice"],
            raw["answers"]["policy_compliance"]["choice"],
            result["outcome"], result["safety_corrections"])


def main() -> None:
    cases = []
    initial = base_graph()
    a = initial.copy()
    a.add_node("helper", label="API helper", source_file="api.py", source_location="L10", community=0, file_type="code")
    a.add_edge("api", "helper", relation="contains", confidence="EXTRACTED", source_file="api.py",
               source_location="L10", source_verified=True)
    cases.append(("A clean local extension", initial, a, []))
    b = initial.copy()
    add_edge(b, "api", "repo", verified=False)
    cases.append(("B new cross-community dependency", initial, b, []))
    c = initial.copy()
    add_edge(c, "service", "api")
    cases.append(("C new import cycle", initial, c, []))
    rule = [{"source": "fixture-policy:1", "text": "API layer must not depend directly on persistence", "matched": True,
             "role_mapping": {"api": "API layer", "repo": "Repository in persistence layer"},
             "matched_evidence": {"source": "api", "target": "repo", "relation": "imports_from",
                                  "source_file": "api.py", "source_location": "L3",
                                  "source_excerpt": "from repo import Repository",
                                  "explanation": "Direct API import of persistence repository is exactly the forbidden dependency"}}]
    cases.append(("D explicit rule with extracted verified edge", initial, b, rule))
    e = initial.copy()
    add_edge(e, "api", "repo", confidence="AMBIGUOUS", verified=False)
    cases.append(("E ambiguous edge cannot prove violation", initial, e, rule))
    f = initial.copy()
    add_edge(f, "service", "api")
    cases.append(("F existing cycle before baseline", f, f.copy(), []))

    with tempfile.TemporaryDirectory(prefix="graphify-arch-fixture-") as temporary:
        directory = Path(temporary)
        (directory / "api.py").write_text("def endpoint():\n    pass\nfrom repo import Repository\n")
        for index, (name, old, new, rules) in enumerate(cases):
            before = directory / f"{index}-before.json"
            after = directory / f"{index}-after.json"
            write_graph(before, old)
            write_graph(after, new)
            state = review["change_state"](directory, before, after, ["fixture.py"], rules)
            structure, policy, outcome, corrections = decide(state)
            print(json.dumps({"case": name, "native_diff": state["graphify_native_diff_summary"],
                              "new_cycles": len(state["new_cycles"]),
                              "existing_cycles": len(state["existing_cycles"]),
                              "cross_edges": len(state["new_cross_community_edges"]),
                              "Jev_structural": structure, "Jev_policy": policy,
                              "outcome": outcome, "safety_corrections": corrections}))


if __name__ == "__main__":
    main()
