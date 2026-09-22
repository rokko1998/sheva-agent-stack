from __future__ import annotations

from pathlib import Path
import runpy
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent
REVIEW = runpy.run_path(str(ROOT / "scripts/architecture-review"))
PROJECT = runpy.run_path(str(ROOT / "scripts/graphify-project"))
JEV = runpy.run_path(str(ROOT / "scripts/jev-architecture-choice"))


class ArchitectureReviewContractTests(unittest.TestCase):
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

    def test_compliant_without_explicit_rule_becomes_not_applicable(self):
        state = {"added_edges": [], "matched_project_rules": []}
        response = {"answers": {"structural_assessment": {"choice": "CLEAN"},
                                "policy_compliance": {"choice": "COMPLIANT"}}}
        result = REVIEW["outcome"](state, response)
        self.assertEqual(result["choices"]["policy_compliance"], "NOT_APPLICABLE")
        self.assertEqual(result["outcome"], "PASS")

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


if __name__ == "__main__":
    unittest.main()
