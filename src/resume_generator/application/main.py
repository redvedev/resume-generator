from dotenv import load_dotenv

import resume_generator.application.port_selector as settings
from resume_generator.application.agent_invoker import AgentInvoker
from resume_generator.application.prompt_generator import PromptGenerator


def main():
    load_dotenv()

    user_reader = settings.user_reader()
    user = user_reader.read_user()

    offer = "We are looking for data analytics in R"
    # TODO: Add filtering user skills to the offer according to the text, and make a new user you will send here
    prompt_generator = PromptGenerator(offer)
    agent = AgentInvoker(prompt_generator)


if __name__ == "__main__":
    main()
