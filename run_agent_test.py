from models.agent import AgentContext, AgentState, AgentConfig
from agent.state_machine import AgentStateMachine

def run_end_to_end_test():
    context = AgentContext(
        user_input="Build a skill-based gaming app like Triumph for the European market, targeting young men.",
        state=AgentState.PLANNING,
        research_plan=None,
        research_report=None,
        validation_result=None,
        human_review=None,
        final_mrd=None,
        research_retry_count=0,
        tool_retry_count=0,
        events=[],
    )

    config = AgentConfig(
        max_research_retries=3,
        max_tool_retries=2,
        default_min_section_confidence=0.6,
        default_min_overall_confidence=0.65,
    )

    agent = AgentStateMachine(context=context, config=config)
    agent.run()

    return context


if __name__ == "__main__":
    final_context = run_end_to_end_test()

    print("\n=== FINAL AGENT STATE ===")
    print(final_context.state)

    print("\n=== EVENT LOG ===")
    for event in final_context.events:
        print(f"[{event.timestamp}] {event.state}: {event.message}")

    print("\n=== MRD OUTPUT (JSON) ===")
    if final_context.final_mrd:
        print(final_context.final_mrd.model_dump())
    else:
        print("No MRD produced")
