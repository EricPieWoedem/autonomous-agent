from typing import List
from datetime import datetime
from pydantic import BaseModel
from models.research import ResearchDomain, ToolName


class ResearchPlan(BaseModel):
    objective: str
    primary_app: str
    comparison_apps: List[str]
    regions: List[str]
    research_domains: List[ResearchDomain]
    tools: List[ToolName]
    minimum_section_confidence: float
    minimum_overall_confidence: float
    assumptions: List[str]
    created_at: datetime
    created_by: str
