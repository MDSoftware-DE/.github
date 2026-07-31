#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SCRIPTS_DIR.parents[1]
CENTRAL_REUSABLES = (
    "deterministic-builds-reusable.yml",
    "docs-governance-reusable.yml",
    "policy-standards-reusable.yml",
    "quality-gate-reusable.yml",
    "security-checks-reusable.yml",
)
sys.path.insert(0, str(SCRIPTS_DIR))

from validate_runner_policy import validate_repository


class RunnerPolicyValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)
        self.workflow_dir = self.repo_root / ".github" / "workflows"
        self.workflow_dir.mkdir(parents=True)
        self.allowlist_path = self.repo_root / ".github" / "runner-policy-allowlist.json"
        self.repository = "MDSoftware-DE/example"
        self.today = date(2026, 7, 31)
        self.write_allowlist([])

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_workflow(self, name: str, body: str) -> Path:
        path = self.workflow_dir / name
        path.write_text(body, encoding="utf-8")
        return path

    def write_allowlist(self, exceptions: list[dict[str, str]]) -> None:
        payload = {"version": 1, "exceptions": exceptions}
        self.allowlist_path.write_text(json.dumps(payload), encoding="utf-8")

    def validate(self):
        return validate_repository(
            repo_root=self.repo_root,
            repository=self.repository,
            allowlist_path=self.allowlist_path,
            today=self.today,
        )

    def test_accepts_literal_wolverine_labels(self) -> None:
        self.write_workflow(
            "build.yml",
            """jobs:
  build:
    runs-on: [self-hosted, wolverine]
    steps:
      - run: true
""",
        )
        self.assertEqual([], self.validate())

    def test_rejects_ubuntu_latest(self) -> None:
        self.write_workflow(
            "build.yml",
            """jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: true
""",
        )
        findings = self.validate()
        self.assertEqual(1, len(findings))
        self.assertIn("GitHub-hosted", findings[0].reason)
        self.assertEqual("ubuntu-latest", findings[0].value)

    def test_rejects_self_hosted_without_wolverine(self) -> None:
        self.write_workflow(
            "build.yml",
            """jobs:
  build:
    runs-on: [self-hosted]
""",
        )
        findings = self.validate()
        self.assertEqual(1, len(findings))
        self.assertIn("wolverine", findings[0].reason)

    def test_accepts_central_reusable_default(self) -> None:
        self.write_workflow(
            "security.yml",
            """jobs:
  security:
    uses: MDSoftware-DE/.github/.github/workflows/security-checks-reusable.yml@main
""",
        )
        self.assertEqual([], self.validate())

    def test_rejects_reusable_override_to_hosted_runner(self) -> None:
        self.write_workflow(
            "security.yml",
            """jobs:
  security:
    uses: MDSoftware-DE/.github/.github/workflows/security-checks-reusable.yml@main
    with:
      runner_labels: '\"ubuntu-latest\"'
""",
        )
        findings = self.validate()
        self.assertEqual(1, len(findings))
        self.assertEqual("security", findings[0].job)
        self.assertEqual("ubuntu-latest", findings[0].value)

    def test_accepts_exact_unexpired_allowlist_entry(self) -> None:
        self.write_workflow("legacy.yml", "jobs:\n  build:\n    runs-on: ubuntu-latest\n")
        self.write_allowlist(
            [
                {
                    "repository": self.repository,
                    "workflow": ".github/workflows/legacy.yml",
                    "job": "build",
                    "value": "ubuntu-latest",
                    "reason": "Requires an unavailable operating system",
                    "owner": "platform-team",
                    "approval": "https://github.com/MDSoftware-DE/.github/issues/11",
                    "review_date": "2026-08-31",
                }
            ]
        )
        self.assertEqual([], self.validate())

    def test_rejects_expired_allowlist_entry(self) -> None:
        self.write_workflow("legacy.yml", "jobs:\n  build:\n    runs-on: ubuntu-latest\n")
        self.write_allowlist(
            [
                {
                    "repository": self.repository,
                    "workflow": ".github/workflows/legacy.yml",
                    "job": "build",
                    "value": "ubuntu-latest",
                    "reason": "Requires an unavailable operating system",
                    "owner": "platform-team",
                    "approval": "https://github.com/MDSoftware-DE/.github/issues/11",
                    "review_date": "2026-07-01",
                }
            ]
        )
        findings = self.validate()
        self.assertEqual(1, len(findings))
        self.assertIn("expired", findings[0].reason)

    def test_ignores_workflow_examples_outside_active_workflow_directory(self) -> None:
        example = self.repo_root / "docs" / "example.yml"
        example.parent.mkdir()
        example.write_text("jobs:\n  build:\n    runs-on: ubuntu-latest\n", encoding="utf-8")
        self.assertEqual([], self.validate())

    def test_reports_path_and_job_for_each_violation(self) -> None:
        self.write_workflow(
            "mixed.yaml",
            """jobs:
  build:
    runs-on: windows-latest
  test:
    runs-on: [self-hosted]
""",
        )
        findings = self.validate()
        self.assertEqual(2, len(findings))
        self.assertEqual({"build", "test"}, {finding.job for finding in findings})
        self.assertEqual(
            {".github/workflows/mixed.yaml"},
            {finding.workflow for finding in findings},
        )

    def test_central_reusable_defaults_are_wolverine(self) -> None:
        expected_default = "default: '[\"self-hosted\",\"wolverine\"]'"
        failures = []
        for workflow_name in CENTRAL_REUSABLES:
            path = REPOSITORY_ROOT / ".github" / "workflows" / workflow_name
            text = path.read_text(encoding="utf-8")
            runner_block = text.split("runner_labels:", 1)[1].split("\n\npermissions:", 1)[0]
            if expected_default not in runner_block:
                failures.append(f"{workflow_name}: Wolverine default missing")
            if "ubuntu-latest" in runner_block or "nightcrawler" in runner_block:
                failures.append(f"{workflow_name}: stale hosted/runtime example remains")
        self.assertEqual([], failures, "\n".join(failures))

    def test_semgrep_reusable_runs_without_docker(self) -> None:
        path = REPOSITORY_ROOT / ".github" / "workflows" / "security-checks-reusable.yml"
        text = path.read_text(encoding="utf-8")
        semgrep_job = (
            text.split("\n  semgrep:", 1)[1]
            .split("\n  secret-scan:", 1)[0]
        )

        self.assertNotIn("\n    container:", semgrep_job)
        self.assertIn("semgrep==1.170.0", semgrep_job)
        self.assertIn("python3 -m venv", semgrep_job)

    def test_runner_policy_workflows_are_wired(self) -> None:
        central_path = REPOSITORY_ROOT / ".github" / "workflows" / "runner-policy.yml"
        self.assertTrue(central_path.is_file(), "central runner-policy workflow is missing")
        central = central_path.read_text(encoding="utf-8")
        self.assertIn("runs-on: [self-hosted, wolverine]", central)
        self.assertIn("validate_runner_policy.py", central)

        reusable_path = REPOSITORY_ROOT / ".github" / "workflows" / "policy-standards-reusable.yml"
        reusable = reusable_path.read_text(encoding="utf-8")
        self.assertIn("enforce_wolverine_runner_policy:", reusable)
        self.assertIn("path: _org_defaults", reusable)
        self.assertIn("_org_defaults/.github/scripts/validate_runner_policy.py", reusable)

        template_path = REPOSITORY_ROOT / ".github" / "workflow-templates" / "policy-standards.yml"
        template = template_path.read_text(encoding="utf-8")
        self.assertIn("enforce_wolverine_runner_policy: true", template)


if __name__ == "__main__":
    unittest.main()
