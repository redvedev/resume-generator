import logging

from dotenv import load_dotenv
from selenium import webdriver

from searching_offers.application.port_selector import (
    _webdriver,
    job_service,
    offer_processor,
)
from searching_offers.domains.search_query import LinkedinSearchQuery

logger = logging.getLogger(__name__)


def setup_logging():
    logging.basicConfig(
        filename="log_file_name.log",
        level=logging.INFO,
        format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # set a format which is simpler for console use
    formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger("").addHandler(console)


def main():
    load_dotenv()
    setup_logging()
    driver = _webdriver()
    js = job_service(driver)
    of = offer_processor(driver)
    js.login()

    search_query = LinkedinSearchQuery(
        keywords=[
            "Data Analyst",
        ],
        geoId="103855053",
        distance=5,
    )
    offers = js.get_offers(search_query)
    print(f"Found {len(offers)} offers")
    offers = [of.process_offer_from_url(url) for url in offers]
    print(offers[0])


if __name__ == "__main__":
    main()
