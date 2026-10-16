"""
Unit tests for PAM JSON Schema contracts.
Validates schemas/pam/nodes.schema.json, edges.schema.json, evidence.schema.json
against positive and negative fixtures.
"""
import json
from pathlib import Path
import jsonschema
import pytest

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas" / "pam"
FIXTURES_DIR = SCHEMA_DIR / "fixtures"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_nodes_schema_valid():
    schema = load_json(SCHEMA_DIR / "nodes.schema.json")
    valid_fixture = load_json(FIXTURES_DIR / "valid_node.json")
    jsonschema.validate(instance=valid_fixture, schema=schema)


def test_nodes_schema_invalid():
    schema = load_json(SCHEMA_DIR / "nodes.schema.json")
    invalid_fixture = load_json(FIXTURES_DIR / "invalid_node.json")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_fixture, schema=schema)


def test_edges_schema_valid():
    schema = load_json(SCHEMA_DIR / "edges.schema.json")
    valid_fixture = load_json(FIXTURES_DIR / "valid_edge.json")
    jsonschema.validate(instance=valid_fixture, schema=schema)


def test_edges_schema_invalid():
    schema = load_json(SCHEMA_DIR / "edges.schema.json")
    invalid_fixture = load_json(FIXTURES_DIR / "invalid_edge.json")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_fixture, schema=schema)


def test_evidence_schema_valid():
    schema = load_json(SCHEMA_DIR / "evidence.schema.json")
    valid_fixture = load_json(FIXTURES_DIR / "valid_evidence.json")
    jsonschema.validate(instance=valid_fixture, schema=schema)


def test_evidence_schema_invalid():
    schema = load_json(SCHEMA_DIR / "evidence.schema.json")
    invalid_fixture = load_json(FIXTURES_DIR / "invalid_evidence.json")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_fixture, schema=schema)
