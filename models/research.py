from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel
from datetime import datetime

# Available external research tools for data gathering.
class ToolName(str, Enum):
    SENSOR_TOWER = "sensor_tower"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    REGULATORY_CHECK = "regulatory_check"

# Status of a tool execution result.
class ToolStatus(str, Enum):
    SUCCESS = "success"
    EMPTY = "empty"
    FAILED = "failed"

# Result from executing a research tool with data or error details.
class ToolResult(BaseModel):
    tool_name: ToolName
    status: ToolStatus
    data: Optional[Any]
    error_message: Optional[str]
    source: str
    collected_at: datetime

# Tool result specific to market intelligence data for an app and region.
class MarketIntelligenceResult(ToolResult):
    app_name: str
    region: str

# A single research finding with confidence and supporting evidence.
class ResearchFinding(BaseModel):
    finding: str
    related_tools: list[ToolName]
    confidence: float
    supporting_data: list[ToolResult]

# Categories of research domains for market analysis.
class ResearchDomain(str, Enum):
    MARKET = "market"
    AUDIENCE = "audience"
    COMPETITION = "competition"
    REGULATION = "regulation"

# Research results grouped by domain with overall confidence.
class ResearchSection(BaseModel):
    domain: ResearchDomain
    findings: list[ResearchFinding]
    overall_confidence: float

# Complete research report containing all domain sections.
class ResearchReport(BaseModel):
    sections: list[ResearchSection]
    generated_at: datetime