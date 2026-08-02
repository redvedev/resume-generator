from dotenv import load_dotenv

import resume_generator.application.port_selector as settings
from resume_generator.application.agent_invoker import AgentInvoker
from resume_generator.application.prompt_generator import PromptGenerator


def main():
    load_dotenv()

    user_reader = settings.user_reader()
    user = user_reader.read_user()

    offer = ""
    prompt_generator = PromptGenerator(offer, user)
    agent = AgentInvoker(prompt_generator)
    print(agent.get_user_education_summary())


if __name__ == "__main__":
    main()
