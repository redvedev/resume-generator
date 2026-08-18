import logging

from dotenv import load_dotenv
from selenium import webdriver

from searching_offers.application.port_selector import _webdriver, job_service

logger = logging.getLogger(__name__)


def main():
    load_dotenv()
    driver = webdriver.Firefox()
    js = job_service(driver)


if __name__ == "__main__":
    main()
