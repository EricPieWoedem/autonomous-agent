from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from models.planning import ResearchPlan
from models.research import ResearchReport
from models.validation import ValidationResult
from models.mrd import MarketRequirementsDocument

class AgentState(str, Enum):
    PLANNING = "planning"
    RESEARCH = "research"
    VALIDATION = "validation"
    HUMAN_REVIEW = "human_review"
    SYNTHESIS = "synthesis"
    COMPLETED = "completed"
    FAILED = "failed"

class HumanReviewDecision(BaseModel):
    approved: bool
    reviewer: str
    notes: str
    decided_at: datetime

class AgentConfig(BaseModel):
    max_research_retries: int
    max_tool_retries: int
    default_min_section_confidence: float
    default_min_overall_confidence: float


class AgentEvent(BaseModel):
    state: AgentState
    message: str
    timestamp: datetime
    metadata: Optional[dict]


class AgentContext(BaseModel):
    user_input: str
    state: AgentState
    research_plan: Optional[ResearchPlan]
    research_report: Optional[ResearchReport]
    validation_result: Optional[ValidationResult]
    human_review: Optional[HumanReviewDecision]
    final_mrd: Optional[MarketRequirementsDocument]
    research_retry_count: int
    tool_retry_count: int
    events: List[AgentEvent]