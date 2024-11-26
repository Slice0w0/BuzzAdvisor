import dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
import os
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableMap
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import logging
from langchain import debug

logging.basicConfig(level=logging.INFO)

dotenv.load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_API_KEY")
COURSE_INFO_CHROMA_PATH = os.getenv("COURSE_INFO_CHROMA_PATH")
MODEL = os.getenv("MODEL")

review_system_template_str = """Your job is to use courses information
provided to answer questions about course prerequisite, 
suggested backgrounds, technical requirements, Contents, Goals, etc. 
Use the following context to answer questions.
Be as detailed as possible, but don't make up any information
that's not from the context. If you don't know an answer, say
you don't know.

{context}
"""

course_info_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"], template=review_system_template_str
    )
)

course_info_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["question"], template="{question}"
    )
)

messages = [course_info_system_prompt, course_info_human_prompt]
course_info_prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"],
    messages=messages,
)
chat_model = ChatOpenAI(model=MODEL, temperature=0, api_key = OPEN_API_KEY)


# Initialize the vector database and retriever
course_info_vector_db = Chroma(
    persist_directory=COURSE_INFO_CHROMA_PATH,
    embedding_function=OpenAIEmbeddings(openai_api_key=OPEN_API_KEY)
)

course_info_retriever = course_info_vector_db.as_retriever(k=5)

# # Define a function to process each document's content and metadata
# def format_with_metadata(documents):
#     logging.info([doc.metadata['source'] for doc in documents["context"]])
#     return [
#         f"Content: {doc.page_content}\nCourse: {doc.metadata['source'].split('/')[-1].rstrip('.json')}"
#         for doc in documents["context"]
#     ]

# # Create a chain that incorporates the formatted documents with metadata
# course_info_chain = (
#     {"context": course_info_retriever, "question": RunnablePassthrough()}
#     | RunnableMap({"context": format_with_metadata, "question": lambda x: x})  # Format context with metadata
#     | course_info_prompt_template
#     | chat_model
#     | StrOutputParser()
# )

course_info_chain = (
    {"context": course_info_retriever, "question": RunnablePassthrough()}
    | course_info_prompt_template
    | chat_model
    | StrOutputParser()
)
