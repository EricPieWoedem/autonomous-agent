## Orchestration Design

### Overview

This system is designed as a deterministic, state-driven autonomous agent whose responsibility is to transform a high-level product intent into a validated Market Requirements Document (MRD).

Rather than relying on fragile prompt chaining or free-form reasoning, the agent uses an explicit state machine orchestration pattern. Each state has clearly defined inputs, outputs, validation rules, and failure conditions. This ensures reliability, auditability, and extensibility.

The Large Language Model (LLM) is treated as an unreliable component whose outputs are always validated against strict data schemas before being accepted into the system.

### Why a State Machine

The orchestration pattern must answer three core questions:

- How does the agent know what to do next?
- How does the agent know when it has enough data to proceed?
- What happens when data is missing, incomplete, or unreliable?

A state machine is the most appropriate model because it:

- Enforces deterministic control flow
- Allows explicit retry and fallback logic
- Supports conditional human-in-the-loop intervention
- Makes failure states first-class citizens
- Prevents silent hallucinations from propagating

Alternative patterns such as linear pipelines or Directed Acyclic Graphs(DAGs) were rejected due to their inability to handle iterative(loop) research and conditional decision-making.

### High-Level Control Flow

```
START
  ↓
PLANNING
  ↓
RESEARCH ← External Sources 
  ↓
VALIDATION
  ├─ sufficient → SYNTHESIS
  ├─ insufficient (recoverable) → RESEARCH
  ├─ high-risk / ambiguous → HUMAN_REVIEW
  └─ unrecoverable → FAILED
  ↓
SYNTHESIS
  ↓
COMPLETED
```

### Agent States

#### 1. PLANNING

Purpose
Translate the user’s high-level intent into a structured research plan.

Inputs

User prompt (free-text)

Outputs

ResearchPlan object defining:

- Required research dimensions (market, audience, competitors, regulation)
- Target entities (e.g., Triumph)
- Regions of interest (e.g., UK, EU)

Failure Conditions

- Prompt too vague or contradictory
- Missing critical information (e.g., target market)

Transitions

- Success → RESEARCH
- Failure → FAILED or request clarification

#### 2. RESEARCH

Purpose
Execute the research plan using external tools and collect raw evidence.

Inputs

Structured ResearchPlan

Actions

Invoke mocked tools such as:

- Market intelligence lookup (Sensor Tower)
- Sentiment analysis
- Regulatory checks

Outputs

Raw research results stored in the agent context

Each result includes:

- Data payload
- Source
- Timestamp
- Confidence level

Failure Handling

- Tool failures do not crash the system
- Empty or partial results are recorded explicitly

Transitions

- Always → VALIDATION

#### 3. VALIDATION

Purpose
Determine whether the collected data is sufficient and reliable enough to proceed.

Inputs

Raw research results

Validation Checks

- Are all required research dimensions covered?
- Are sources present and credible?
- Are confidence thresholds met?

Outputs

Validation report with one of:

- sufficient
- insufficient_but_recoverable
- high_risk
- unrecoverable

Transitions

- sufficient → SYNTHESIS
- insufficient_but_recoverable → RESEARCH
- high_risk → HUMAN_REVIEW
- unrecoverable → FAILED

#### 4. HUMAN_REVIEW (Conditional)

Purpose
Allow controlled human intervention in high-risk or ambiguous scenarios.

Triggered When

- Regulatory ambiguity
- Conflicting market signals
- Persistently missing critical data

Human Actions

- Approve continuation
- Reject findings
- Modify assumptions

Transitions

- Approved → SYNTHESIS
- Rejected → FAILED

#### 5. SYNTHESIS

Purpose
Transform validated research data into a structured Market Requirements Document.

Constraints

- No new facts may be introduced
- All claims must map back to validated sources

Inputs

Validated research context

Outputs

Draft MRD object validated against strict schema

Failure Conditions

- Schema validation failure
- Missing required MRD fields

Transitions

- Success → COMPLETED
- Failure → FAILED

#### 6. COMPLETED

Purpose
Emit the final, validated MRD as a machine-readable JSON object.

Outputs

- MarketRequirementsDocument (JSON)

This is a terminal success state.

#### 7. FAILED

Purpose
Terminate execution gracefully with structured error information.

Outputs

- Failure reason
- State at which failure occurred
- Diagnostic metadata

This is a terminal failure state, not a system crash.

### Agent Context (Shared State)

The agent maintains a single Agent Context object that persists across states.
This context serves as the system’s source of truth and includes:

- User intent
- Research plan
- Tool outputs
- Validation reports
- Confidence scores
- Execution metadata

All state transitions read from and write to this context.
The agent itself holds no implicit memory.

### Error Handling & Self-Correction

- Tool failures trigger retries or fallback strategies
- Partial data is explicitly marked with confidence scores
- Validation gates prevent low-quality data from entering synthesis
- The agent degrades gracefully instead of hallucinating missing information

### Extensibility

This orchestration model is domain-agnostic:

- Research tools can be swapped (e.g., Gambling → SaaS)
- MRD schemas can evolve independently
- New states can be added without rewriting core logic

The state machine provides a stable backbone for future extensions.

### Summary

This orchestration design prioritizes:

- Determinism over improvisation
- Validation over verbosity
- Reliability over creativity

By explicitly separating planning, research, validation, synthesis, and human oversight, the system avoids common failure modes seen in 
prompt-driven agents and aligns with production-grade engineering principles.
