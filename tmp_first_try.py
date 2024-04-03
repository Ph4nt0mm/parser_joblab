from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium_stealth import stealth
from selenium.webdriver.chrome.webdriver import WebDriver
from typing import List


class WebScraper:
    def __init__(self, url: str = 'https://joblab.ru/resume') -> None:
        self._url: str = url
        self._driver: WebDriver = self._setup_driver()

    def _setup_driver(self) -> WebDriver:
        options = uc.ChromeOptions()
        driver: WebDriver = uc.Chrome(options=options)
        self._apply_stealth(driver)
        return driver

    @staticmethod
    def _apply_stealth(driver: WebDriver) -> None:
        stealth(
            driver,
            languages=['en-US', 'en'],
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor='Intel Inc.',
            renderer='Intel Iris OpenGL Engine',
            fix_hairline=True
        )

    def fetch_page_source(self) -> str:
        self._driver.get(self._url)
        return self._driver.page_source

    @classmethod
    def parse_content(cls, html: str) -> List[str]:
        soup = BeautifulSoup(html, 'html.parser')
        return [element.text for element in soup.find_all('p')]

    def close(self) -> None:
        self._driver.quit()


if __name__ == '__main__':
    scraper = WebScraper()
    page_source = scraper.fetch_page_source()
    content = scraper.parse_content(page_source)
    print(content)
    scraper.close()
