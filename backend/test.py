from agent.course_rag_agent import course_rag_agent_executor

response = course_rag_agent_executor.invoke(
    {
        "input": (
            "What's the technical background needed for CS 6515"
        )
    }
)