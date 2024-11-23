# learning-assistant

Learning and Planning LLM Assistant

## packages

```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

## database prep

```bash
python3 scripts/insert_data.py

python3 scripts/insert_chroma_course_info.py

python3 scripts/insert_chroma_review.py
```

## start backend

```bash
fastapi run backend/main.py
```

## start frontend

```bash
streamlit run frontend/chatbot.py
```

## .env

```
OPEN_API_KEY=
OPENAI_API_KEY=

REVIEWS_CHROMA_PATH=./data/chroma_data_review/
COURSE_INFO_CHROMA_PATH=./data/chroma_data_course_info/
MODEL=gpt-3.5-turbo-0125

COURSE_RATING_SQLITE_PATH=data/gatech_courses.db
```
