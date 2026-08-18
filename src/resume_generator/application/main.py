import json
import logging
from contextlib import contextmanager
from pathlib import Path
from shutil import copy

from dotenv import load_dotenv

from resume_generator.application.agent_invoker import AgentInvoker
from resume_generator.application.config import OFFER_DIR, OUTPUT_DIR, TEMPLATE_DIR
from resume_generator.application.latex_builder import LatexGenerator
from resume_generator.application.prompt_generator import PromptGenerator
from resume_generator.domains.user import User

logger = logging.getLogger(__name__)


def configure_logging() -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    )

    root_logger.addHandler(stream_handler)


@contextmanager
def offer_file_logger(log_file: Path):
    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    )
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    try:
        yield
    finally:
        root_logger.removeHandler(file_handler)
        file_handler.close()

    root_logger.addHandler(file_handler)


class FileManager:
    def __init__(self) -> None:
        self.prompt_generator = PromptGenerator()
        self.agent = AgentInvoker(self.prompt_generator)
        self.latex_builder = LatexGenerator()
        self.offers = OFFER_DIR
        self.target_folder = OUTPUT_DIR
        self.MINIMUM_FIT_SCORE = 8

    def _should_process_offer(self, job_description: str) -> bool:
        logger.info("Running fit check before resume generation")
        user_fit = self.agent.get_user_fit(job_description)
        logger.info("Fit score calculated: %s", user_fit)
        if user_fit < self.MINIMUM_FIT_SCORE:
            logger.info("User fit score below threshold")
            return False
        return True

    def _generate_resume_with_validation(
        self,
        job_description: str,
        user: User,
        requirement_analysis,
    ) -> tuple[str, object]:
        logger.info("Generating initial resume draft")
        validation = self.agent.validate_resume(
            job_description,
            user,
            requirement_analysis,
        )
        latex = self.latex_builder.generate_tex(user)
        logger.info("Initial validation result: %s", validation.valid)
        if validation.valid:
            return latex, validation

        logger.info("Validation failed, retrying resume generation")
        return self._retry_resume_generation(
            job_description=job_description,
            requirement_analysis=requirement_analysis,
            validation=validation,
        )

    def _retry_resume_generation(
        self,
        *,
        job_description: str,
        requirement_analysis,
        validation,
        counter: int = 0,
    ) -> tuple[str, object]:
        logger.info("Retry attempt %s started", counter + 1)
        if counter >= 3:
            raise RuntimeError(
                "Resume validation failed after 3 attempts. Issues: "
                + json.dumps(validation.issues, indent=4)
            )
        feedback = "\n".join(validation.issues)
        retry_user = self.agent.prepare_user_model(
            job_description,
            requirement_analysis=requirement_analysis.model_dump_json(indent=4),
            validation_feedback=feedback,
        )
        retry_validation = self.agent.validate_resume(
            job_description,
            retry_user,
            requirement_analysis
        )

        logger.info("Retry validation result: %s", retry_validation.valid)

        if retry_validation.valid:
            retry_latex = self.latex_builder.generate_tex(retry_user)
            return retry_latex, retry_validation
        return self._retry_resume_generation(
            job_description=job_description,
            requirement_analysis=requirement_analysis,
            validation=retry_validation,
            counter=counter + 1,
        )

    def _write_outputs(
        self,
        processed_offer_target: Path,
        job_description: str,
        latex: str,
        notes: str,
        requirement_analysis,
        validation,
    ) -> None:
        logger.info("Writing generated artifacts to %s", processed_offer_target)
        processed_offer_target.mkdir(parents=True, exist_ok=True)

        offer_copy_file = processed_offer_target / "offer.txt"
        resume_file = processed_offer_target / "resume.tex"
        notes_file = processed_offer_target / "notes.md"
        requirement_analysis_file = processed_offer_target / "requirement_analysis.json"
        validation_file = processed_offer_target / "validation_result.json"
        resume_source = TEMPLATE_DIR / "resume.cls"
        resume_target = processed_offer_target / "resume.cls"

        offer_copy_file.write_text(encoding="utf-8", data=job_description)
        resume_file.write_text(encoding="utf-8", data=latex)
        notes_file.write_text(encoding="utf-8", data=notes)
        requirement_analysis_file.write_text(
            encoding="utf-8",
            data=requirement_analysis.model_dump_json(indent=2),
        )
        validation_file.write_text(
            encoding="utf-8",
            data=validation.model_dump_json(indent=2),
        )
        copy(resume_source, resume_target)

    def process_offer(
        self,
        offer_source: Path,
        processed_offer_target: Path,
    ) -> None:
        log_file = processed_offer_target / "resume_builder.log"
        with offer_file_logger(log_file):
            logger.info("Processing offer: %s", offer_source)
            logger.info("Writing logs to %s", log_file)
            job_description = offer_source.read_text(encoding="utf-8")
            logger.info("Analyzing requirements before user selection")
            requirement_analysis = self.agent.analyze_requirements(job_description)
            logger.info(
                "Requirement analysis completed with %s matches",
                len(requirement_analysis.matches),
            )
            if not self._should_process_offer(job_description):
                return

            logger.info("Preparing user model from confirmed matches")
            user = self.agent.prepare_user_model(
                job_description,
                requirement_analysis=requirement_analysis.model_dump_json(indent=4),
            )
            logger.info("User model prepared")
            latex, validation = self._generate_resume_with_validation(
                job_description,
                user,
                requirement_analysis,
            )
            logger.info("Preparing job notes")
            notes = self.agent.prepare_job_notes(job_description, user)

            self._write_outputs(
                processed_offer_target,
                job_description,
                latex,
                notes,
                requirement_analysis,
                validation,
            )

    def process_offers_dir(self) -> None:
        for file in self.offers.rglob("*.txt"):
            offer_name = file.stem
            output_dir = self.target_folder / offer_name
            self.process_offer(file, output_dir)


def main():
    configure_logging()
    logger.info("Application started. Loading environment variables")
    load_dotenv()

    logger.info("Trying to read user data")
    fm = FileManager()
    logger.info("Starting offer processing")
    fm.process_offers_dir()
    logger.info("Offer processing finished")


if __name__ == "__main__":
    main()
