import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import JSONLoader

# Load the .env file
load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_API_KEY")

DRIVE_FOLDER = "./data/oms-central/review"
loader = DirectoryLoader(DRIVE_FOLDER, glob='**/*.json', show_progress=True, loader_cls=JSONLoader, loader_kwargs = {'jq_schema':'.props.pageProps.course.reviews[].body', 'text_content': False})
reviews = loader.load()

REVIEWS_CHROMA_PATH = "./data/chroma_data_review/"
reviews_vector_db = Chroma.from_documents(
    reviews, OpenAIEmbeddings(openai_api_key = OPEN_API_KEY), persist_directory=REVIEWS_CHROMA_PATH
)