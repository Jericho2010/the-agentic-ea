"""
Unit tests for EA Navigator Estate Intelligence Engine.
Tests graph traversal, blast radius calculation, financial exposure,
PII lineage detection, and MADR generation.
"""
import pytest
from src.navigator.engine import EstateIntelligenceEngine


@pytest.fixture(scope="module")
def engine():
    return EstateIntelligenceEngine()


def test_resolve_node_urn(engine):
    urn1 = engine.resolve_node_urn("payments-api")
    assert urn1 == "urn:ea:microservice:payments-api"

    urn2 = engine.resolve_node_urn("urn:ea:database:billing-db")
    assert urn2 == "urn:ea:database:billing-db"


def test_blast_radius_payments_api(engine):
    blast = engine.calculate_blast_radius("payments-api")
    assert blast["found"] is True
    assert blast["target"]["name"] == "payments-api"
    # Payments API has upstream callers (e.g. checkout-service, web-storefront)
    assert blast["upstream_count"] >= 1
    # Check financial exposure
    assert blast["financial_exposure"]["total_annual_risk_usd"] > 0
    # Customer PII detected across payments flow
    assert blast["pii_compliance"]["has_pii_exposure"] is True
    # Criticality tier
    assert blast["aggregate_criticality"] in ("Tier-0", "Tier-1")


def test_blast_radius_billing_db(engine):
    blast = engine.calculate_blast_radius("billing-db")
    assert blast["found"] is True
    assert blast["target"]["name"] == "billing-db"
    assert blast["target"]["kind"] == "Database"
    assert blast["upstream_count"] >= 2


def test_madr_generation(engine):
    madr = engine.generate_madr("payments-api")
    assert "# ADR-002: Modernization & Risk Mitigation for payments-api" in madr
    assert "## Context and Problem Statement" in madr
    assert "## Decision Drivers" in madr
    assert "## Decision Outcome" in madr
    assert "Databricks Unity Catalog" in madr


def test_codriving_actions(engine):
    actions = engine.get_codriving_actions("payments-api")
    assert len(actions) >= 4
    labels = [a["label"] for a in actions]
    assert any("Simulate" in l for l in labels)
    assert any("ADR" in l for l in labels)
