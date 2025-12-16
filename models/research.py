from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel
from datetime import datetime

class ToolName(str, Enum):
    SENSOR_TOWER = "sensor_tower"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    REGULATORY_CHECK = "regulatory_check"

class ToolStatus(str, Enum):
    SUCCESS = "success"
    EMPTY = "empty"
    FAILED = "failed"

class ToolResult(BaseModel):
    tool_name: ToolName
    status: ToolStatus
    data: Optional[Any]
    error_message: Optional[str]
    source: str
    collected_at: datetime

class MarketIntelligenceResult(ToolResult):
    app_name: str
    region: str

class ResearchFinding(BaseModel):
    finding: str
    related_tools: list[ToolName]
    confidence: float
    supporting_data: list[ToolResult]

class ResearchDomain(str, Enum):
    MARKET = "market"
    AUDIENCE = "audience"
    COMPETITION = "competition"
    REGULATION = "regulation"

class ResearchSection(BaseModel):
    domain: ResearchDomain
    findings: list[ResearchFinding]
    overall_confidence: float

class ResearchReport(BaseModel):
    sections: list[ResearchSection]
    generated_at: datetime