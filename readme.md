# BuzzAdvisor

A RAG-Based LLM Academic Advisor Agent. BuzzAdvisor can handle multiple types of questions from students, including course reviews, ratings, and information, and provide fast responses with accuracy.

Type of Questions BuzzAdvisor can handle: <br>
1. Review-Related Questions: “Could you recommend me an interesting CS course?”  <br>
2. Course-Specific Questions: ”What are the prerequisites and syllabus for CS 6220?”  <br>
3. Quantitative Questions: What are the 5 most difficult courses in CS?”  <br>


## Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### Load Database

```bash
python3 scripts/insert_data.py
python3 scripts/insert_chroma_course_info.py
python3 scripts/insert_chroma_course_info.py
```

### `.env` file

Need to attach an `.env` file as shown in below in the project root directory

```text
OPEN_API_KEY=<your_api_key>
OPENAI_API_KEY=<the_same_api_key>

REVIEWS_CHROMA_PATH=./data/chroma_data_review/
COURSE_INFO_CHROMA_PATH=./data/chroma_data_course_info/
MODEL=gpt-3.5-turbo-0125

COURSE_RATING_SQLITE_PATH=data/gatech_courses.db
```

## Running the Project

## Start Backend

```bash
fastapi run backend/main.py
```

### Start Frontend

```bash
streamlit run frontend/chatbot.py
```

## Project Structure

- `data/`: stored the raw and processed data
- `frontend/`: the code for the Streamlit frontend
- `backend/`: the code for the backend LangChain architecture and FastAPI endpoints
- `scripts/`: web scrapping and data-processing scripts used

## References

### Open-Source Packages

- Chroma vector database: https://www.trychroma.com/
- SQLite relational database: https://www.sqlite.org/
- LangChain framework for agent construction: https://www.langchain.com/
- Streamlit frontend template: https://llm-examples.streamlit.app
- FastAPI sever endpoints: https://fastapi.tiangolo.com/
- HTML parsing: https://pypi.org/project/beautifulsoup4/

### Dataset

Our dataset is collected through web scrapping over the 
- OMS Central: https://www.omscentral.com/
- OMSCS Website: https://omscs.gatech.edu/current-courses


### Performance Measurement 

We ensembled the following 3 exsiting LLMs to evaluate our solution against the answer to GPT-3.5
- ChatGPT-4o: https://chatgpt.com/
- Qwen2.5: https://tongyi.aliyun.com/
- Llama3.2: https://www.llama.com/
