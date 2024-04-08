import undetected_chromedriver as uc
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium_stealth import stealth


class BaseWebScraper:
    def __init__(self) -> None:
        self._driver: WebDriver = self._setup_driver()

    def __enter__(self) -> 'BaseWebScraper':
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def _setup_driver(self) -> WebDriver:
        options: uc.ChromeOptions = uc.ChromeOptions()
        driver: WebDriver = uc.Chrome(options=options)
        self._apply_stealth(driver=driver)
        return driver

    @staticmethod
    def _apply_stealth(driver: WebDriver) -> None:
        stealth(
            driver=driver,
            languages=['en-US', 'en'],
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor='Intel Inc.',
            renderer='Intel Iris OpenGL Engine',
            fix_hairline=True
        )

    def close(self) -> None:
        if self._driver:
            self._driver.quit()
