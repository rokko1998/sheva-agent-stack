from __future__ import annotations

from pathlib import Path
import runpy
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import networkx as nx
from networkx.readwrite import json_graph
import json


ROOT = Path(__file__).resolve().parent.parent
REVIEW = runpy.run_path(str(ROOT / "scripts/architecture_review.py"))
PROJECT = runpy.run_path(str(ROOT / "scripts/graphify-project"))
JEV = runpy.run_path(str(ROOT / "scripts/jev-architecture-choice"))


class ArchitectureReviewContractTests(unittest.TestCase):
    def test_canonical_command_path_is_executable(self):
        process = subprocess.run([str(ROOT / "scripts/architecture-review"), "--help"],
                                 text=True, capture_output=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn("usage: scripts/architecture-review", process.stdout)

    def test_choice_policy_is_complete(self):
        questions = JEV["questions"]()
        self.assertEqual(tuple(questions), ("structural_assessment", "policy_compliance"))
        self.assertEqual(tuple(questions["structural_assessment"]["criteria"]),
                         ("CLEAN", "CONCERN", "UNCERTAIN"))
        self.assertEqual(tuple(questions["policy_compliance"]["criteria"]),
                         ("COMPLIANT", "VIOLATED", "NOT_APPLICABLE", "UNCERTAIN"))

    def test_unreliable_violation_is_downgraded(self):
        state = {"added_edges": [{"source": "api", "target": "repo", "relation": "imports_from",
                                   "confidence": "AMBIGUOUS", "source_verified": True}],
                 "matched_project_rules": [{"matched_evidence": {"source": "api", "target": "repo",
                                                                    "relation": "imports_from"}}]}
        response = {"answers": {"structural_assessment": {"choice": "UNCERTAIN"},
                                "policy_compliance": {"choice": "VIOLATED"}}}
        result = REVIEW["outcome"](state, response)
        self.assertEqual(result["choices"]["policy_compliance"], "UNCERTAIN")
        self.assertEqual(result["outcome"], "NEEDS_REVIEW")
        self.assertTrue(result["requires_inspection"])

    def test_fabricated_rule_cannot_support_violation_with_real_edge(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "architecture.md").write_text("Actual rule allows this dependency\n")
            (project / "api.py").write_text("first\nsecond\nfrom repo import Repository\n")
            old = nx.DiGraph()
            old.add_node("api", label="API", source_file="api.py", community=0, file_type="code")
            old.add_node("repo", label="Repository", source_file="repo.py", community=1, file_type="code")
            new = old.copy()
            new.add_edge("api", "repo", relation="imports_from", confidence="EXTRACTED",
                         source_file="api.py", source_location="L3")
            before = project / "before.json"
            after = project / "after.json"
            before.write_text(json.dumps(json_graph.node_link_data(old, edges="links")))
            after.write_text(json.dumps(json_graph.node_link_data(new, edges="links")))
            rule = {"source_file": "architecture.md", "source_location": "L1",
                    "text": "Invented rule forbids this dependency", "matched": True,
                    "matched_evidence": {"source": "api", "target": "repo",
                                         "relation": "imports_from", "source_file": "api.py",
                                         "source_location": "L3",
                                         "source_excerpt": "from repo import Repository"}}
            state = REVIEW["change_state"](project, before, after, ["api.py"], [rule])
            self.assertTrue(state["added_edges"][0]["source_verified"])
            self.assertFalse(state["explicit_project_rules"][0]["source_verified"])
            self.assertEqual(state["reliable_policy_evidence"], [])
            response = {"answers": {"structural_assessment": {"choice": "CONCERN"},
                                    "policy_compliance": {"choice": "VIOLATED"}}}
            result = REVIEW["outcome"](state, response)
            self.assertEqual(result["choices"]["policy_compliance"], "UNCERTAIN")
            self.assertEqual(result["outcome"], "NEEDS_REVIEW")

    def test_verified_rule_and_matching_edge_preserve_violation(self):
        edge = {"source": "api", "target": "repo", "relation": "imports_from",
                "confidence": "EXTRACTED", "source_verified": True}
        state = {"added_edges": [edge], "matched_project_rules": [],
                 "reliable_policy_evidence": [{"rule_source_verified": True, "edge": edge}],
                 "new_cycles": [], "truncated": {}}
        response = {"answers": {"structural_assessment": {"choice": "CONCERN"},
                                "policy_compliance": {"choice": "VIOLATED"}}}
        result = REVIEW["outcome"](state, response)
        self.assertEqual(result["choices"]["policy_compliance"], "VIOLATED")
        self.assertEqual(result["outcome"], "NEEDS_REVIEW")

    def test_compliant_without_explicit_rule_becomes_not_applicable(self):
        state = {"added_edges": [], "matched_project_rules": []}
        response = {"answers": {"structural_assessment": {"choice": "CLEAN"},
                                "policy_compliance": {"choice": "COMPLIANT"}}}
        result = REVIEW["outcome"](state, response)
        self.assertEqual(result["choices"]["policy_compliance"], "NOT_APPLICABLE")
        self.assertEqual(result["outcome"], "PASS")

    def test_new_cycle_cannot_remain_clean(self):
        state = {"new_cycles": [{"cycle": ["a.py", "b.py"]}], "truncated": {},
                 "added_edges": [], "matched_project_rules": [], "reliable_policy_evidence": []}
        response = {"answers": {"structural_assessment": {"choice": "CLEAN"},
                                "policy_compliance": {"choice": "NOT_APPLICABLE"}}}
        result = REVIEW["outcome"](state, response)
        self.assertEqual(result["choices"]["structural_assessment"], "CONCERN")
        self.assertEqual(result["outcome"], "CONCERN")

    def test_truncated_material_delta_cannot_remain_clean(self):
        state = {"new_cycles": [], "truncated": {"nodes": False, "edges": True},
                 "added_edges": [], "matched_project_rules": [], "reliable_policy_evidence": []}
        response = {"answers": {"structural_assessment": {"choice": "CLEAN"},
                                "policy_compliance": {"choice": "NOT_APPLICABLE"}}}
        result = REVIEW["outcome"](state, response)
        self.assertEqual(result["choices"]["structural_assessment"], "UNCERTAIN")
        self.assertEqual(result["outcome"], "NEEDS_REVIEW")

    def test_cycle_rotations_are_same_directed_cycle(self):
        before = REVIEW["cycle_keys"]([{"cycle": ["a", "b", "c"]}])
        after = REVIEW["cycle_keys"]([{"cycle": ["b", "c", "a", "b"]}])
        reverse = REVIEW["cycle_keys"]([{"cycle": ["a", "c", "b"]}])
        self.assertEqual(before, after)
        self.assertFalse(after - before)
        self.assertFalse(before - after)
        self.assertNotEqual(before, reverse)

    def test_graphify_section_replace_preserves_other_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            original = "PREAMBLE\n\n## user-rules\nkeep exact  \n\n## graphify\nold\n\n## suffix\nkeep\n"
            (project / "AGENTS.md").write_text(original)
            self.assertTrue(PROJECT["replace_rules"](project, "## graphify\nnew\n"))
            actual = (project / "AGENTS.md").read_text()
            self.assertTrue(actual.startswith("PREAMBLE\n\n## user-rules\nkeep exact  \n\n"))
            self.assertTrue(actual.endswith("## suffix\nkeep\n"))
            self.assertEqual(actual.count("## graphify"), 1)

    def test_source_excerpt_must_match_cited_line(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "api.py").write_text("first\nsecond\nfrom repo import Repository\n")
            edge = {"source": "api", "target": "repo", "relation": "imports_from",
                    "source_file": "api.py", "source_location": "L3"}
            evidence = {**edge, "source_excerpt": "from repo import Repository"}
            rule = {"source": "policy:1", "text": "API must not import persistence",
                    "matched": True, "matched_evidence": evidence}
            self.assertTrue(REVIEW["verified_rule_edge"](project, edge, [rule]))
            evidence["source_excerpt"] = "fabricated"
            self.assertFalse(REVIEW["verified_rule_edge"](project, edge, [rule]))

    def test_explicit_rule_must_match_real_policy_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "architecture.md").write_text("# Rules\nAPI must not import persistence\nEnd\n")
            rule = {"source_file": "architecture.md", "source_location": "L2",
                    "text": "API must not import persistence", "matched": True}
            self.assertTrue(REVIEW["verify_explicit_rule"](project, rule))
            rule.update(source_location="L2-L3", text="API must not import persistence\nEnd")
            self.assertTrue(REVIEW["verify_explicit_rule"](project, rule))
            rule["text"] = "Invented rule"
            self.assertFalse(REVIEW["verify_explicit_rule"](project, rule))
            rule.update(source_file="../outside.md", source_location="L1", text="outside")
            self.assertFalse(REVIEW["verify_explicit_rule"](project, rule))

    def test_existing_nodes_use_baseline_community_membership(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            old = nx.DiGraph()
            old.add_node("a", label="A", source_file="a.py", community=0, file_type="code")
            old.add_node("b", label="B", source_file="b.py", community=0, file_type="code")
            new = old.copy()
            new.nodes["b"]["community"] = 1
            new.add_edge("a", "b", relation="imports_from", confidence="EXTRACTED",
                         source_file="a.py", source_location="L1")
            before = project / "before.json"
            after = project / "after.json"
            before.write_text(json.dumps(json_graph.node_link_data(old, edges="links")))
            after.write_text(json.dumps(json_graph.node_link_data(new, edges="links")))
            state = REVIEW["change_state"](project, before, after, [], [])
            self.assertEqual(state["new_cross_community_edges"], [])
            self.assertEqual(state["added_edges"][0]["community_boundary_basis"], "BASELINE")
            self.assertFalse(state["added_edges"][0]["crosses_community_boundary"])

    def test_new_node_boundary_is_marked_post_change_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            old = nx.DiGraph()
            old.add_node("a", label="A", source_file="a.py", community=0, file_type="code")
            new = old.copy()
            new.add_node("b", label="B", source_file="b.py", community=1, file_type="code")
            new.add_edge("a", "b", relation="imports_from", confidence="EXTRACTED",
                         source_file="a.py", source_location="L1")
            before = project / "before.json"
            after = project / "after.json"
            before.write_text(json.dumps(json_graph.node_link_data(old, edges="links")))
            after.write_text(json.dumps(json_graph.node_link_data(new, edges="links")))
            state = REVIEW["change_state"](project, before, after, [], [])
            self.assertEqual(state["new_cross_community_edges"][0]["community_boundary_basis"],
                             "POST_CHANGE_NEW_NODE")

    def test_graphify_update_pins_python_hash_seed(self):
        with patch.object(REVIEW["subprocess"], "run") as run:
            run.return_value = object()
            REVIEW["graphify_update"](Path("/tmp/project"))
            self.assertEqual(run.call_args.kwargs["env"]["PYTHONHASHSEED"], "0")


if __name__ == "__main__":
    unittest.main()
