import json
import logging
from abc import ABC, abstractmethod

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver


class Logger:
    def __init__(self, name: str, log_file: str) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)


class ConfigManager:
    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self.settings = self._load_config()

    def _load_config(self) -> dict:
        with open(self.config_path, 'r') as config_file:
            return json.load(config_file)

    def get_setting(self, key: str) -> any:
        return self.settings.get(key, None)

    def update_setting(self, key: str, value: any) -> None:
        self.settings[key] = value
        with open(self.config_path, 'w') as config_file:
            json.dump(self.settings, config_file, indent=4)


class ErrorHandler:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def handle(self, error: Exception, message: str) -> None:
        self.log_error(f'{message} | Exception: {error}')

    def log_error(self, message: str) -> None:
        self.logger.error(message)

    def retry_operation(self, function, *args, **kwargs) -> any:
        attempts = 3
        for attempt in range(attempts):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                self.log_error(f'Retry {attempt + 1}/{attempts} failed: {e}')
                if attempt == attempts - 1:
                    raise e
