from datetime import datetime
from statistics import mean
from models.agent import (
    AgentState,
    AgentContext,
    AgentEvent,
    AgentConfig,
    HumanReviewDecision,
)
from models.validation import ValidationStatus, ValidationIssue, ValidationResult
from models.planning import ResearchPlan
from models.research import (
    ToolName, 
    ToolResult,
    ToolStatus,
    ResearchFinding,
    ResearchSection,
    ResearchReport, 
    ResearchDomain,
)
from models.mrd import (
    MRDMeta,
    MarketState,
    MarketTrend,
    AudienceInsight,
    TargetAudience,
    Competitor,
    CompetitiveLandscape,
    ProductGap,
    GapAnalysis,
    RegulatoryRegion,
    RegulatoryAnalysis,
    FeatureRecommendation,
    StrategicRecommendations,
    ConfidenceSummary,
    MarketRequirementsDocument,
)
from tools.external_tools import (
    search_sensor_tower,
    analyze_sentiment,
    check_regulatory_compliance,
)

class AgentStateMachine:
    def __init__(self, context: AgentContext, config: AgentConfig):
        self.context = context
        self.config = config

    def run(self):
        while self.context.state not in {AgentState.COMPLETED, AgentState.FAILED}:
            if self.context.state == AgentState.PLANNING:
                self._handle_planning()

            elif self.context.state == AgentState.RESEARCH:
                self._handle_research()

            elif self.context.state == AgentState.VALIDATION:
                self._handle_validation()

            elif self.context.state == AgentState.HUMAN_REVIEW:
                self._handle_human_review()

            elif self.context.state == AgentState.SYNTHESIS:
                self._handle_synthesis()

    def _transition(self, new_state: AgentState, message: str):
        self.context.events.append(
            AgentEvent(
                state=new_state,
                message=message,
                timestamp=datetime.utcnow(),
                metadata=None,
            )
        )
        self.context.state = new_state

    def _handle_planning(self):
        plan = self._create_research_plan()
        self.context.research_plan = plan
        self._transition(AgentState.RESEARCH, "Research plan created")

    def _handle_research(self):
        if self.context.research_retry_count >= self.config.max_research_retries:
            self._transition(AgentState.FAILED, "Exceeded maximum research retries")
            return

        report = self._run_research()
        self.context.research_report = report
        self.context.research_retry_count += 1
        self._transition(AgentState.VALIDATION, "Research completed")

    def _handle_validation(self):
        result = self._validate_research()
        self.context.validation_result = result

        if result.status == ValidationStatus.PASS:
            self._transition(AgentState.SYNTHESIS, "Validation passed")

        elif result.status == ValidationStatus.RETRY:
            self._transition(AgentState.RESEARCH, "Validation requested retry")

        elif result.status == ValidationStatus.HUMAN_REVIEW:
            self._transition(AgentState.HUMAN_REVIEW, "Validation requires human review")

        else:
            self._transition(AgentState.FAILED, "Validation failed")

    def _handle_human_review(self):
        decision = self._get_human_decision()
        self.context.human_review = decision

        if decision.approved:
            self._transition(AgentState.SYNTHESIS, "Human review approved")

        else:
            self._transition(AgentState.FAILED, "Human review rejected")

    def _handle_synthesis(self):
        mrd = self._synthesize_mrd()
        self.context.final_mrd = mrd
        self._transition(AgentState.COMPLETED, "MRD synthesis completed")

    def _create_research_plan(self) -> ResearchPlan:
        return ResearchPlan(
            objective=self.context.user_input,
            primary_app="Triumph",
            comparison_apps=["Skillz"],
            regions=["UK", "EU"],
            research_domains=[
                ResearchDomain.MARKET,
                ResearchDomain.AUDIENCE,
                ResearchDomain.COMPETITION,
                ResearchDomain.REGULATION,
            ],
            tools=[
                ToolName.SENSOR_TOWER,
                ToolName.SENTIMENT_ANALYSIS,
                ToolName.REGULATORY_CHECK,
            ],
            minimum_section_confidence=self.config.default_min_section_confidence,
            minimum_overall_confidence=self.config.default_min_overall_confidence,
            assumptions=[
                "The product operates under a skill-based gaming model",
                "Publicly available data reflects current market conditions",
            ],
            created_at=datetime.utcnow(),
            created_by="agent",
        )

    def _run_research(self) -> ResearchReport:
        plan = self.context.research_plan

        if plan is None:
            raise RuntimeError("Research called without a research plan")

        sections = []

        tool_results = []

        market_data = search_sensor_tower(plan.primary_app)
        tool_results.append(
            ToolResult(
                tool_name=ToolName.SENSOR_TOWER,
                status=ToolStatus.SUCCESS,
                data=market_data,
                error_message=None,
                source="Sensor Tower (mocked)",
                collected_at=datetime.utcnow(),
            )
        )

        sentiment_data = analyze_sentiment("TikTok")
        tool_results.append(
            ToolResult(
                tool_name=ToolName.SENTIMENT_ANALYSIS,
                status=ToolStatus.SUCCESS,
                data=sentiment_data,
                error_message=None,
                source="TikTok sentiment (mocked)",
                collected_at=datetime.utcnow(),
            )
        )

        regulatory_data = check_regulatory_compliance("UK/EU")
        tool_results.append(
            ToolResult(
                tool_name=ToolName.REGULATORY_CHECK,
                status=ToolStatus.SUCCESS,
                data=regulatory_data,
                error_message=None,
                source="Regulatory DB (mocked)",
                collected_at=datetime.utcnow(),
            )
        )

        market_section = ResearchSection(
            domain=ResearchDomain.MARKET,
            findings=[
                ResearchFinding(
                    finding="Influencer-driven acquisition is outperforming paid channels",
                    related_tools=[ToolName.SENSOR_TOWER],
                    confidence=0.8,
                    supporting_data=[tool_results[0]],
                )
            ],
            overall_confidence=0.8,
        )

        audience_section = ResearchSection(
            domain=ResearchDomain.AUDIENCE,
            findings=[
                ResearchFinding(
                    finding="Young users engage more with short-session competitive games",
                    related_tools=[ToolName.SENTIMENT_ANALYSIS],
                    confidence=0.7,
                    supporting_data=[tool_results[1]],
                )
            ],
            overall_confidence=0.7,
        )

        competition_section = ResearchSection(
            domain=ResearchDomain.COMPETITION,
            findings=[
                ResearchFinding(
                    finding="Competitors lack IO-style elimination game modes",
                    related_tools=[ToolName.SENSOR_TOWER],
                    confidence=0.65,
                    supporting_data=[tool_results[0]],
                )
            ],
            overall_confidence=0.65,
        )

        regulation_section = ResearchSection(
            domain=ResearchDomain.REGULATION,
            findings=[
                ResearchFinding(
                    finding="Skill-based gaming is conditionally permitted in UK/EU",
                    related_tools=[ToolName.REGULATORY_CHECK],
                    confidence=0.6,
                    supporting_data=[tool_results[2]],
                )
            ],
            overall_confidence=0.6,
        )

        sections.extend(
            [
                market_section,
                audience_section,
                competition_section,
                regulation_section,
            ]
        )

        return ResearchReport(
            sections=sections,
            generated_at=datetime.utcnow(),
        )

    def _get_human_decision(self) -> HumanReviewDecision:
        validation = self.context.validation_result

        if validation is None:
            raise RuntimeError("Human review requested without validation result")

        has_critical_issues = any(
            issue.level == "critical" for issue in validation.issues
        )

        approved = (
            validation.overall_confidence
            >= self.config.default_min_overall_confidence
            and not has_critical_issues
        )

        return HumanReviewDecision(
            approved=approved,
            reviewer="simulated_human",
            notes=(
                "Approved based on sufficient confidence and no critical risks"
                if approved
                else "Rejected due to low confidence or critical risks"
            ),
            decided_at=datetime.utcnow(),
        )

    def _validate_research(self) -> ValidationResult:
        issues = []

        report = self.context.research_report
        plan = self.context.research_plan

        if report is None or plan is None:
            return ValidationResult(
                status=ValidationStatus.FAIL,
                issues=[
                    ValidationIssue(
                        level="critical",
                        message="Missing research report or research plan",
                        related_section="system",
                    )
                ],
                overall_confidence=0.0,
                validated_at=datetime.utcnow(),
            )

        section_map = {section.domain: section for section in report.sections}

        for required_domain in plan.research_domains:
            if required_domain not in section_map:
                issues.append(
                    ValidationIssue(
                        level="error",
                        message=f"Missing required research domain: {required_domain}",
                        related_section=required_domain.value,
                    )
                )

        if issues:
            return ValidationResult(
                status=ValidationStatus.RETRY,
                issues=issues,
                overall_confidence=0.0,
                validated_at=datetime.utcnow(),
            )

        section_confidences = []
        regulatory_confidence = None

        for domain, section in section_map.items():
            section_confidences.append(section.overall_confidence)

            if domain == ResearchDomain.REGULATION:
                regulatory_confidence = section.overall_confidence

            for finding in section.findings:
                if not finding.supporting_data:
                    issues.append(
                        ValidationIssue(
                            level="error",
                            message="Finding has no supporting tool data",
                            related_section=domain.value,
                        )
                    )

        overall_confidence = mean(section_confidences)

        if regulatory_confidence is not None and regulatory_confidence < 0.6:
            return ValidationResult(
                status=ValidationStatus.HUMAN_REVIEW,
                issues=issues,
                overall_confidence=overall_confidence,
                validated_at=datetime.utcnow(),
            )

        if overall_confidence < plan.minimum_overall_confidence:
            return ValidationResult(
                status=ValidationStatus.RETRY,
                issues=issues,
                overall_confidence=overall_confidence,
                validated_at=datetime.utcnow(),
            )

        return ValidationResult(
            status=ValidationStatus.PASS,
            issues=issues,
            overall_confidence=overall_confidence,
            validated_at=datetime.utcnow(),
        )

    def _synthesize_mrd(self) -> MarketRequirementsDocument:
        report = self.context.research_report
        validation = self.context.validation_result

        if report is None or validation is None:
            raise RuntimeError("Synthesis called without validated research")

        section_map = {section.domain: section for section in report.sections}

        market_section = section_map[ResearchDomain.MARKET]
        audience_section = section_map[ResearchDomain.AUDIENCE]
        competition_section = section_map[ResearchDomain.COMPETITION]
        regulation_section = section_map[ResearchDomain.REGULATION]

        market_trends = [
            MarketTrend(
                trend=finding.finding,
                evidence=", ".join(
                    tr.source for tr in finding.supporting_data
                ),
                confidence=finding.confidence,
            )
            for finding in market_section.findings
        ]

        market_state = MarketState(
            summary=" ".join(f.finding for f in market_section.findings),
            key_trends=market_trends,
            succeeding_players=["Triumph"],
            struggling_players=["Skillz"],
        )

        audience_insights = [
            AudienceInsight(
                insight=finding.finding,
                source=", ".join(
                    tr.source for tr in finding.supporting_data
                ),
                confidence=finding.confidence,
            )
            for finding in audience_section.findings
        ]

        target_audience = TargetAudience(
            age_range="18-30",
            primary_gender="Male",
            regions=["UK", "EU"],
            behavioral_insights=audience_insights,
            acquisition_channels=["TikTok", "Influencer referrals"],
        )

        competitors = [
            Competitor(
                name="Triumph",
                category="Skill-based real-money gaming",
                strengths=["Fast games", "Influencer growth"],
                weaknesses=["Limited game modes"],
                data_source="Aggregated research findings",
            )
        ]

        competitive_landscape = CompetitiveLandscape(
            competitors=competitors
        )

        gaps = [
            ProductGap(
                gap_description=finding.finding,
                evidence=", ".join(
                    tr.source for tr in finding.supporting_data
                ),
                opportunity_rationale="Identified unmet opportunity",
            )
            for finding in competition_section.findings
        ]

        gap_analysis = GapAnalysis(
            identified_gaps=gaps
        )

        regulatory_regions = [
            RegulatoryRegion(
                region="UK/EU",
                legal_status="Conditionally permitted",
                constraints=["Age verification", "AML checks"],
                confidence=regulation_section.overall_confidence,
            )
        ]

        regulatory_analysis = RegulatoryAnalysis(
            regions=regulatory_regions,
            open_risks=[
                f.finding for f in regulation_section.findings
            ],
        )

        features = [
            FeatureRecommendation(
                feature=gap.gap_description,
                priority="High",
                justification="Derived from validated gap analysis",
                dependencies=["Real-time matchmaking"],
            )
            for gap in gaps
        ]

        strategic_recommendations = StrategicRecommendations(
            features=features
        )

        confidence_summary = ConfidenceSummary(
            overall_confidence=validation.overall_confidence,
            weak_areas=["Regulatory clarity"],
            recommended_next_steps=[
                "Conduct legal review",
                "Pilot launch in UK",
            ],
        )

        meta = MRDMeta(
            generated_at=datetime.utcnow(),
            agent_version="0.1.0",
            input_prompt=self.context.user_input,
            target_regions=["UK", "EU"],
            vertical="Real-money skill gaming",
        )

        return MarketRequirementsDocument(
            meta=meta,
            market_state=market_state,
            target_audience=target_audience,
            competitive_landscape=competitive_landscape,
            gap_analysis=gap_analysis,
            regulatory_analysis=regulatory_analysis,
            strategic_recommendations=strategic_recommendations,
            confidence_summary=confidence_summary,
        )










