"""
Unit tests for EA Sentinel Governance Gate.
Tests policy enforcement (EA-POL-001, EA-POL-002, EA-POL-003),
Tri-Modal execution, and visual delta diagram compilation.
"""
from pathlib import Path
import pytest
from src.sentinel.gate import EASentinelGate

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(scope="module")
def sentinel_gate():
    return EASentinelGate(provider="subscription_cli")


def test_sentinel_violating_patch(sentinel_gate):
    patch_path = FIXTURES_DIR / "pr_unapproved_db.patch"
    patch_content = patch_path.read_text(encoding="utf-8")

    res = sentinel_gate.evaluate_patch(patch_content)
    assert res["passed"] is False
    assert res["status"] == "REJECTED"
    assert res["violations_count"] == 3

    policy_ids = {v["policy_id"] for v in res["violations"]}
    assert "EA-POL-001" in policy_ids  # Cassandra unapproved
    assert "EA-POL-002" in policy_ids  # Unencrypted PII
    assert "EA-POL-003" in policy_ids  # Missing OwnerTeam / Tier

    assert "RED" in res["markdown_report"] or "BLOCKED" in res["markdown_report"]
    assert Path(res["diagrams"]["html_path"]).exists()
    assert Path(res["diagrams"]["svg_path"]).exists()


def test_sentinel_clean_patch(sentinel_gate):
    patch_path = FIXTURES_DIR / "pr_clean.patch"
    patch_content = patch_path.read_text(encoding="utf-8")

    res = sentinel_gate.evaluate_patch(patch_content)
    assert res["passed"] is True
    assert res["status"] == "APPROVED"
    assert res["violations_count"] == 0
    assert "PASSED" in res["markdown_report"]
