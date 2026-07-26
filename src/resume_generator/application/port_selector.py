from resume_generator.adapters.job_context import JobContextGeneratorImpl
from resume_generator.adapters.llm.llm_enum import LLM
from resume_generator.adapters.llm.llm_gemini import GeminiAdapter
from resume_generator.adapters.llm.llm_lmstudio import LMStudioAdapter
from resume_generator.adapters.user_processor import JsonUserProcessor
from resume_generator.application.config import DATA_DIR
from resume_generator.ports.job_context_generator import JobContextGenerator
from resume_generator.ports.llm import LLMInterface
from resume_generator.ports.user_processor import UserProcessor


class Settings:
    def __init__(self):
        self.llm_model = LLM.GEMINI


def get_llm_model() -> LLMInterface:
    settings = Settings()
    if settings.llm_model == LLM.LMSTUDIO:
        return LMStudioAdapter(llm_model=settings.llm_model.value)
    if settings.llm_model == LLM.GEMINI:
        return GeminiAdapter(llm_model=settings.llm_model.value)
    raise ValueError(f"Unsupported LLM model: {settings.llm_model.value}")


def get_job_context_generator(job_description: str) -> JobContextGenerator:
    return JobContextGeneratorImpl(job_description=job_description)


def get_user_processor() -> UserProcessor:
    return JsonUserProcessor(data_dir=DATA_DIR)

