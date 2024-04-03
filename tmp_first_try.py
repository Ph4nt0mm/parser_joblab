from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium_stealth import stealth
from typing import List


class WebScraper:
    def __init__(self) -> None:
        self.url: str = 'https://joblab.ru/resume'
        self.driver = self.__setup_driver()

    def __setup_driver(self) -> uc.Chrome:
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options)
        self.__apply_stealth(driver)
        return driver

    def __apply_stealth(self, driver: uc.Chrome) -> None:
        stealth(driver,
                languages=['en-US', 'en'],
                vendor='Google Inc.',
                platform='Win32',
                webgl_vendor='Intel Inc.',
                renderer='Intel Iris OpenGL Engine',
                fix_hairline=True)

    def fetch_page_source(self) -> str:
        self.driver.get(self.url)
        return self.driver.page_source

    def parse_content(self, html: str) -> List[str]:
        soup = BeautifulSoup(html, 'html.parser')
        return [element.text for element in soup.find_all('p')]

    def close(self) -> None:
        self.driver.quit()


if __name__ == '__main__':
    scraper = WebScraper()
    page_source = scraper.fetch_page_source()
    content = scraper.parse_content(page_source)
    print(content)
    scraper.close()
