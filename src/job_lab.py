from base import abc_classes

import pandas as pd
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


class JobLabDriverManager(abc_classes.DriverManagerABC):
    def __init__(self, driver_path: str, headless: bool = True) -> None:
        super().__init__(driver_path=driver_path, headless=headless)

    def _init_driver(self) -> WebDriver:
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        return uc.Chrome(executable_path=self.driver_path, options=options)


class JobLabScraper(abc_classes.ScraperABC):
    def __init__(self, driver_manager: abc_classes.DriverManagerABC) -> None:
        super().__init__(driver_manager=driver_manager)

    def scrape(self, start_url: str) -> pd.DataFrame:
        self.driver_manager.driver.get(start_url)
        data = []  # Example: Implement specific scraping logic here
        # Example scraping logic goes here.
        return pd.DataFrame(data)


class JobLabDataExtractor(abc_classes.DataExtractorABC):
    @staticmethod
    def extract_text(soup: BeautifulSoup, selector: str) -> str:
        element = soup.select_one(selector)
        return element.text.strip() if element else ''

    @staticmethod
    def extract_attribute(soup: BeautifulSoup, selector: str, attribute: str) -> str:
        element = soup.select_one(selector)
        return element[attribute] if element and attribute in element.attrs else ''

    @staticmethod
    def extract_links(soup: BeautifulSoup, selector: str) -> list:
        elements = soup.select(selector)
        return [element['href'] for element in elements if 'href' in element.attrs]


class JobLabLinkNavigator(abc_classes.LinkNavigatorABC):
    def __init__(self, driver_manager: JobLabDriverManager) -> None:
        super().__init__(driver_manager=driver_manager)

    def find_next_page(self) -> bool:
        try:
            next_button = self.driver_manager.driver.find_element_by_link_text('Next')
            if next_button:
                next_button.click()
                return True
        except Exception:
            return False
        return False


class JobLabDataProcessor(abc_classes.DataProcessorABC):

    def __init__(self) -> None:
        super().__init__()

    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        # Implement specific data cleaning logic here
        return data.dropna()  # Example cleaning operation

    def transform_data(self, data: pd.DataFrame) -> pd.DataFrame:
        # Implement data transformation logic here
        return data  # Example transformation (placeholder)

    def merge_data(self, data_list: list) -> pd.DataFrame:
        return pd.concat(data_list, ignore_index=True)
