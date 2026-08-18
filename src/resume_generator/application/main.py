import logging
from pathlib import Path
from shutil import copy

from dotenv import load_dotenv

import resume_generator.application.port_selector as settings
from resume_generator.application.agent_invoker import AgentInvoker
from resume_generator.application.config import OFFER_DIR, OUTPUT_DIR, TEMPLATE_DIR
from resume_generator.application.latex_builder import LatexGenerator
from resume_generator.application.prompt_generator import PromptGenerator
from resume_generator.domains.user import User

logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
logger = logging.getLogger()


class FileManager:
    def __init__(self) -> None:
        self.prompt_generator = PromptGenerator()
        self.agent = AgentInvoker(self.prompt_generator)
        self.latex_builder = LatexGenerator()
        self.offers = OFFER_DIR
        self.target_folder = OUTPUT_DIR
        self.MINIMUM_FIT_SCORE = 8

    def process_offer(
        self,
        offer_source: Path,
        processed_offer_target: Path,
    ) -> None:
        job_description = offer_source.read_text(encoding="utf-8")
        user_fit = self.agent.get_user_fit(job_description)
        if user_fit < self.MINIMUM_FIT_SCORE:
            logger.info("User fit score below threshold")
            return
        user = self.agent.prepare_user_model(job_description)
        latex = self.latex_builder.generate_tex(user)
        notes = self.agent.prepare_job_notes(job_description, user)

        processed_offer_target.mkdir(parents=True, exist_ok=True)
        offer_copy_file = processed_offer_target / "offer.txt"
        resume_file = processed_offer_target / "resume.tex"
        notes_file = processed_offer_target / "notes.md"
        resume_source = TEMPLATE_DIR / "resume.cls"
        resume_target = processed_offer_target / "resume.cls"

        offer_copy_file.write_text(encoding="utf-8", data=job_description)
        resume_file.write_text(encoding="utf-8", data=latex)
        notes_file.write_text(encoding="utf-8", data=notes)
        copy(resume_source, resume_target)

    def process_offers_dir(self) -> None:
        for file in self.offers.rglob("*.txt"):
            offer_name = file.stem
            output_dir = self.target_folder / offer_name
            self.process_offer(file, output_dir)


def main():
    logger.info("Application started. Loading environment variables")
    load_dotenv()

    logger.info("Trying to read user data")
    fm = FileManager()
    fm.process_offers_dir()


if __name__ == "__main__":
    main()
