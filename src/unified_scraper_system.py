from src.scrappers.job_lab_v2 import JobLabDriverManager, JobLabScraper, JobLabDataProcessor
from src.support_modules.api_menager import APIManager
from src.support_modules.monitoring_manager import MonitoringManager
from src.support_modules.performance_optimizer import PerformanceOptimizer


class UnifiedScraper:
    """
    Orchestrates the scraping process, leveraging various system components for optimized operations.
    """

    def __init__(self, base_url: str, driver_path: str):
        """
        Initializes all components necessary for the scraping operations.

        Args:
            base_url (str): Base URL for API interactions.
            driver_path (str): Path to the WebDriver executable.
        """
        self.api_manager = APIManager(base_url)
        self.monitoring_manager = MonitoringManager(self.api_manager)
        self.driver_manager = JobLabDriverManager(driver_path=driver_path, headless=True)
        self.scraper = JobLabScraper(self.driver_manager)
        self.data_processor = JobLabDataProcessor()
        self.performance_optimizer = PerformanceOptimizer(self.monitoring_manager)

    def start_scraping(self, start_url: str) -> None:
        """
        Starts the scraping process and handles all associated tasks.

        Args:
            start_url (str): The starting URL for the scraping process.
        """
        try:
            # Monitor and optimize performance before starting the scrape
            self.performance_optimizer.adjust_concurrency(target_concurrency=5)
            self.performance_optimizer.throttle_requests(rate_limit=1.0)

            # Start scraping
            data = self.scraper.scrape(start_url)
            clean_data = self.data_processor.clean_data(data)
            self.monitoring_manager.record_metric('data_rows_collected', float(len(clean_data)))

            # Further processing and storage operations can be added here
        except Exception as e:
            self.monitoring_manager.alert(f"Scraping failed: {str(e)}")
            raise

    def shutdown(self) -> None:
        """
        Shuts down all system components cleanly.
        """
        self.driver_manager.close_driver()
