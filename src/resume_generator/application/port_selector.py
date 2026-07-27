from resume_generator.adapters.user_processor import JsonUserReader
from resume_generator.application.config import PERSONAL_INFO_DIR
from resume_generator.ports.user_processor import UserDataReader


class Settings:
    def __init__(self):
        pass


def get_user_processor() -> UserDataReader:
    return JsonUserReader(data_dir=PERSONAL_INFO_DIR)
