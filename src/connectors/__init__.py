"""
The Agentic EA Platform — Production Enterprise Connectors Framework.
"""
from src.connectors.backstage import BackstageConnector
from src.connectors.base import EnterpriseConnector, resolve_secret
from src.connectors.github import GitHubConnector
from src.connectors.jira import JiraConnector
from src.connectors.manager import ConnectorManager
from src.connectors.servicenow import ServiceNowConnector

__all__ = [
    "EnterpriseConnector",
    "resolve_secret",
    "GitHubConnector",
    "ServiceNowConnector",
    "JiraConnector",
    "BackstageConnector",
    "ConnectorManager",
]
