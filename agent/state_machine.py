from datetime import datetime
from models.agent import (
    AgentState,
    AgentContext,
    AgentEvent,
    AgentConfig,
    HumanReviewDecision,
)
from models.validation import ValidationStatus
from models.planning import ResearchPlan
from models.research import ResearchReport
from models.mrd import MarketRequirementsDocument

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
        raise NotImplementedError
    
    def _run_research(self) -> ResearchReport:
        raise NotImplementedError
    
    def _validate_research(self):
        raise NotImplementedError

    def _get_human_decision(self) -> HumanReviewDecision:
        raise NotImplementedError

    def _synthesize_mrd(self) -> MarketRequirementsDocument:
        raise NotImplementedError









