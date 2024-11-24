import os
import dotenv

from chains.course_info_chain import course_info_chain
from chains.review_chain import review_chain
from chains.course_rating_chain import generate as course_rating_chain
from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory

dotenv.load_dotenv()
MODEL = os.getenv("MODEL")

course_agent_prompt = hub.pull("hwchase17/openai-functions-agent")

tools = [
    Tool(
        name="Reviews",
        func=review_chain.invoke,
        description=(
            "Use this tool to answer questions about student experiences, feelings, or qualitative "
            "aspects such as course recommendations. Not suitable for objective queries involving "
            "statistics or factual details about courses' difficulty, ratings, or workload. "
            "Please pass the entire user question as input to this tool. For example, if the user asks, "
            '"Can you recommend some challenging courses?", pass the full question as input.'
        ),
    ),
    Tool(
        name="Course_Ratings",
        func=course_rating_chain,
        description=(
            "This tool is designed to handle objective questions that involve statistics, percentages, "
            "aggregations, or factual details about courses' difficulty, ratings, and workload. "
            "Ensure you pass the entire user question as input to this tool. For instance, if the user inquires, "
            '"What are the top five most difficult courses?", provide the complete question as input.'
        ),
    ),
    Tool(
        name="Course_Information",
        func=course_info_chain.invoke,
        description=(
            "Utilize this tool to answer questions regarding courses' prerequisites, content, and workload. "
            "It is important to pass the entire user question as input to this tool. For example, if the user asks, "
            '"What technical background is needed for CS 6515?", input the full question.'
        ),
    ),
]


chat_model = ChatOpenAI(
    model=MODEL,
    temperature=0,
)

course_rag_agent = create_openai_functions_agent(
    llm=chat_model,
    prompt=course_agent_prompt,
    tools=tools,
)

course_rag_agent_executor = AgentExecutor(
    agent=course_rag_agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True,
)

memory = ChatMessageHistory(session_id="course-rag")

course_rag_agent_with_chat_history = RunnableWithMessageHistory(
    course_rag_agent_executor,
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)
