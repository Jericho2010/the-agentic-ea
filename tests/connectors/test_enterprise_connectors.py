"""
Comprehensive Unit Tests for The Agentic EA Enterprise Connectors Framework.
Validates dynamic secret resolution, connection lifecycle, mock HTTP error handling,
bi-directional conversions (Backstage <-> PAM), and ConnectorManager orchestration.
"""
from __future__ import annotations

import base64
import json
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.connectors.backstage import BackstageConnector
from src.connectors.base import EnterpriseConnector, resolve_secret
from src.connectors.github import GitHubConnector
from src.connectors.jira import JiraConnector
from src.connectors.manager import ConnectorManager
from src.connectors.servicenow import ServiceNowConnector


# ============================================================================
# 1. Secret Resolution Tests
# ============================================================================

def test_resolve_secret_from_env(monkeypatch):
    monkeypatch.setenv("TEST_ENTERPRISE_KEY", "super-secret-token-123")
    val = resolve_secret("TEST_ENTERPRISE_KEY")
    assert val == "super-secret-token-123"


def test_resolve_secret_aliases(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("GITHUB_PERSONAL_ACCESS_TOKEN", "pat-token-abc")
    val = resolve_secret("GITHUB_TOKEN")
    assert val == "pat-token-abc"


def test_resolve_secret_default():
    val = resolve_secret("NON_EXISTENT_SECRET_XYZ", default="fallback-val")
    assert val == "fallback-val"


# ============================================================================
# 2. GitHub Connector Tests
# ============================================================================

def test_github_unconfigured(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_PERSONAL_ACCESS_TOKEN", raising=False)
    gh = GitHubConnector(token="")
    res = gh.test_connection()
    assert res["status"] == "UNCONFIGURED"
    assert "not configured" in res["message"]


def test_github_connection_success():
    gh = GitHubConnector(token="ghp_mocktoken")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"login": "octocat-enterprise", "name": "The Enterprise Bot"}
    mock_resp.headers = {
        "X-RateLimit-Remaining": "4950",
        "X-RateLimit-Limit": "5000",
        "X-OAuth-Scopes": "repo, read:org",
    }

    with patch.object(gh.session, "request", return_value=mock_resp):
        res = gh.test_connection()
        assert res["status"] == "CONNECTED"
        assert res["details"]["login"] == "octocat-enterprise"
        assert res["details"]["rate_limit_remaining"] == "4950"
        assert res["latency_ms"] >= 0


def test_github_auth_error():
    gh = GitHubConnector(token="bad_token")
    mock_resp = MagicMock()
    mock_resp.status_code = 401
    mock_resp.text = '{"message": "Bad credentials"}'

    with patch.object(gh.session, "request", return_value=mock_resp):
        res = gh.test_connection()
        assert res["status"] == "AUTH_ERROR"
        assert "authentication failed" in res["message"]


def test_github_unreachable():
    gh = GitHubConnector(token="mock_token")
    with patch.object(gh.session, "request", side_effect=requests.exceptions.ConnectTimeout("Network timed out")):
        res = gh.test_connection()
        assert res["status"] == "UNREACHABLE"
        assert "unreachable" in res["message"]


def test_github_operations():
    gh = GitHubConnector(token="ghp_mock")

    # 1. list_repositories
    mock_repo_resp = MagicMock()
    mock_repo_resp.status_code = 200
    mock_repo_resp.json.return_value = [{"id": 101, "name": "checkout-service", "full_name": "corp/checkout-service"}]
    with patch.object(gh.session, "request", return_value=mock_repo_resp):
        repos = gh.list_repositories(org="corp")
        assert len(repos) == 1
        assert repos[0]["name"] == "checkout-service"

    # 2. get_file_contents with base64 decoding
    raw_text = "architecture: microservice\ntier: Tier-1"
    b64_content = base64.b64encode(raw_text.encode("utf-8")).decode("utf-8")
    mock_file_resp = MagicMock()
    mock_file_resp.status_code = 200
    mock_file_resp.json.return_value = {
        "name": "architecture.yaml",
        "path": "docs/architecture.yaml",
        "encoding": "base64",
        "content": b64_content,
    }
    with patch.object(gh.session, "request", return_value=mock_file_resp):
        file_data = gh.get_file_contents("corp/checkout-service", "docs/architecture.yaml")
        assert file_data["decoded_content"] == raw_text

    # 3. list_pull_requests
    mock_pr_resp = MagicMock()
    mock_pr_resp.status_code = 200
    mock_pr_resp.json.return_value = [{"number": 42, "title": "feat: modernize checkout database"}]
    with patch.object(gh.session, "request", return_value=mock_pr_resp):
        prs = gh.list_pull_requests("corp/checkout-service")
        assert len(prs) == 1
        assert prs[0]["number"] == 42

    # 4. post_pr_comment
    mock_comment_resp = MagicMock()
    mock_comment_resp.status_code = 201
    mock_comment_resp.json.return_value = {"id": 999, "body": "Sentinel Approved"}
    with patch.object(gh.session, "request", return_value=mock_comment_resp):
        comment = gh.post_pr_comment("corp/checkout-service", 42, "Sentinel Approved")
        assert comment["id"] == 999

    # 5. set_commit_status
    mock_status_resp = MagicMock()
    mock_status_resp.status_code = 201
    mock_status_resp.json.return_value = {"state": "success", "context": "ea/sentinel-gate"}
    with patch.object(gh.session, "request", return_value=mock_status_resp):
        status_res = gh.set_commit_status(
            "corp/checkout-service",
            sha="abcdef1234567890",
            state="success",
            description="All EA Sentinel architectural governance policies passed.",
        )
        assert status_res["state"] == "success"

    # Invalid state check
    with pytest.raises(ValueError):
        gh.set_commit_status("corp/checkout-service", sha="abc", state="invalid_state", description="test")


# ============================================================================
# 3. ServiceNow Connector Tests
# ============================================================================

def test_servicenow_instance_normalization():
    sn1 = ServiceNowConnector(instance="dev99999", username="admin", password="pwd")
    assert sn1.base_url == "https://dev99999.service-now.com"

    sn2 = ServiceNowConnector(instance="https://myinstance.service-now.com/", token="bearer_token")
    assert sn2.base_url == "https://myinstance.service-now.com"


def test_servicenow_unconfigured(monkeypatch):
    monkeypatch.delenv("SERVICENOW_INSTANCE", raising=False)
    monkeypatch.delenv("SERVICENOW_TOKEN", raising=False)
    sn = ServiceNowConnector(instance="")
    res = sn.test_connection()
    assert res["status"] == "UNCONFIGURED"


def test_servicenow_connection_success():
    sn = ServiceNowConnector(instance="dev12345", token="mock_sn_token")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"result": [{"sys_id": "sys123", "name": "checkout-db"}]}

    with patch.object(sn.session, "request", return_value=mock_resp):
        res = sn.test_connection()
        assert res["status"] == "CONNECTED"
        assert res["details"]["sample_records_returned"] == 1


def test_servicenow_auth_error():
    sn = ServiceNowConnector(instance="dev12345", username="admin", password="wrong_password")
    mock_resp = MagicMock()
    mock_resp.status_code = 401
    mock_resp.text = '{"error": {"message": "User Not Authenticated"}}'

    with patch.object(sn.session, "request", return_value=mock_resp):
        res = sn.test_connection()
        assert res["status"] == "AUTH_ERROR"


def test_servicenow_operations_and_conformance():
    sn = ServiceNowConnector(instance="dev12345", token="mock_sn_token")

    # 1. fetch_ci_table
    raw_cis = [
        {
            "sys_id": "ci_001",
            "name": "payments-db",
            "sys_class_name": "cmdb_ci_database",
            "operational_status": "Operational",
            "environment": "Production",
            "business_criticality": "Tier-1",
            "support_group": "Data Platform Team",
            "ip_address": "10.0.1.50",
            "correlation_id": "arn:aws:rds:eu-west-1:123456789012:db:payments-db",
        }
    ]
    mock_fetch_resp = MagicMock()
    mock_fetch_resp.status_code = 200
    mock_fetch_resp.json.return_value = {"result": raw_cis}

    with patch.object(sn.session, "request", return_value=mock_fetch_resp):
        cis = sn.fetch_ci_table("cmdb_ci_database")
        assert len(cis) == 1
        assert cis[0]["name"] == "payments-db"

    # 2. sync_cmdb_cis_to_bronze_format
    conformed = sn.sync_cmdb_cis_to_bronze_format(raw_cis)
    assert len(conformed) == 1
    row = conformed[0]
    assert row["sys_id"] == "ci_001"
    assert row["name"] == "payments-db"
    assert row["ci_class"] == "cmdb_ci_database"
    assert row["tier"] == "Tier-1"
    assert row["cloud_resource_id"] == "arn:aws:rds:eu-west-1:123456789012:db:payments-db"
    assert "payments-db" in row["raw_attributes"]
    assert "synced_at" in row

    # 3. create_change_request
    mock_cr_resp = MagicMock()
    mock_cr_resp.status_code = 201
    mock_cr_resp.json.return_value = {"result": {"number": "CHG003001", "sys_id": "cr_101"}}
    with patch.object(sn.session, "request", return_value=mock_cr_resp):
        cr = sn.create_change_request(
            short_description="Decommission Cassandra Legacy Cluster",
            description="Migrating remaining reads to CockroachDB per Target State Blueprint.",
        )
        assert cr["number"] == "CHG003001"

    # 4. update_ci
    mock_update_resp = MagicMock()
    mock_update_resp.status_code = 200
    mock_update_resp.json.return_value = {"result": {"sys_id": "ci_001", "operational_status": "Retired"}}
    with patch.object(sn.session, "request", return_value=mock_update_resp):
        upd = sn.update_ci("cmdb_ci_database", "ci_001", {"operational_status": "Retired"})
        assert upd["operational_status"] == "Retired"


# ============================================================================
# 4. Jira Connector Tests
# ============================================================================

def test_jira_unconfigured(monkeypatch):
    monkeypatch.delenv("JIRA_URL", raising=False)
    monkeypatch.delenv("JIRA_API_TOKEN", raising=False)
    jira = JiraConnector(base_url="", api_token="")
    res = jira.test_connection()
    assert res["status"] == "UNCONFIGURED"


def test_jira_connection_success():
    jira = JiraConnector(base_url="https://company.atlassian.net", email="ea@company.com", api_token="secret_token")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "displayName": "Enterprise Architecture Bot",
        "emailAddress": "ea@company.com",
        "active": True,
        "accountId": "acc_12345",
    }

    with patch.object(jira.session, "request", return_value=mock_resp):
        res = jira.test_connection()
        assert res["status"] == "CONNECTED"
        assert res["details"]["displayName"] == "Enterprise Architecture Bot"


def test_jira_auth_error():
    jira = JiraConnector(base_url="https://company.atlassian.net", email="ea@company.com", api_token="invalid")
    mock_resp = MagicMock()
    mock_resp.status_code = 401
    mock_resp.text = '{"errorMessages": ["Invalid credentials"]}'

    with patch.object(jira.session, "request", return_value=mock_resp):
        res = jira.test_connection()
        assert res["status"] == "AUTH_ERROR"


def test_jira_operations():
    jira = JiraConnector(base_url="https://company.atlassian.net", api_token="pat_mock")

    # 1. search_issues
    mock_search_resp = MagicMock()
    mock_search_resp.status_code = 200
    mock_search_resp.json.return_value = {
        "issues": [
            {"id": "10001", "key": "EA-101", "fields": {"summary": "Refactor legacy payment gateway"}}
        ]
    }
    with patch.object(jira.session, "request", return_value=mock_search_resp):
        issues = jira.search_issues("project = EA AND status = Open")
        assert len(issues) == 1
        assert issues[0]["key"] == "EA-101"

    # 2. create_issue with ADF format (v3)
    mock_create_resp = MagicMock()
    mock_create_resp.status_code = 201
    mock_create_resp.json.return_value = {"id": "10002", "key": "EA-102", "self": "https://company.atlassian.net/rest/api/3/issue/10002"}
    with patch.object(jira.session, "request", return_value=mock_create_resp) as mock_req:
        issue = jira.create_issue(
            project_key="EA",
            summary="Address Cassandra Single Point of Failure (SPOF)",
            description="Identified during S12 Disaster Recovery audit.",
            labels=["ArchitectureModernization", "TechDebt"],
        )
        assert issue["key"] == "EA-102"
        # Verify ADF formatting in payload
        called_payload = mock_req.call_args[1]["json"]
        desc = called_payload["fields"]["description"]
        assert desc["type"] == "doc"
        assert desc["content"][0]["content"][0]["text"] == "Identified during S12 Disaster Recovery audit."

    # 3. get_project_components
    mock_comp_resp = MagicMock()
    mock_comp_resp.status_code = 200
    mock_comp_resp.json.return_value = [{"id": "c1", "name": "Billing"}, {"id": "c2", "name": "Payments"}]
    with patch.object(jira.session, "request", return_value=mock_comp_resp):
        components = jira.get_project_components("EA")
        assert len(components) == 2
        assert components[0]["name"] == "Billing"

    # 4. link_issues
    mock_link_resp = MagicMock()
    mock_link_resp.status_code = 201
    mock_link_resp.text = ""
    with patch.object(jira.session, "request", return_value=mock_link_resp):
        link_res = jira.link_issues("EA-101", "EA-102")
        assert link_res["status"] == "linked"


# ============================================================================
# 5. Backstage Connector Tests
# ============================================================================

def test_backstage_unconfigured(monkeypatch):
    monkeypatch.delenv("BACKSTAGE_URL", raising=False)
    bs = BackstageConnector(base_url="")
    res = bs.test_connection()
    assert res["status"] == "UNCONFIGURED"


def test_backstage_connection_success():
    bs = BackstageConnector(base_url="http://localhost:7007", token="mock_jwt")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = [{"metadata": {"name": "order-service"}}]

    with patch.object(bs.session, "request", return_value=mock_resp):
        res = bs.test_connection()
        assert res["status"] == "CONNECTED"
        assert res["details"]["sample_entities_count"] == 1


def test_backstage_conversions_and_techdocs():
    bs = BackstageConnector(base_url="http://localhost:7007")

    # 1. convert_entity_to_pam_node (Component -> Microservice)
    bs_entity = {
        "apiVersion": "backstage.io/v1alpha1",
        "kind": "Component",
        "metadata": {
            "name": "checkout-service",
            "description": "Core checkout processing engine",
            "tags": ["java", "tier-1", "ecommerce"],
            "annotations": {
                "ea/data_classification": "PII:High",
            },
        },
        "spec": {
            "type": "service",
            "lifecycle": "production",
            "owner": "Checkout Squad",
            "system": "order-processing-system",
        },
    }
    pam_node = bs.convert_entity_to_pam_node(bs_entity)
    assert pam_node["urn"] == "urn:ea:microservice:checkout-service"
    assert pam_node["entity_type"] == "Microservice"
    assert pam_node["tier"] == "Tier-1"
    assert pam_node["data_classification"] == "PII:High"
    assert pam_node["owner"] == "Checkout Squad"
    assert pam_node["properties"]["system"] == "order-processing-system"

    # 2. convert_entity_to_pam_node (Resource -> Database)
    db_entity = {
        "apiVersion": "backstage.io/v1alpha1",
        "kind": "Resource",
        "metadata": {
            "name": "customer-pii-db",
            "tags": ["postgres"],
        },
        "spec": {
            "type": "database",
            "owner": "Data Team",
        },
    }
    pam_db = bs.convert_entity_to_pam_node(db_entity)
    assert pam_db["urn"] == "urn:ea:database:customer-pii-db"
    assert pam_db["entity_type"] == "Database"

    # 3. export_pam_nodes_to_backstage_entities
    exported = bs.export_pam_nodes_to_backstage_entities([pam_node, pam_db])
    assert len(exported) == 2
    assert exported[0]["kind"] == "Component"
    assert exported[0]["spec"]["type"] == "service"
    assert exported[0]["metadata"]["annotations"]["ea.governance/urn"] == "urn:ea:microservice:checkout-service"

    assert exported[1]["kind"] == "Resource"
    assert exported[1]["spec"]["type"] == "database"

    # 4. generate_techdocs_bundle
    adrs = [
        {
            "number": "0001",
            "title": "Adopt CockroachDB for Distributed Orders",
            "status": "Accepted",
            "date": "2026-10-20",
            "context": "Need multi-region transactional consistency without SPOF.",
            "decision": "Migrate to managed CockroachDB cluster.",
        }
    ]
    bundle = bs.generate_techdocs_bundle("checkout-service", adrs=adrs)
    assert "mkdocs.yml" in bundle
    assert "docs/index.md" in bundle
    assert "docs/adrs/ADR-0001.md" in bundle
    assert "CockroachDB" in bundle["docs/adrs/ADR-0001.md"]
    assert "checkout-service" in bundle["docs/index.md"]


# ============================================================================
# 6. Connector Manager Tests
# ============================================================================

def test_connector_manager_orchestration():
    mock_gh = MagicMock(spec=GitHubConnector)
    mock_gh.name = "GitHub"
    mock_gh.test_connection.return_value = {"connector": "GitHub", "status": "CONNECTED", "latency_ms": 12.5}

    mock_sn = MagicMock(spec=ServiceNowConnector)
    mock_sn.name = "ServiceNow"
    mock_sn.test_connection.return_value = {"connector": "ServiceNow", "status": "CONNECTED", "latency_ms": 25.1}
    mock_sn.fetch_ci_table.return_value = [{"sys_id": "ci_1", "name": "app-gateway"}]
    mock_sn.sync_cmdb_cis_to_bronze_format.return_value = [{"sys_id": "ci_1", "name": "app-gateway", "ci_class": "cmdb_ci"}]

    mock_jira = MagicMock(spec=JiraConnector)
    mock_jira.name = "Jira"
    mock_jira.test_connection.return_value = {"connector": "Jira", "status": "UNCONFIGURED", "latency_ms": 0.0}

    mock_bs = MagicMock(spec=BackstageConnector)
    mock_bs.name = "Backstage"
    mock_bs.test_connection.return_value = {"connector": "Backstage", "status": "CONNECTED", "latency_ms": 8.4}
    mock_bs.fetch_entities.return_value = [{"metadata": {"name": "service-x"}}]
    mock_bs.convert_entity_to_pam_node.return_value = {"urn": "urn:ea:microservice:service-x", "name": "service-x"}

    manager = ConnectorManager(
        github=mock_gh,
        servicenow=mock_sn,
        jira=mock_jira,
        backstage=mock_bs,
    )

    # 1. Parallel connection testing
    health_results = manager.test_all_connections(parallel=True)
    assert len(health_results) == 4
    assert health_results["github"]["status"] == "CONNECTED"
    assert health_results["jira"]["status"] == "UNCONFIGURED"

    # 2. Active connectors list
    active = manager.get_active_connectors()
    assert "github" in active
    assert "servicenow" in active
    assert "backstage" in active
    assert "jira" not in active

    # 3. Synchronize to bronze with mock catalog client
    mock_catalog_client = MagicMock()
    mock_catalog_client.save_cmdb_ci.return_value = 1
    mock_catalog_client.merge_nodes.return_value = 1

    sync_report = manager.sync_all_to_bronze(client=mock_catalog_client)
    assert "servicenow" in sync_report["synced_connectors"]
    assert "backstage" in sync_report["synced_connectors"]
    assert sync_report["records_ingested"]["cmdb_ci"] == 1
    assert sync_report["records_ingested"]["pam_nodes_from_backstage"] == 1
    mock_catalog_client.save_cmdb_ci.assert_called_once()
    mock_catalog_client.merge_nodes.assert_called_once()
