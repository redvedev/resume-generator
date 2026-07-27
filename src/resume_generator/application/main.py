from dotenv import load_dotenv

import resume_generator.application.port_selector as settings

# from resume_generator.application.compile import main as compile_all
# from resume_generator.application.offer_processor import process_offers


def main():
    load_dotenv()

    user_processor = settings.get_user_processor()
    user = user_processor.read_user()

    offer = "test offer text"
    job_context = settings.get_job_context_generator(offer, user)
    prompt = job_context.get_llm_prompt_work(user)
    print(prompt)
    # llm = settings.get_llm_model()
    # response = llm.generate_response("What is 2+2?")


if __name__ == "__main__":
    main()
