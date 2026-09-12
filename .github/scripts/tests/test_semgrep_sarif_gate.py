#!/usr/bin/env python3
"""Exercise the real reusable workflow's inline gate, not a copied counter."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest


WORKFLOW = Path(__file__).resolve().parents[2] / "workflows/security-checks-reusable.yml"


class SemgrepSarifGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        step = WORKFLOW.read_text(encoding="utf-8").split(
            "      - name: Enforce Semgrep SARIF findings\n", 1
        )[1]
        cls.gate = textwrap.dedent(step.split("<<'PY'\n", 1)[1].split("          PY\n", 1)[0])

    def run_gate(self, results, fail_on_findings="true", extra_runs=None):
        report = {"runs": [{"results": results}] + (extra_runs or [])}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.sarif"
            path.write_text(json.dumps(report), encoding="utf-8")
            return subprocess.run(
                [sys.executable, "-", str(path), fail_on_findings],
                input=self.gate, text=True, capture_output=True, check=False,
            )

    def test_no_findings_pass(self):
        result = self.run_gate([])
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unsuppressed_finding_blocks(self):
        result = self.run_gate([{"ruleId": "synthetic-open"}])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Semgrep findings: 1", result.stdout)

    def test_semgrep_in_source_suppression_passes(self):
        result = self.run_gate([{"suppressions": [{"kind": "inSource"}]}])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Semgrep findings: 0", result.stdout)

    def test_explicitly_accepted_in_source_suppression_passes(self):
        result = self.run_gate([{"suppressions": [{"kind": "inSource", "status": "accepted"}]}])
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_other_suppression_states_do_not_hide_findings(self):
        for suppression in (
            {"kind": "inSource", "status": "rejected"},
            {"kind": "inSource", "status": "underReview"},
            {"kind": "inSource", "status": "unknown"},
            {"kind": "inSource", "status": None},
            {"kind": "external", "status": "accepted"},
            {"status": "accepted"},
            {},
        ):
            with self.subTest(suppression=suppression):
                result = self.run_gate([{"suppressions": [suppression]}])
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Semgrep findings: 1", result.stdout)

    def test_empty_suppressions_still_block(self):
        result = self.run_gate([{"suppressions": []}])
        self.assertNotEqual(result.returncode, 0)

    def test_mixed_runs_preserve_open_findings(self):
        result = self.run_gate(
            [{"suppressions": [{"kind": "inSource"}]}],
            extra_runs=[{"results": [{"ruleId": "synthetic-open"}]}],
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Semgrep findings: 1", result.stdout)

    def test_existing_report_only_option_is_preserved(self):
        result = self.run_gate([{"ruleId": "synthetic-open"}], fail_on_findings="false")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Semgrep findings: 1", result.stdout)


if __name__ == "__main__":
    unittest.main()
