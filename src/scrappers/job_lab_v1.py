import logging
import time
from typing import List, Dict

import pandas as pd
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


class JobLabScraper:
    BASE_URL = 'https://joblab.ru'

    def __init__(self):
        self.__driver = self.__init_driver()

    @staticmethod
    def __init_driver() -> WebDriver:
        try:
            _options: Options = Options()
            _options.add_argument(argument='--headless')
            _options.add_argument(argument='--disable-gpu')
            driver: WebDriver = uc.Chrome(options=_options)
            logging.info(msg='Chrome driver started in headless mode')
            return driver
        except WebDriverException as e:
            logging.error(msg=f'Failed to initialize driver: {e}')
            raise

    def scrape(self, path: str = '/resume') -> pd.DataFrame:
        _links = self.__scrape_resume_links(f'{self.BASE_URL}{path}')
        data = self.__collect_data(_links)
        return data

    def __scrape_resume_links(self, start_url: str) -> List[str]:
        self.__driver.get(start_url)
        links: List[str] = []
        while self.__has_next_page():
            links.extend(self.__extract_links())
            self.__go_to_next_page()
            time.sleep(2)
        return links

    def __extract_links(self) -> List[str]:
        _soup = BeautifulSoup(self.__driver.page_source, 'html.parser')
        return [a['href'] for a in _soup.select('a.resume_link')]

    def __has_next_page(self) -> bool:
        try:
            self.__driver.find_element(By.LINK_TEXT, 'Следующая')
            return True
        except NoSuchElementException:
            logging.info(msg='No next page button found.')
            return False

    def __go_to_next_page(self) -> None:
        try:
            _next_button = self.__driver.find_element(By.LINK_TEXT, 'Следующая')
            _next_button.click()
        except NoSuchElementException:
            logging.info(msg='Cannot navigate to next page, next button not found.')

    def __collect_data(self, links: List[str]) -> pd.DataFrame:
        _resumes = [
            self.__scrape_resume_page(resume_url=f'{self.BASE_URL}{link}')
            for link in links
        ]
        return pd.DataFrame(_resumes)

    def __scrape_resume_page(self, resume_url: str) -> Dict[str, any]:
        self.__driver.get(resume_url)
        soup = BeautifulSoup(self.__driver.page_source, 'html.parser')
        resume_data: Dict[str, any] = {
            'title': soup.find('h1').text.strip(),
            'name': self._extract_text(soup, 'Имя'),
            'contact': self._extract_text(soup, 'Контакты'),
            'photo_url': self._extract_photo_url(soup),
            'general_info': self._extract_text(soup, 'Общая информация'),
            'experience': self._extract_experience(soup),
            'education': self._extract_education(soup),
            'additional_info': self._extract_text(soup, 'Дополнительная информация'),
        }
        return resume_data

    @staticmethod
    def _extract_text(soup: BeautifulSoup, section_title: str) -> str:
        section = soup.find('p', text=section_title)
        return section.find_next('div').text.strip() if section else 'Not Available'

    @staticmethod
    def _extract_photo_url(soup: BeautifulSoup) -> str:
        style = soup.find('div', class_='resume_img')['style']
        return style.split('url(')[1].split(')')[0].strip() if style else 'No Image'

    @staticmethod
    def _extract_experience(soup: BeautifulSoup) -> List[str]:
        return [div.text.strip() for div in soup.find_all('div', class_='experience')]

    @staticmethod
    def _extract_education(soup: BeautifulSoup) -> List[str]:
        return [div.text.strip() for div in soup.find_all('div', class_='education')]


if __name__ == '__main__':
    try:
        scraper: JobLabScraper = JobLabScraper()
        _data = scraper.scrape()
        print(_data.head())

    except Exception as e:
        logging.error(msg=f'Failed during scraping process: {e}')
