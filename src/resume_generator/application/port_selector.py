from langchain_google_genai import ChatGoogleGenerativeAI

from resume_generator.adapters.user_processor import JsonUserReader
from resume_generator.application.config import PERSONAL_INFO_DIR
from resume_generator.ports.user_processor import UserDataReader


def get_llm_agent():
    return ChatGoogleGenerativeAI(model="gemini-flash-lite-latest", temperature=0)


def get_user_processor() -> UserDataReader:
    return JsonUserReader(data_dir=PERSONAL_INFO_DIR)
