from agent.course_rag_agent import course_rag_agent_executor
from fastapi import FastAPI
from models.course_rag_query import CourseQueryInput, CourseQueryOutput

app = FastAPI(
    title="GT Course Chatbot",
    description="Endpoints for a GT course selection assistant RAG chatbot",
)

async def invoke_agent_with_retry(query: str):
    """
    Retry the agent if a tool fails to run. This can help when there
    are intermittent connection issues to external APIs.
    """

    return await course_rag_agent_executor.ainvoke({"input": query})


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/course-rag-agent")
async def query_course_agent(
    query: CourseQueryInput,
) -> CourseQueryOutput:
    query_response = await invoke_agent_with_retry(query.text)
    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]

    return query_response
