import logging
import sys

from dotenv import load_dotenv

import resume_generator.application.port_selector as settings
from resume_generator.application.agent_invoker import AgentInvoker
from resume_generator.application.latex_builder import LatexGenerator
from resume_generator.application.prompt_generator import PromptGenerator

logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
logger = logging.getLogger()


def main():
    logging.info("Application started. Loading environment variables")
    load_dotenv()

    user_reader = settings.user_reader()
    logging.info("Trying to read user data")
    user = user_reader.read_user()

    offer = "We are looking for data analytics in R"
    logging.info(f"Processing offer: {offer}")
    # TODO: Add filtering user skills to the offer according to the text, and make a new user you will send here

    prompt_generator = PromptGenerator(offer)
    agent = AgentInvoker(prompt_generator)
    latex_builder = LatexGenerator(agent)
    latex = latex_builder.generate_tex(user)


if __name__ == "__main__":
    main()
