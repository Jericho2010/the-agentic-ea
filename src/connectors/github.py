"""
Enterprise GitHub Connector.
Integrates with GitHub REST API for repository inspection, architecture AST manifest scanning,
pull request Sentinel governance checks, and commit status gates.
"""
from __future__ import annotations

import base64
import logging
import time
from typing import Any, Dict, List, Optional

import requests

from src.connectors.base import EnterpriseConnector, resolve_secret

logger = logging.getLogger("agentic_ea.connectors.github")


class GitHubConnector(EnterpriseConnector):
    """
    Production connector for GitHub (Cloud and GitHub Enterprise Server).
    Provides authentication, repository scanning, PR gating, and commit status reporting.
    """

    def __init__(
        self,
        token: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 15,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        resolved_url = base_url or resolve_secret("GITHUB_BASE_URL", default="https://api.github.com")
        super().__init__(
            name="GitHub",
            base_url=resolved_url,
            timeout=timeout,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
        )

        self.token = token or resolve_secret("GITHUB_TOKEN") or resolve_secret("GITHUB_PERSONAL_ACCESS_TOKEN")
        if self.token:
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            })

    def test_connection(self) -> Dict[str, Any]:
        """
        Tests GitHub connectivity by querying authenticated user info or rate limits.
        """
        if not self.token:
            return self._format_result(
                status="UNCONFIGURED",
                latency_ms=0.0,
                details={"error": "Missing token"},
                message="GitHub token not configured. Set GITHUB_TOKEN or GITHUB_PERSONAL_ACCESS_TOKEN.",
            )

        start = time.perf_counter()
        try:
            resp = self._request("GET", "/user")
            latency_ms = (time.perf_counter() - start) * 1000

            if resp.status_code == 200:
                data = resp.json()
                details = {
                    "login": data.get("login"),
                    "name": data.get("name"),
                    "rate_limit_remaining": resp.headers.get("X-RateLimit-Remaining"),
                    "rate_limit_limit": resp.headers.get("X-RateLimit-Limit"),
                    "scopes": resp.headers.get("X-OAuth-Scopes", ""),
                }
                return self._format_result(
                    status="CONNECTED",
                    latency_ms=latency_ms,
                    details=details,
                    message=f"Successfully authenticated as GitHub user '{data.get('login')}'.",
                )
            elif resp.status_code in (401, 403):
                return self._format_result(
                    status="AUTH_ERROR",
                    latency_ms=latency_ms,
                    details={"status_code": resp.status_code, "error": resp.text},
                    message="GitHub authentication failed: invalid or expired credentials.",
                )
            else:
                return self._format_result(
                    status="UNREACHABLE",
                    latency_ms=latency_ms,
                    details={"status_code": resp.status_code, "error": resp.text},
                    message=f"GitHub API returned unexpected HTTP status {resp.status_code}.",
                )
        except requests.RequestException as e:
            latency_ms = (time.perf_counter() - start) * 1000
            return self._format_result(
                status="UNREACHABLE",
                latency_ms=latency_ms,
                details={"error": str(e)},
                message=f"GitHub API unreachable: {str(e)}",
            )

    def list_repositories(
        self,
        org: Optional[str] = None,
        type: str = "all",
        per_page: int = 30,
        page: int = 1,
    ) -> List[Dict[str, Any]]:
        """
        Lists repositories for an organization or authenticated user.
        """
        endpoint = f"/orgs/{org}/repos" if org else "/user/repos"
        params = {"type": type, "per_page": per_page, "page": page}
        resp = self._request("GET", endpoint, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else []

    def get_file_contents(
        self,
        repo: str,
        path: str,
        ref: str = "main",
    ) -> Dict[str, Any]:
        """
        Retrieves file contents from a repository, automatically decoding base64 payload.
        """
        endpoint = f"/repos/{repo}/contents/{path.lstrip('/')}"
        params = {"ref": ref}
        resp = self._request("GET", endpoint, params=params)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, dict) and data.get("encoding") == "base64" and "content" in data:
            try:
                decoded = base64.b64decode(data["content"]).decode("utf-8")
                data["decoded_content"] = decoded
            except Exception as e:
                logger.warning(f"Failed to decode base64 content for {path}: {e}")
                data["decoded_content"] = ""
        return data

    def list_pull_requests(
        self,
        repo: str,
        state: str = "open",
        per_page: int = 30,
        page: int = 1,
    ) -> List[Dict[str, Any]]:
        """
        Lists pull requests for a given repository.
        """
        endpoint = f"/repos/{repo}/pulls"
        params = {"state": state, "per_page": per_page, "page": page}
        resp = self._request("GET", endpoint, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else []

    def post_pr_comment(
        self,
        repo: str,
        pr_number: int,
        comment: str,
    ) -> Dict[str, Any]:
        """
        Posts an architectural review or Sentinel gate comment on a Pull Request.
        """
        endpoint = f"/repos/{repo}/issues/{pr_number}/comments"
        resp = self._request("POST", endpoint, json_data={"body": comment})
        resp.raise_for_status()
        return resp.json()

    def set_commit_status(
        self,
        repo: str,
        sha: str,
        state: str,
        description: str,
        context: str = "ea/sentinel-gate",
        target_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Sets a commit status check on a commit SHA (state: pending | success | error | failure).
        """
        valid_states = {"pending", "success", "error", "failure"}
        if state not in valid_states:
            raise ValueError(f"Invalid commit state '{state}'. Must be one of {valid_states}.")

        endpoint = f"/repos/{repo}/statuses/{sha}"
        payload: Dict[str, Any] = {
            "state": state,
            "description": description[:140],  # GitHub limits description to 140 chars
            "context": context,
        }
        if target_url:
            payload["target_url"] = target_url

        resp = self._request("POST", endpoint, json_data=payload)
        resp.raise_for_status()
        return resp.json()
