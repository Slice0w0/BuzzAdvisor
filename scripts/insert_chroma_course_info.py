import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import JSONLoader

DRIVE_FOLDER = "./data/oms-official"
loader = DirectoryLoader(DRIVE_FOLDER, glob='**/*.json', show_progress=True, loader_cls=JSONLoader, loader_kwargs = {'jq_schema':'.', 'text_content': False})
course_info = loader.load()

# Load the .env file
load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_API_KEY")

COURSE_INFO_CHROMA_PATH = "./data/chroma_data_course_info/"
course_info_vector_db = Chroma.from_documents(
    course_info, OpenAIEmbeddings(openai_api_key = OPEN_API_KEY), persist_directory=COURSE_INFO_CHROMA_PATH
)