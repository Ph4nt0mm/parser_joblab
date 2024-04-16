from abc import ABC, abstractmethod

import pandas as pd
from bs4 import BeautifulSoup
from requests.sessions import Session
from selenium.webdriver.chrome.webdriver import WebDriver


class DriverManagerABC(ABC):
    """
    Abstract base class defining the interface for a WebDriver manager.
    """

    @abstractmethod
    def __init__(self, driver_path: str, headless: bool) -> None:
        raise NotImplementedError('Method "__init__" not implemented')

    @abstractmethod
    def _init_driver(self) -> WebDriver:
        raise NotImplementedError('Method "_init_driver" not implemented')

    @abstractmethod
    def close_driver(self) -> None:
        raise NotImplementedError('Method "close_driver" not implemented')


class ScraperABC(ABC):
    """
    Abstract base class defining the interface for a web scraper.
    """

    @abstractmethod
    def __init__(self, driver_manager: DriverManagerABC) -> None:
        raise NotImplementedError('Method "__init__" not implemented')

    @abstractmethod
    def scrape(self, start_url: str) -> pd.DataFrame:
        raise NotImplementedError('Method "scrape" not implemented')


class DataExtractorABC(ABC):
    """
    Abstract base class defining the interface for data extraction from HTML content.
    """

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
    """
    Abstract base class defining the interface for navigating through web pages.
    """

    @abstractmethod
    def __init__(self, driver_manager: DriverManagerABC) -> None:
        raise NotImplementedError('Method "__init__" not implemented')

    @abstractmethod
    def navigate_to_url(self, url: str) -> None:
        raise NotImplementedError('Method "navigate_to_url" not implemented')

    @abstractmethod
    def find_next_page(self) -> bool:
        raise NotImplementedError('Method "find_next_page" not implemented')

    @abstractmethod
    def go_back(self) -> None:
        raise NotImplementedError('Method "go_back" not implemented')

    @abstractmethod
    def refresh_page(self) -> None:
        raise NotImplementedError('Method "refresh_page" not implemented')


class LoggerABC(ABC):
    """
    Abstract base class defining the interface for a logging system.
    """

    @abstractmethod
    def __init__(self, name: str, log_file: str) -> None:
        raise NotImplementedError('Constructor "__init__" not implemented')

    @abstractmethod
    def info(self, message: str) -> None:
        raise NotImplementedError('Method "info" not implemented')

    @abstractmethod
    def warning(self, message: str) -> None:
        raise NotImplementedError('Method "warning" not implemented')

    @abstractmethod
    def error(self, message: str) -> None:
        raise NotImplementedError('Method "error" not implemented')


class ConfigManagerABC(ABC):
    """
    Abstract base class defining the interface for managing configuration settings.
    """

    @abstractmethod
    def __init__(self, config_path: str) -> None:
        raise NotImplementedError('Constructor "__init__" not implemented')

    @abstractmethod
    def get_setting(self, key: str) -> any:
        raise NotImplementedError('Method "get_setting" not implemented')

    @abstractmethod
    def update_setting(self, key: str, value: any) -> None:
        raise NotImplementedError('Method "update_setting" not implemented')


class ErrorHandlerABC(ABC):
    """
    Abstract base class defining the interface for handling errors during scraping operations.
    """

    @abstractmethod
    def __init__(self, logger: LoggerABC) -> None:
        raise NotImplementedError('Constructor "__init__" not implemented')

    @abstractmethod
    def handle(self, error: Exception, message: str) -> None:
        raise NotImplementedError('Method "handle" not implemented')

    @abstractmethod
    def log_error(self, message: str) -> None:
        raise NotImplementedError('Method "log_error" not implemented')

    @abstractmethod
    def retry_operation(self, function, *args, **kwargs) -> any:
        raise NotImplementedError('Method "retry_operation" not implemented')


class SessionManagerABC(ABC):
    """
    Abstract base class defining the interface for managing session data such as cookies and headers.
    """

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError('Constructor "__init__" not implemented')

    @abstractmethod
    def add_cookie(self, cookie_dict: dict) -> None:
        raise NotImplementedError('Method "add_cookie" not implemented')

    @abstractmethod
    def update_headers(self, headers: dict) -> None:
        raise NotImplementedError('Method "update_headers" not implemented')

    @abstractmethod
    def get_session(self) -> Session:
        raise NotImplementedError('Method "get_session" not implemented')


class DataProcessorABC(ABC):
    """
    Abstract base class defining the interface for processing and transforming data collected during scraping.
    """

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError('Constructor "__init__" not implemented')

    @abstractmethod
    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError('Method "clean_data" not implemented')

    @abstractmethod
    def transform_data(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError('Method "transform_data" not implemented')

    @abstractmethod
    def merge_data(self, data_list: list) -> pd.DataFrame:
        raise NotImplementedError('Method "merge_data" not implemented')
