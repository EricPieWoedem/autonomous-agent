from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Metadata for traceability, versioning, and audit purposes.
class MRDMeta(BaseModel):
    generated_at: datetime
    agent_version: str
    input_prompt: str
    target_regions: List[str]
    vertical: str

# A market trend supported by evidence and a confidence score.
class MarketTrend(BaseModel):
    trend: str
    evidence: str
    confidence: float

# Current state of the market with key trends and player performance.
class MarketState(BaseModel):
    summary: str
    key_trends: List[MarketTrend]
    succeeding_players: List[str]
    struggling_players: List[str]

# A behavioral or demographic insight about the target audience.
class AudienceInsight(BaseModel):
    insight: str
    source: str
    confidence: float

# Demographics and behavioral profile of the intended customer base.
class TargetAudience(BaseModel):
    age_range: str
    primary_gender: Optional[str]
    regions: List[str]
    behavioral_insights: List[AudienceInsight]
    acquisition_channels: List[str]

# A competitor with their strengths and weaknesses.
class Competitor(BaseModel):
    name: str
    category: str
    strengths: List[str]
    weaknesses: List[str]
    data_source: str

# Collection of competitors operating in the same market space.
class CompetitiveLandscape(BaseModel):
    competitors: List[Competitor]

# An unmet need in the market representing a potential opportunity.
class ProductGap(BaseModel):
    gap_description: str
    evidence: str
    opportunity_rationale: str

# Analysis of market gaps and unmet customer needs.
class GapAnalysis(BaseModel):
    identified_gaps: List[ProductGap]

# Legal status and regulatory constraints for a specific region.
class RegulatoryRegion(BaseModel):
    region: str
    legal_status: str
    constraints: List[str]
    confidence: float

# Regulatory compliance requirements and risks across target regions.
class RegulatoryAnalysis(BaseModel):
    regions: List[RegulatoryRegion]
    open_risks: List[str]

# A recommended product feature with priority and justification.
class FeatureRecommendation(BaseModel):
    feature: str
    priority: str
    justification: str
    dependencies: List[str]

# Strategic product features recommended based on market analysis.
class StrategicRecommendations(BaseModel):
    features: List[FeatureRecommendation]

# Overall confidence assessment and areas needing further research.
class ConfidenceSummary(BaseModel):
    overall_confidence: float
    weak_areas: List[str]
    recommended_next_steps: List[str]

# Complete market requirements document with all analysis sections.
class MarketRequirementsDocument(BaseModel):
    meta: MRDMeta
    market_state: MarketState
    target_audience: TargetAudience
    competitive_landscape: CompetitiveLandscape
    gap_analysis: GapAnalysis
    regulatory_analysis: RegulatoryAnalysis
    strategic_recommendations: StrategicRecommendations
    confidence_summary: ConfidenceSummary
