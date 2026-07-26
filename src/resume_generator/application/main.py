import src.application.port_selector as settings
from src.application.offer_processor import process_offers
from dotenv import load_dotenv
from src.application.compile import main as compile_all
def main():
    load_dotenv()

    user_processor = settings.get_user_processor()
    llm = settings.get_llm_model()
    process_offers(llm, user_processor)
    compile_all()

if __name__ == "__main__":
    main()