from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class MRDMeta(BaseModel):
    generated_at: datetime
    agent_version: str
    input_prompt: str
    target_regions: List[str]
    vertical: str

class MarketTrend(BaseModel):
    trend: str
    evidence: str
    confidence: float

class MarketState(BaseModel):
    summary: str
    key_trends: List[MarketTrend]
    succeeding_players: List[str]
    struggling_players: List[str]

class AudienceInsight(BaseModel):
    insight: str
    source: str
    confidence: float

class TargetAudience(BaseModel):
    age_range: str
    primary_gender: Optional[str]
    regions: List[str]
    behavioral_insights: List[AudienceInsight]
    acquisition_channels: List[str]

class Competitor(BaseModel):
    name: str
    category: str
    strengths: List[str]
    weaknesses: List[str]
    data_source: str

class CompetitiveLandscape(BaseModel):
    competitors: List[Competitor]

class ProductGap(BaseModel):
    gap_description: str
    evidence: str
    opportunity_rationale: str

class GapAnalysis(BaseModel):
    identified_gaps: List[ProductGap]

class RegulatoryRegion(BaseModel):
    region: str
    legal_status: str
    constraints: List[str]
    confidence: float

class RegulatoryAnalysis(BaseModel):
    regions: List[RegulatoryRegion]
    open_risks: List[str]

class FeatureRecommendation(BaseModel):
    feature: str
    priority: str
    justification: str
    dependencies: List[str]

class StrategicRecommendations(BaseModel):
    features: List[FeatureRecommendation]

class ConfidenceSummary(BaseModel):
    overall_confidence: float
    weak_areas: List[str]
    recommended_next_steps: List[str]

class MarketRequirementsDocument(BaseModel):
    meta: MRDMeta
    market_state: MarketState
    target_audience: TargetAudience
    competitive_landscape: CompetitiveLandscape
    gap_analysis: GapAnalysis
    regulatory_analysis: RegulatoryAnalysis
    strategic_recommendations: StrategicRecommendations
    confidence_summary: ConfidenceSummary
