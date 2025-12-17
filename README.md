# Overview

This project implements a contract-driven autonomous agent that generates a Market Requirements Document (MRD) from a high-level user prompt.

The goal of the system is not to "sound smart", but to behave like a production-grade engineering system:

- Deterministic
- Auditable
- Structured
- Safe under uncertainty
- Explicit about failures and confidence

The agent follows a state-machine orchestration pattern, enforces strict data contracts using Pydantic, and separates reasoning, validation, and control flow.

## High-Level Flow

```
User Input
   ↓
PLANNING → ResearchPlan
   ↓
RESEARCH → ResearchReport (tool-backed)
   ↓
VALIDATION → ValidationResult
   ↓
(HUMAN REVIEW if needed)
   ↓
SYNTHESIS → Market Requirements Document (MRD)
```

- The agent never skips states
- All transitions are explicit
- All intermediate artifacts are typed and validated

## Project Structure

```
autonomous-agent/
│
├── agent/
│   └── state_machine.py        # Orchestration & control flow
│
├── models/
│   ├── planning.py             # ResearchPlan contract
│   ├── research.py             # Tool & research contracts
│   ├── validation.py           # Validation rules & outcomes
│   ├── mrd.py                  # Final MRD schema
│   └── agent.py                # AgentState, Context, Config
│
├── tools/
│   └── external_tools.py       # Mocked external data sources
│
├── docs/
│   ├── architecture.md         # Mermaid architecture diagram
│   └── agent_orchestration.md  # Orchestration design
│
├── run_agent_test.py           # End-to-end execution test
├── requirements.txt
└── README.md
```

Each directory represents one responsibility only. There is no mixed logic or implicit behavior.

## Key Design Principles

### 1. Contract-First Design

Every important artifact in the system is defined as a Pydantic model:

- Research plans
- Tool outputs
- Research findings
- Validation results
- Final MRD
- Agent state & memory

If data does not match the contract → the system refuses to proceed.

This prevents:

- Hallucinations
- Partial outputs
- Silent corruption

2. Explicit Orchestration

The agent is implemented as a deterministic state machine:

AgentState.PLANNING
AgentState.RESEARCH
AgentState.VALIDATION
AgentState.HUMAN_REVIEW
AgentState.SYNTHESIS
AgentState.COMPLETED
AgentState.FAILED

State transitions are:

Explicit

Logged

Reproducible

The agent never “decides” implicitly — it enforces rules defined in validation logic.

## Evaluation Criteria

**Question:**
Does the system produce structured data we can save to a DB, or just markdown text?

**Answer:**
The system produces fully structured JSON, validated by Pydantic.

**Proof:**

Final output is a MarketRequirementsDocument Pydantic model:

<!--models/mrd.py -->
```python
class MarketRequirementsDocument(BaseModel):
    meta: MRDMeta
    market_state: MarketState
    target_audience: TargetAudience
    competitive_landscape: CompetitiveLandscape
    gap_analysis: GapAnalysis
    regulatory_analysis: RegulatoryAnalysis
    strategic_recommendations: StrategicRecommendations
    confidence_summary: ConfidenceSummary
```

During testing, the MRD is serialized via:

final_context.final_mrd.model_dump()

Output is DB-ready JSON

{
  "meta": {...},
  "market_state": {...},
  "target_audience": {...},
  ...
}

Any missing field → validation error → no MRD produced.

Question:
What happens if “Sensor Tower” returns no data? Does the whole flow crash?

Answer:
No. The system degrades gracefully and reacts deterministically.

Proof:

Tool calls are wrapped in ToolResult:

<!-- models/research.py -->
ToolResult(
    tool_name=ToolName.SENSOR_TOWER,
    status=ToolStatus.EMPTY | FAILED | SUCCESS,
    data=...,
    source=...,
)

Validation logic inspects:

Tool status

Supporting data

Confidence

Outcomes are explicit:

RETRY if data may improve

HUMAN_REVIEW if risk is high

FAIL after bounded retries

Observed during testing:

Missing or weak data → retries

Persistently bad data → controlled failure

High regulatory risk → human review

No crashes. No silent success.

Question:
Can we easily swap out a “Gambling” module for a “SaaS” module later?

Answer:
Yes — without changing orchestration or validation logic.

**Proof:**

Domain logic is isolated in schemas, not code paths.

MRD structure is vertical-agnostic:

<!-- models/mrd.py -->
```
vertical: str
```

Research domains are enums:

<!-- models/research.py -->
```python
class ResearchDomain(Enum):
    MARKET
    AUDIENCE
    COMPETITION
    REGULATION
```

To support SaaS:

- We replace REGULATION logic with compliance rules
- Swap external_tools.py implementations
- Keep the agent, validation, and synthesis logic

This is possible because:

- Orchestration is domain-agnostic
- Validation rules are configurable
- Synthesis is schema-driven

**Question:**
Where does human review happen and how is it enforced?

**Answer:**
Human review is a first-class state.

**Proof:**

Validation can return HUMAN_REVIEW

Agent transitions explicitly:

<!-- agent/sate-machine.py -->
```python
elif result.status == ValidationStatus.HUMAN_REVIEW:
    self._transition(AgentState.HUMAN_REVIEW)
```

Human decisions are structured:

<!-- models/agent.py -->
```python
class HumanReviewDecision(BaseModel):
    approved: bool
    reviewer: str
    notes: str
    decided_at: datetime
```

In this task, review is simulated — but the interface is production-ready.

## Architecture & Orchestration

Architecture diagram: docs/Architecture_Diagram.md

Orchestration design: docs/Orchestration_Design.md

## How to Run

1. Setup

Run the following commands in your terminal

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Run End-to-End Test

Run "python run_agent_test.py" in your terminal

- Final state: AgentState.COMPLETED
- Full event log
- Valid MRD JSON printed

To intentionally run agent fail tests; example, set overall_confidence = 0.4 for audience_section or totally remove one required section under sections.extend([...]) in the file agent/state_machine.py to see the different types of validation errors.






