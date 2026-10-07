"""Illustrative PAM Pydantic sketch — not a runtime dependency of this docs repo."""
from __future__ import annotations
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class Layer(str, Enum):
    STRATEGY = "strategy"
    APPLICATION = "application"
    TECHNOLOGY = "technology"
    DATA = "data"
    GOVERNANCE = "governance"


class RelationshipType(str, Enum):
    REALIZES = "realizes"
    SERVES = "serves"
    HOSTED_ON = "hosted_on"
    ACCESSES = "accesses"
    CONSUMES = "consumes"
    EXPOSES = "exposes"
    FLOWS_TO = "flows_to"
    GOVERNS = "governs"
    THREATENS = "threatens"
    BUNDLED_IN = "bundled_in"
    OWNED_BY = "owned_by"


class MetamodelNode(BaseModel):
    urn: str = Field(..., description="urn:ea:<layer>:<type>:<slug>")
    name: str
    layer: Layer
    type: str
    owner_team: Optional[str] = None
    repo_url: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)


class MetamodelEdge(BaseModel):
    source_urn: str
    target_urn: str
    relation: RelationshipType
    attributes: Dict[str, Any] = Field(default_factory=dict)
