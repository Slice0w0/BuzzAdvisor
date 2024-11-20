from agent.course_rag_agent import course_rag_agent_executor
from chains.review_chain import review_chain
import logging

#logging.basicConfig(level=logging.DEBUG)

# response = course_rag_agent_executor.invoke(
#     {
#         "input": (
#             "What's the technical background needed for CS 6515"
#         )
#     }
# )

response = course_rag_agent_executor.invoke(
    {
        "input": (
            "Give some challenging courses"
        )
    }
)

#print(review_chain.invoke("Some challenging coures"))