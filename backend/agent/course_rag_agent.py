import os
import dotenv

from chains.course_info_chain import course_info_chain
from chains.review_chain import review_chain
from chains.course_rating_chain import generate as course_rating_chain
from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_openai_functions_agent
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()
MODEL = os.getenv("MODEL")

course_agent_prompt = hub.pull("hwchase17/openai-functions-agent")

tools = [
    Tool(
        name="Reviews",
        func=review_chain.invoke,
        description="""Useful when you need to answer questions
        about student experiences, feelings, or any other qualitative
        question such as course recommendations that could be answered 
        about a student using semantic search. Not useful for answering 
        objective questions that involve counting, percentages, aggregations, 
        or listing facts about courses' level of difficulty, rating, and workload, etc.. 
        Use the entire prompt as input to the tool. For instance, 
        if the prompt is "Give me some challenging courses", the input should be
        "Give me some challenging courses".
        """,
    ),
    Tool(
        name="Course_Ratings",
        func=course_rating_chain,
        description="""Useful for answering objective questions that 
        involve counting, percentages, aggregations,  or listing facts 
        about courses' level of difficulty, rating, and workload, etc.. 
        Use the entire prompt as input to the tool. For instance, 
        if the prompt is "Give me the top five most difficult courses", 
        the input should be "Give me the top five most difficult courses".
        """,
    ),
    Tool(
        name="Course_Information",
        func=course_info_chain.invoke,
        description="""Useful when you need to answer questions
        about subject questions about courses' prerequisite, course contents, and workload, etc.. 
        Use the entire prompt as input to the tool. For instance, 
        if the prompt is "What's the technical background needed for CS 6515", the input should be
        "What's the technical background needed for CS 6515"
        """,
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
