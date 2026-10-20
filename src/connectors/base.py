"""
Enterprise Connector Framework — Base Abstractions & Utilities.
Provides dynamic Databricks secret resolution, resilient HTTP session management,
and standard enterprise health check contracts.
"""
from __future__ import annotations

import logging
import os
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger("agentic_ea.connectors")


def resolve_secret(key: str, scope: str = "ea_secrets", default: Optional[str] = None) -> Optional[str]:
    """
    Dynamically resolves secrets across enterprise environments:
    1. Databricks Secret Scopes via dbutils.secrets.get(scope, key) if running in Databricks.
    2. Environment variables (os.environ.get) with support for common aliases.
    3. User-provided default fallback.
    """
    # 1. Databricks dbutils discovery
    try:
        import IPython
        ip = IPython.get_ipython()
        if ip and "dbutils" in ip.user_ns:
            dbutils = ip.user_ns["dbutils"]
            val = dbutils.secrets.get(scope=scope, key=key)
            if val:
                return str(val).strip()
    except Exception:
        pass

    try:
        from pyspark.dbutils import DBUtils
        from pyspark.sql import SparkSession
        spark = SparkSession.getActiveSession()
        if spark:
            dbutils = DBUtils(spark)
            val = dbutils.secrets.get(scope=scope, key=key)
            if val:
                return str(val).strip()
    except Exception:
        pass

    # 2. Environment variable check
    env_val = os.environ.get(key)
    if env_val is not None and env_val.strip():
        return env_val.strip()

    # Common aliases lookup
    aliases = {
        "GITHUB_TOKEN": ["GITHUB_PERSONAL_ACCESS_TOKEN", "GH_TOKEN"],
        "GITHUB_PERSONAL_ACCESS_TOKEN": ["GITHUB_TOKEN", "GH_TOKEN"],
        "SERVICENOW_TOKEN": ["SN_TOKEN", "SERVICENOW_BEARER_TOKEN"],
        "SERVICENOW_INSTANCE": ["SN_INSTANCE", "SERVICENOW_URL"],
        "JIRA_API_TOKEN": ["JIRA_TOKEN", "JIRA_PASSWORD"],
        "JIRA_URL": ["JIRA_BASE_URL", "JIRA_HOST"],
        "BACKSTAGE_URL": ["BACKSTAGE_HOST", "BACKSTAGE_BASE_URL"],
    }
    for alias in aliases.get(key, []):
        val = os.environ.get(alias)
        if val is not None and val.strip():
            return val.strip()

    return default


class EnterpriseConnector(ABC):
    """
    Abstract base class for production enterprise connectors.
    Enforces standardized connection testing, secret resolution, and HTTP session lifecycle.
    """

    def __init__(
        self,
        name: str,
        base_url: str,
        timeout: int = 10,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        self.name = name
        self.base_url = base_url.rstrip("/") if base_url else ""
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Configures requests.Session with connection pooling and automated retry policy."""
        session = requests.Session()
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST", "PATCH"],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update({
            "User-Agent": f"The-Agentic-EA-Platform/1.0 ({self.name}-Connector)",
            "Accept": "application/json",
        })
        return session

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Any] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> requests.Response:
        """Dispatches an HTTP request against the base URL with standardized exception handling."""
        clean_endpoint = endpoint.lstrip("/")
        if self.base_url:
            url = f"{self.base_url}/{clean_endpoint}"
        else:
            url = endpoint

        req_timeout = timeout or self.timeout
        req_headers = headers or {}

        response = self.session.request(
            method=method.upper(),
            url=url,
            params=params,
            json=json_data,
            data=data,
            headers=req_headers,
            timeout=req_timeout,
        )
        return response

    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """
        Executes a live health check verifying authentication, network reachability,
        and API endpoint availability.

        Returns standard contract:
        {
            "connector": str,
            "status": "CONNECTED" | "AUTH_ERROR" | "UNREACHABLE" | "UNCONFIGURED",
            "latency_ms": float,
            "details": dict,
            "message": str,
            "tested_at": str (ISO 8601),
        }
        """
        raise NotImplementedError

    def _format_result(
        self,
        status: str,
        latency_ms: float,
        details: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:
        """Formats the standardized connection test response."""
        return {
            "connector": self.name,
            "status": status,
            "latency_ms": round(latency_ms, 2),
            "details": details,
            "message": message,
            "tested_at": datetime.now(timezone.utc).isoformat(),
        }
