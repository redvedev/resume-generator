from dotenv import load_dotenv

import resume_generator.application.port_selector as settings
from resume_generator.application.compile import main as compile_all
from resume_generator.application.offer_processor import process_offers


def main():
    load_dotenv()

    user_processor = settings.get_user_processor()
    llm = settings.get_llm_model()
    response = llm.generate_response("What is 2+2?")
    print(response)
    # process_offers(llm, user_processor)
    # compile_all()


if __name__ == "__main__":
    main()

