from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from searching_offers.adapters.linkedin_job_service import LinkedinJobService
from searching_offers.ports.job_service_connector import JobServiceConnector


def _webdriver() -> WebDriver:
    return webdriver.Firefox()


def job_service(driver: WebDriver) -> JobServiceConnector:
    return LinkedinJobService(driver)
