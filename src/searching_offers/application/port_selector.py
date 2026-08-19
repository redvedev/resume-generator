from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from searching_offers.adapters.linkedin.job_service import LinkedinJobService
from searching_offers.adapters.linkedin.offer_processor import LinkedinOfferProcessor
from searching_offers.ports.job_service_connector import JobServiceConnector
from searching_offers.ports.offer_processor import OfferProcessorPort


def _webdriver() -> WebDriver:
    return webdriver.Firefox()


def job_service(driver: WebDriver) -> JobServiceConnector:
    return LinkedinJobService(driver)


def offer_processor(driver: WebDriver) -> OfferProcessorPort:
    return LinkedinOfferProcessor(driver)
