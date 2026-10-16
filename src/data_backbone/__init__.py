"""
Databricks Unity Catalog Data Backbone for The Agentic EA.
"""
from src.data_backbone.client import UnityCatalogClient, get_unity_catalog_client
from src.data_backbone.seed import seed_database
from src.data_backbone.catalog import (
    CATALOG_NAME,
    SCHEMA_METAMODEL,
    SCHEMA_BRONZE,
    SCHEMA_SILVER,
    SCHEMA_GOLD,
    DDL_STATEMENTS,
)

__all__ = [
    "UnityCatalogClient",
    "get_unity_catalog_client",
    "seed_database",
    "CATALOG_NAME",
    "SCHEMA_METAMODEL",
    "SCHEMA_BRONZE",
    "SCHEMA_SILVER",
    "SCHEMA_GOLD",
    "DDL_STATEMENTS",
]
