import json
import logging
from abc import ABC, abstractmethod

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver


class DriverManagerABC(ABC):
    def __init__(self, driver_path: str, headless: bool = True) -> None:
        self.driver_path = driver_path
        self.headless = headless
        self.driver = self._init_driver()

    @abstractmethod
    def _init_driver(self) -> WebDriver:
        raise NotImplementedError('Method "_init_driver" not implemented')

    def close_driver(self) -> None:
        self.driver.quit()


class ScraperABC(ABC):
    def __init__(self, driver_manager: DriverManagerABC) -> None:
        self.driver_manager = driver_manager

    @abstractmethod
    def scrape(self, start_url: str) -> pd.DataFrame:
        raise NotImplementedError('Method "scrape" not implemented')


class DataExtractorABC(ABC):
    @staticmethod
    @abstractmethod
    def extract_text(soup: BeautifulSoup, selector: str) -> str:
        raise NotImplementedError('Method "extract_text" not implemented')

    @staticmethod
    @abstractmethod
    def extract_attribute(soup: BeautifulSoup, selector: str, attribute: str) -> str:
        raise NotImplementedError('Method "extract_attribute" not implemented')

    @staticmethod
    @abstractmethod
    def extract_links(soup: BeautifulSoup, selector: str) -> list:
        raise NotImplementedError('Method "extract_links" not implemented')


class LinkNavigatorABC(ABC):
    def __init__(self, driver_manager: DriverManagerABC) -> None:
        self.driver_manager = driver_manager

    def navigate_to_url(self, url: str) -> None:
        self.driver_manager.driver.get(url)

    @abstractmethod
    def find_next_page(self) -> bool:
        raise NotImplementedError('Method "find_next_page" not implemented')

    def go_back(self) -> None:
        self.driver_manager.driver.back()

    def refresh_page(self) -> None:
        self.driver_manager.driver.refresh()


class DataProcessorABC(ABC):
    def __init__(self) -> None:
        return

    @abstractmethod
    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError('Method "clean_data" not implemented')

    @abstractmethod
    def transform_data(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError('Method "transform_data" not implemented')

    @abstractmethod
    def merge_data(self, data_list: list) -> pd.DataFrame:
        raise NotImplementedError('Method "merge_data" not implemented')
