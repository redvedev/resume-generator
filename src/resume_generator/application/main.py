import logging
from pathlib import Path

from dotenv import load_dotenv

from resume_generator.application.offer_processor import OfferProcessor

logger = logging.getLogger(__name__)


def main():
    load_dotenv()
    fm = OfferProcessor()
    fm.process_offers_dir()


if __name__ == "__main__":
    main()
