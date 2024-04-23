import sys
import time
from pprint import pformat
from typing import List, Dict

import pandas as pd
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from loguru import logger
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from settings.config import settings

logger.remove()
logger.add(sink=sys.stderr,  level=settings.LOGURU_LEVEL)
pd.set_option('display.max_columns', None)


class JobLabDataParser:
    @staticmethod
    def extract_text(soup: BeautifulSoup, section_title: str) -> str:
        section = soup.find('p', string=section_title)
        if section:
            section = soup.find('p', string=section_title).parent
            second_parent = section.parent
            result = second_parent.find_all(recursive=False)[1].text.strip()
            logger.debug(
                f'\nFor field:\t {section_title}\n'
                f'Extracted text:\t{result}'
            )
            return result
        else:
            return 'Not Available'

    @staticmethod
    def extract_photo_url(soup: BeautifulSoup) -> str:
        img_div = soup.find('div', class_='resume_img')
        if img_div:
            style = img_div['style']
            result = style.split('url(')[1].split(')')[0].strip() if style else 'No Image'
            return result
        else:
            return 'No Image'

    @staticmethod
    def extract_detailed_block(soup: BeautifulSoup, block_title: str) -> Dict[str, Dict[str, str]]:
        h2_block = soup.find('h2', string=block_title)

        result_dict = {block_title: {}}

        if h2_block:
            for sibling in h2_block.find_parent('tr').find_next_siblings('tr'):
                if len(sibling.find_all('td')) <= 1:
                    break
                key = sibling.find_all('td')[0].get_text(strip=True)
                value = sibling.find_all('td')[1].get_text(strip=True)
                result_dict[block_title][key] = value
        return result_dict

    @staticmethod
    def extract_block_with_sub_blocks(soup: BeautifulSoup, block_title: str) -> List[Dict[str, Dict[str, str]]]:
        # Find the 'Образование' section
        education_header = soup.find('h2', string=block_title)

        result_data = []
        current_block_data = {}

        if education_header:
            for sibling in education_header.find_parent('tr').find_next_siblings('tr'):
                # Check for stopping conditions
                if len(sibling.find_all('td')) <= 1:
                    if current_block_data:
                        result_data.append(current_block_data)
                        return result_data
                else:
                    key, value = (cell.get_text(strip=True) for cell in sibling.find_all('td'))
                    current_block_data[key] = value

                if sibling.find('hr') is not None:
                    if current_block_data:
                        result_data.append(current_block_data)
                    current_block_data = {}

        if current_block_data:
            result_data.append(current_block_data)
        return result_data


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
            logger.info('Chrome driver started in headless mode')
            return driver
        except WebDriverException as e:
            logger.error(f'Failed to initialize driver: {e}')
            raise

    def scrape(self, path: str = '/resume') -> pd.DataFrame:
        _links = self.__scrape_resume_links(f'{self.BASE_URL}{path}')
        data = self.__collect_data(_links)
        return data

    def __scrape_resume_links(self, start_url: str) -> List[str]:
        logger.info('Scrapping links')
        self.__driver.get(start_url)
        links: List[str] = []
        page_number = 1
        while self.__has_next_page():
            parsed_links = self.__extract_links()
            links.extend(parsed_links)
            logger.info(f'Page {page_number} parsed. Links: {parsed_links}')
            self.__go_to_next_page()

            page_number += 1
            if page_number == 2:
                return links

            time.sleep(2)

        return links

    def __extract_links(self) -> List[str]:
        _soup = BeautifulSoup(self.__driver.page_source, 'html.parser')
        return [a['href'] for a in _soup.select('p.prof a')]

    def __has_next_page(self) -> bool:
        try:
            self.__driver.find_element(By.LINK_TEXT, 'Следующая →')
            return True
        except NoSuchElementException:
            logger.info('No next page button found.')
            return False

    def __go_to_next_page(self) -> None:
        try:
            _next_button = self.__driver.find_element(By.LINK_TEXT, 'Следующая →')
            _next_button.click()
        except NoSuchElementException:
            logger.info('Cannot navigate to next page, next button not found.')

    def __collect_data(self, links: List[str]) -> pd.DataFrame:
        logger.info('Scrapping data from resume pages')
        _resumes = []
        for link in links:
            _resumes.append(self.__scrape_resume_page(resume_url=f'{self.BASE_URL}{link}'))
            time.sleep(2)
        return pd.DataFrame(_resumes)

    def __scrape_resume_page(self, resume_url: str) -> Dict[str, any]:
        self.__driver.get(resume_url)
        soup = BeautifulSoup(self.__driver.page_source, 'html.parser')
        resume_data: Dict[str, any] = {
            'Title': soup.find('h1').text.strip(),
            'Name': JobLabDataParser.extract_text(soup, 'Имя'),
            'Contact': JobLabDataParser.extract_text(soup, 'Контакты'),
            'Photo_url': JobLabDataParser.extract_photo_url(soup),
            'Accommodation': JobLabDataParser.extract_text(soup, 'Проживание'),
            'Wage': JobLabDataParser.extract_text(soup, 'Заработная плата'),
            'Schedule': JobLabDataParser.extract_text(soup, 'График работы'),
            'Education': JobLabDataParser.extract_text(soup, 'Образование'),
            'Experience': JobLabDataParser.extract_text(soup, 'Опыт работы'),
            'Citizenship': JobLabDataParser.extract_text(soup, 'Гражданство'),
            'Gender': JobLabDataParser.extract_text(soup, 'Пол'),
            'Age': JobLabDataParser.extract_text(soup, 'Возраст'),
            'Experience detailed': JobLabDataParser.extract_block_with_sub_blocks(soup, 'Опыт работы'),
            'Education detailed': JobLabDataParser.extract_detailed_block(soup, 'Образование'),
            'Additional info': JobLabDataParser.extract_detailed_block(soup, 'Дополнительная информация')
        }
        logger.debug(
            f'\nScraped data from:\t {resume_url}\n'
            f'{pformat(resume_data)}'
        )
        return resume_data

    def __del__(self):
        try:
            self.__driver.quit()
        except Exception as e:
            logger.error(f"Failed to quit the driver cleanly: {str(e)}")


if __name__ == '__main__':
    try:
        scraper: JobLabScraper = JobLabScraper()
        _data = scraper.scrape()
        logger.info(f'Data scraped: {_data.shape}')

        _data.to_csv('C:\\Users\\f.tropin\\Documents\\work\\ebeyshiy_parser_joblab\\result.csv')
        logger.info('Data saved')

    except Exception as e:
        logger.error(f'Failed during scraping process: {e}')
