import json
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


pd.set_option('display.max_columns', None)


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
        logging.info(msg='Scrapping links')
        self.__driver.get(start_url)
        links: List[str] = []
        page_number = 1
        while self.__has_next_page():
            parsed_links = self.__extract_links()
            print(f'Page {page_number} parsed. Links: {parsed_links}')
            links.extend(parsed_links)
            self.__go_to_next_page()
            time.sleep(2)
            page_number += 1
            if page_number == 2:
                return links

        return links

    def __extract_links(self) -> List[str]:
        _soup = BeautifulSoup(self.__driver.page_source, 'html.parser')
        return [a['href'] for a in _soup.select('p.prof a')]

    def __has_next_page(self) -> bool:
        try:
            self.__driver.find_element(By.LINK_TEXT, 'Следующая →')
            return True
        except NoSuchElementException:
            logging.info(msg='No next page button found.')
            return False

    def __go_to_next_page(self) -> None:
        try:
            _next_button = self.__driver.find_element(By.LINK_TEXT, 'Следующая →')
            _next_button.click()
        except NoSuchElementException:
            logging.info(msg='Cannot navigate to next page, next button not found.')

    def __collect_data(self, links: List[str]) -> pd.DataFrame:
        logging.info(msg='Starting collecting data')
        _resumes = [self.__scrape_resume_page(resume_url=f'{self.BASE_URL}{link}') for link in links]
        return pd.DataFrame(_resumes)

    def __scrape_resume_page(self, resume_url: str) -> Dict[str, any]:
        print(resume_url)
        self.__driver.get(resume_url)
        soup = BeautifulSoup(self.__driver.page_source, 'html.parser')
        resume_data: Dict[str, any] = {
            'title': soup.find('h1').text.strip(),
            'name': self._extract_text(soup, 'Имя'),
            'contact': self._extract_text(soup, 'Контакты'),
            'photo_url': self._extract_photo_url(soup),
            'general_info': self._extract_text(soup, 'Общая информация'),
            'Accommodation': self._extract_text(soup, 'Проживание'),
            'wage': self._extract_text(soup, 'Заработная плата'),
            'schedule': self._extract_text(soup, 'График работы'),
            'education': self._extract_text(soup, 'Образование'),
            'experience': self._extract_text(soup, 'Опыт работы'),
            'citizenship': self._extract_text(soup, 'Гражданство'),
            'floor': self._extract_text(soup, 'Пол'),
            'age': self._extract_text(soup, 'Возраст'),
            'experience detailed': self._extract_experience(soup),
            'education detailed': self._extract_education(soup),
            'additional_info': self._extract_additional_info(soup)
        }
        return resume_data

    @staticmethod
    def _extract_text(soup: BeautifulSoup, section_title: str) -> str:
        section = soup.find('p', string=section_title)
        if section:
            section = soup.find('p', string=section_title).parent
            second_parent = section.parent
            print(second_parent.find_all(recursive=False)[1].text.strip())
            result = section.find_next('div').text.strip() if section else 'Not Available'
            return result
        else:
            return 'Not Available'

    @staticmethod
    def _extract_photo_url(soup: BeautifulSoup) -> str:
        img_div = soup.find('div', class_='resume_img')
        # print(img_div)
        if img_div:
            style = img_div['style']
            result = style.split('url(')[1].split(')')[0].strip() if style else 'No Image'
            print(result)
            return result
        else:
            print('No Image')
            return 'No Image'

    @staticmethod
    def _extract_experience(soup: BeautifulSoup) -> List[str]:
        return [div.text.strip() for div in soup.find_all('div', class_='experience')]

    @staticmethod
    def _extract_education(soup: BeautifulSoup) -> List[str]:
        return [div.text.strip() for div in soup.find_all('div', class_='education')]

    @staticmethod
    def _extract_additional_info(soup: BeautifulSoup) -> Dict[str, Dict[str, str]]:
        h2 = soup.find('h2', string='Дополнительная информация')

        # Initialize the result dictionary
        info_dict = {'Дополнительная информация': {}}

        # Once the <h2> is found, navigate to the next <tr> siblings and parse the data
        if h2:
            for sibling in h2.find_parent('tr').find_next_siblings('tr'):
                # Assuming each <tr> has exactly two <td>: one for the term and one for its description
                cells = sibling.find_all('td')
                if len(cells) == 2:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    info_dict['Дополнительная информация'][key] = value
        print(info_dict)
        return info_dict


if __name__ == '__main__':
    try:
        scraper: JobLabScraper = JobLabScraper()
        _data = scraper.scrape()
        print(_data.head())

    except Exception as e:
        logging.error(msg=f'Failed during scraping process: {e}')
