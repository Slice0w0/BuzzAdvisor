import sys
import os
import sqlite3
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI


# Set the OpenAI API key (ensure this is securely stored in production)
os.environ["OPENAI_API_KEY"] = "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" # Replace with your actual OpenAI API key

# Initialize the language model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Define the SQLite database file path
db_path = "data/gatech_courses.db"

def get_sql_query(question):
    # Define the prompt template, using "question" instead of "input"
    db = SQLDatabase.from_uri("sqlite:///data/gatech_courses.db")
    template = '''
    Given an input question, first create a syntactically correct SQL query to retrieve up to {top_k} results from the database.
    Use the following format:

    For example, to answer "What are the 5 most difficult courses for computer science?"? You should return the query : 
    
    SELECT codes, name, workload
    FROM courses
    ORDER BY workload DESC
    LIMIT 5;
    

    Only use the following tables and their columns and select the code for each query by default:

    {table_info}.

    Question: {input}
    '''

    # Create the PromptTemplate object with required variables
    prompt = PromptTemplate(input_variables=["input", "top_k", "table_info"], template=template)

    # Create the SQL query chain using the language model, database, and prompt
    sql_query_chain = create_sql_query_chain(llm, db, prompt=prompt)

    # Example question to test the prompt
    input = question
    response = sql_query_chain.invoke({
    "question": input,
    "top_k": 5,  # Specify the number of results to retrieve
    "table_info": db.get_table_info()  # Populate table schema info
    })
    return response

def execute_sql_query(db_path, query):
    """
    Executes the SQL query on the specified SQLite database.
    Returns the results as a list of tuples.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the SQL query
    cursor.execute(query)
    results = cursor.fetchall()

    # Close the connection
    conn.close()
    print(f"results:{results}")
    return results

def generate_response_with_gpt(question, results):
    """
    Generates a response using GPT based on the query results.
    """
    # Format the results in a structured way for GPT
    
    structured_results = "\n".join([f"{result}" for result in results])

    # Create a prompt for GPT
    prompt = f"""
        You are an assistant with access to a course database. A user has asked the following question:

        Question: "{question}"

        Here is the data retrieved from the database:

        {structured_results}

        Based on this data, please provide a response to answer the user's question in a friendly and informative way.
        """

    # Use GPT to generate a response
   
    gpt_response = llm(prompt)
    return gpt_response


# Example question that matches the context of the SQL query
question = "Could you give a brief introduction for course CS-6400?"

# Retrieve the SQL query from query_database
sql_query = get_sql_query(question)
print(sql_query)

# Execute the SQL query and retrieve the results
results = execute_sql_query(db_path, sql_query)

# Generate a natural language response based on the query results
response = generate_response_with_gpt(question, results)

# Print the response
print("Generated Response:\n", response)
