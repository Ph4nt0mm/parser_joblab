import json
import logging
from time import sleep


class Logger:
    def __init__(self, name: str, log_file: str) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(filename=log_file)
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

    def retry_operation(
        self, function, *args, max_retries=3, backoff_in_seconds=2, **kwargs
    ) -> any:
        """
        Retry operation with exponential backoff.

        Args:
            function: The function to retry.
            max_retries (int): Maximum number of retries.
            backoff_in_seconds (int): Initial backoff interval in seconds.
            args, kwargs: Arguments for the function.
        """
        attempt = 0
        while attempt < max_retries:
            try:
                return function(*args, **kwargs)
            except Exception as e:
                self.log_error(f'Retry {attempt + 1}/{max_retries}  failed: {e}')
                sleep(backoff_in_seconds * (2 ** attempt))
                attempt += 1
        self.log_error(f'All retries failed for function: {function}.')
        return None
