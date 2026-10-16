"""
Unit tests for Ingestion connectors and DLT conformance pipeline.
"""
from src.ingestion.ingest_cloud_cur import CloudCURIngestor
from src.ingestion.ingest_github_org import GitHubOrgIngestor
from src.ingestion.dlt_metamodel_pipeline import StandaloneConformancePipeline
from src.data_backbone.client import get_unity_catalog_client


def test_cloud_cur_ingestion():
    ingestor = CloudCURIngestor(provider="AWS")
    records = ingestor.ingest()
    assert len(records) >= 6

    client = get_unity_catalog_client()
    stored = client.get_bronze_records("cloud_resources")
    assert len(stored) >= 6


def test_github_org_ingestion():
    ingestor = GitHubOrgIngestor(org_name="enterprise-org")
    records = ingestor.scan_and_ingest()
    assert len(records) >= 2

    client = get_unity_catalog_client()
    stored = client.get_bronze_records("git_repos")
    assert len(stored) >= 2



def test_dlt_conformance_pipeline():
    pipeline = StandaloneConformancePipeline()
    res = pipeline.run_all()
    assert res["status"] == "success"
    assert res["time_matrix_records"] >= 5

    client = get_unity_catalog_client()
    time_matrix = client.get_time_matrix()
    assert len(time_matrix) >= 5
    drift = client.get_drift_reconciled()
    assert len(drift) >= 1
