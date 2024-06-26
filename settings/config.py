from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DEV: bool = True

    LOGURU_LEVEL: str = 'INFO'
    SLEEEP_BETWEEN_REQUESTS: int = 2
    MAX_NUM_PAGES_WITH_LINKS: int = 3
    OUTPUT_PATH: int = 3

    class Config:
        env_file = Path(BASE_DIR, 'settings', 'env')
        load_dotenv(env_file)


settings = Settings()




