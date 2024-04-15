import time
from typing import List
import undetected_chromedriver as uc
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from bs4 import BeautifulSoup
import pandas as pd
import logging


class JoblabScraper:
    def __init__(self, base_url: str = 'https://joblab.ru'):
        self.base_url = base_url
        self.driver = self.__init_driver()

    @staticmethod
    def __init_driver() -> WebDriver:
        try:
            options = uc.ChromeOptions()
            options.add_argument('--headless')
            driver = uc.Chrome(options=options)
            logging.info('Chrome driver started in headless mode')
            return driver
        except WebDriverException as e:
            logging.error(f'Failed to initialize driver: {e}')
            raise

    def scrape_resume_links(self, start_url: str) -> List[str]:
        self.driver.get(start_url)
        links = []
        while True:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            page_links = [a['href'] for a in soup.select('a.resume_link')]
            links.extend(page_links)
            next_button = self.driver.find_element(By.LINK_TEXT, 'Следующая')
            if 'disabled' in next_button.get_attribute('class'):
                break
            next_button.click()
        return links

    def scrape_resume_page(self, resume_url: str) -> dict:
        self.driver.get(resume_url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        resume_data = {
            'title': soup.find('h1').text,
            'name': soup.find('div', class_='name').text,
            'contact': soup.find('div', class_='contact').text,
            'photo_url': soup.find('img')['src'],
            'general_info': soup.find('section', id='general_info').text,
            'experience': [div.text for div in soup.find_all('div', class_='experience')],
            'education': [div.text for div in soup.find_all('div', class_='education')],
            'additional_info': soup.find('section', id='additional_info').text
        }
        return resume_data

    def collect_data(self, links: List[str]) -> pd.DataFrame:
        resumes = [self.scrape_resume_page(url) for url in links]
        return pd.DataFrame(resumes)

    def set_search_parameters(
        self,
        keywords: str = None,
        sort: str = None,
        salary_max: int = None,
        region: str = None,
        city: str = None,
        metro: str = None,
        category: str = None,
        work_schedule: str = None,
        education: str = None,
        experience: str = None,
        gender: str = None,
        exclude_params: List[str] = None
    ) -> None:
        """ Set search parameters on the resume search page """
        self.driver.get(f'{self.base_url}/resume')
        if keywords:
            self.driver.find_element(By.NAME, 'Keywords').send_keys(keywords)
        if sort:
            self._select_dropdown_option('Sort', sort)
        if salary_max:
            self.driver.find_element(By.NAME, 'SalaryMax').send_keys(salary_max)
        if region:
            self._select_dropdown_option('Region', region)
        if city:
            self._select_dropdown_option('City', city)
        if metro:
            self._select_dropdown_option('Metro', metro)
        if category:
            self._select_dropdown_option('Category', category)
        if work_schedule:
            self._select_dropdown_option('WorkSchedule', work_schedule)
        if education:
            self._select_dropdown_option('Education', education)
        if experience:
            self._select_dropdown_option('Experience', experience)
        if gender:
            self._select_dropdown_option('Gender', gender)
        if exclude_params:
            for param in exclude_params:
                checkbox = self.driver.find_element(By.ID, f'exclude{param}')
                if not checkbox.is_selected():
                    checkbox.click()
        self.driver.find_element(By.ID, 'search_button').click()

    def _select_dropdown_option(self, dropdown_id: str, value: str) -> None:
        """ Helper method to select an option from a dropdown menu """
        dropdown = self.driver.find_element(By.ID, dropdown_id)
        for option in dropdown.find_elements(By.TAG_NAME, 'option'):
            if option.text == value:
                option.click()
                break

    def run(self, search_url: str, search_params: dict = None) -> pd.DataFrame:
        """ Main method to initiate scraping process """
        if search_params:
            self.set_search_parameters(**search_params)
        else:
            self.driver.get(search_url)
        time.sleep(2)  # Add delay to ensure the page loads completely
        links = self.scrape_resume_links(search_url)
        data = self.collect_data(links)
        return data

    def __del__(self):
        self.driver.quit()


if __name__ == '__main__':
    # Example usage:
    scraper = JoblabScraper()
    params = {
        'keywords': 'Python developer',
        'region': 'Moscow',
        'salary_max': 200000
    }
    data = scraper.run('https://joblab.ru/resume', search_params=params)
    print(data)
