from langchain_google_genai import ChatGoogleGenerativeAI

from resume_generator.adapters.json_user_reader import JsonUserReader
from resume_generator.application.config import PERSONAL_INFO_DIR
from resume_generator.ports.user_processor import UserDataReader


def llm_agent():
    return ChatGoogleGenerativeAI(model="gemini-flash-lite-latest", temperature=0)


def user_reader() -> UserDataReader:
    return JsonUserReader(data_dir=PERSONAL_INFO_DIR)
