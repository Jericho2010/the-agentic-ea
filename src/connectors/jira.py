"""
Enterprise Jira Issue & Architecture Backlog Connector.
Integrates with Jira REST API (Cloud v3 and Data Center v2) for backlog syncing,
architectural refactoring ticket generation, tech debt tracking, and component traceability.
"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

import requests

from src.connectors.base import EnterpriseConnector, resolve_secret

logger = logging.getLogger("agentic_ea.connectors.jira")


class JiraConnector(EnterpriseConnector):
    """
    Production connector for Jira Cloud & Jira Server/Data Center REST APIs.
    Supports Atlassian Document Format (ADF), JQL issue search, and ticket orchestration.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        email: Optional[str] = None,
        api_token: Optional[str] = None,
        timeout: int = 15,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        resolved_url = base_url or resolve_secret("JIRA_URL") or ""
        super().__init__(
            name="Jira",
            base_url=resolved_url,
            timeout=timeout,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
        )

        self.email = email or resolve_secret("JIRA_EMAIL") or resolve_secret("JIRA_USER")
        self.api_token = api_token or resolve_secret("JIRA_API_TOKEN") or resolve_secret("JIRA_TOKEN")

        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

        if self.email and self.api_token:
            # Standard Jira Cloud Basic Auth (email:api_token)
            self.session.auth = (self.email, self.api_token)
        elif self.api_token:
            # Personal Access Token (Server/Data Center)
            self.session.headers["Authorization"] = f"Bearer {self.api_token}"

    def test_connection(self) -> Dict[str, Any]:
        """
        Tests Jira connectivity by querying the current user's profile (/rest/api/3/myself or v2).
        """
        if not self.base_url or not self.api_token:
            return self._format_result(
                status="UNCONFIGURED",
                latency_ms=0.0,
                details={"error": "Missing Jira URL or API token"},
                message="Jira not configured. Set JIRA_URL and JIRA_API_TOKEN (plus JIRA_EMAIL for Cloud).",
            )

        start = time.perf_counter()
        try:
            # Try v3 first
            resp = self._request("GET", "/rest/api/3/myself")
            if resp.status_code == 404:
                resp = self._request("GET", "/rest/api/2/myself")

            latency_ms = (time.perf_counter() - start) * 1000

            if resp.status_code == 200:
                data = resp.json()
                details = {
                    "displayName": data.get("displayName"),
                    "emailAddress": data.get("emailAddress"),
                    "active": data.get("active"),
                    "accountType": data.get("accountType", "standard"),
                }
                return self._format_result(
                    status="CONNECTED",
                    latency_ms=latency_ms,
                    details=details,
                    message=f"Successfully authenticated with Jira as '{data.get('displayName')}'.",
                )
            elif resp.status_code in (401, 403):
                return self._format_result(
                    status="AUTH_ERROR",
                    latency_ms=latency_ms,
                    details={"status_code": resp.status_code, "error": resp.text},
                    message="Jira authentication failed: invalid API token or email.",
                )
            else:
                return self._format_result(
                    status="UNREACHABLE",
                    latency_ms=latency_ms,
                    details={"status_code": resp.status_code, "error": resp.text},
                    message=f"Jira API returned unexpected HTTP status {resp.status_code}.",
                )
        except requests.RequestException as e:
            latency_ms = (time.perf_counter() - start) * 1000
            return self._format_result(
                status="UNREACHABLE",
                latency_ms=latency_ms,
                details={"error": str(e)},
                message=f"Jira instance unreachable: {str(e)}",
            )

    def search_issues(
        self,
        jql: str,
        max_results: int = 50,
        start_at: int = 0,
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Executes a JQL search across Jira projects and issues.
        """
        endpoint = "/rest/api/3/search"
        payload: Dict[str, Any] = {
            "jql": jql,
            "maxResults": max_results,
            "startAt": start_at,
        }
        if fields:
            payload["fields"] = fields

        resp = self._request("POST", endpoint, json_data=payload)
        if resp.status_code == 404:
            # Fallback to v2
            resp = self._request("POST", "/rest/api/2/search", json_data=payload)

        resp.raise_for_status()
        data = resp.json()
        return data.get("issues", []) if isinstance(data, dict) else []

    def create_issue(
        self,
        project_key: str,
        summary: str,
        description: str,
        issue_type: str = "Task",
        labels: Optional[List[str]] = None,
        components: Optional[List[str]] = None,
        api_version: int = 3,
    ) -> Dict[str, Any]:
        """
        Creates a Jira issue with Atlassian Document Format (ADF) description for Cloud or string for Server.
        """
        if api_version == 3:
            # Standard Jira Cloud ADF format
            desc_field = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description}],
                    }
                ],
            }
        else:
            desc_field = description

        fields: Dict[str, Any] = {
            "project": {"key": project_key},
            "summary": summary,
            "description": desc_field,
            "issuetype": {"name": issue_type},
        }
        if labels:
            fields["labels"] = labels
        if components:
            fields["components"] = [{"name": c} for c in components]

        endpoint = f"/rest/api/{api_version}/issue"
        resp = self._request("POST", endpoint, json_data={"fields": fields})
        resp.raise_for_status()
        return resp.json()

    def get_project_components(self, project_key: str) -> List[Dict[str, Any]]:
        """
        Fetches defined architectural components for a given Jira project.
        """
        endpoint = f"/rest/api/3/project/{project_key}/components"
        resp = self._request("GET", endpoint)
        if resp.status_code == 404:
            resp = self._request("GET", f"/rest/api/2/project/{project_key}/components")

        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else []

    def link_issues(
        self,
        inward_issue_key: str,
        outward_issue_key: str,
        link_type: str = "Relates",
    ) -> Dict[str, Any]:
        """
        Creates an issue link between two issues for architecture traceability.
        """
        endpoint = "/rest/api/3/issueLink"
        payload = {
            "type": {"name": link_type},
            "inwardIssue": {"key": inward_issue_key},
            "outwardIssue": {"key": outward_issue_key},
        }
        resp = self._request("POST", endpoint, json_data=payload)
        if resp.status_code == 404:
            resp = self._request("POST", "/rest/api/2/issueLink", json_data=payload)

        resp.raise_for_status()
        return resp.json() if resp.text else {"status": "linked"}
