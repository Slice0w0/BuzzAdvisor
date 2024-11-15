import os
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Define the URI for your SQLite database
db = SQLDatabase.from_uri("sqlite:///data/gatech_courses.db")

# Set up the language model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Define the prompt template, using "question" instead of "input"
template = '''
Given an input question, first create a syntactically correct SQL query to retrieve up to {top_k} results from the database.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables and their columns:

{table_info}.

Question: {input}
'''

# Create the PromptTemplate object with required variables
prompt = PromptTemplate(input_variables=["input", "top_k", "table_info"], template=template)

# Create the SQL query chain using the language model, database, and prompt
sql_query_chain = create_sql_query_chain(llm, db, prompt=prompt)

# Example question to test the prompt
input = "What are the 5 most difficult courses for computer science?"
response = sql_query_chain.invoke({
    "question": input,
    "top_k": 5,  # Specify the number of results to retrieve
    "table_info": db.get_table_info()  # Populate table schema info
})

def get_sql_query():
    return response



