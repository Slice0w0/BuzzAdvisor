from openai import OpenAI
import streamlit as st
import requests
import os

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8000/course-rag-agent")


def clear_chat_history():
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]


# CS 6220 Learning and Planning Agent
with st.sidebar:
    st.image("frontend/visit-tech.png", use_container_width=True)
    st.header("About")
    st.markdown(
        # """
        # Try this course recommender system
        # """
        """
        Welcome to the **CS 6220 Learning and Planning Agent**, your personalized academic assistant.
        """
    )
    metric = st.selectbox("Major:", ["Computer Science", "Math", "Biology", "Business"])
    openai_api_key = st.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password"
    )
    st.markdown("---")
    st.button("Clear Chat History", on_click=clear_chat_history)
    st.markdown(
        """
        ## Features
        - **Get Courses Review and Information**
        - **Plan Your Academic Path**
        - **Empower Your Academic Growth**
        """
    )
    st.header("Example Questions")
    st.markdown(
        "- Could you recommend the top three most difficult courses which statisfies the foundational requirement?"
    )
    st.markdown(
        "- Could you recommend five courses with the highest rating and the least workload?"
    )
    # st.markdown(
    #     "- At which hospitals are patients complaining about billing and "
    #     "insurance issues?"
    # )
    # "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    # "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    # "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Course Recommender")
st.info("Ask me questions about Gatech Courses")
st.caption("🚀 AI Learning and Planning Agent")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "output" in msg.keys():
            st.markdown(msg["output"])
        if "explanation" in msg.keys():
            with st.status("How was this generated", state="complete"):
                st.info(msg["explanation"])

    # st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    # client = OpenAI(api_key=openai_api_key)
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    data = {"text": prompt}
    with st.spinner("Retrieving Our Databases"):
        response = requests.post(CHATBOT_URL, json=data)
        if response.status_code == 200:
            output_text = response.json()["output"]
            explanation = response.json()["intermediate_steps"]
        else:
            output_text = """An error occurred while processing your message.
            Please try again or rephrase your message."""
            explanation = output_text
    st.chat_message("assistant").markdown(output_text)
    st.status("How was this generated", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation,
        }
    )
    # st.session_state.messages.append({"role": "user", "content": prompt})
    # st.chat_message("user").write(prompt)
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo", messages=st.session_state.messages
    # )
    # msg = response.choices[0].message.content
    # st.session_state.messages.append({"role": "assistant", "content": msg})
    # st.chat_message("assistant").write(msg)
