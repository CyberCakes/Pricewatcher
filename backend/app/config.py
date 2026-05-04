from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
	PROJECT_NAME: str = "PriceWatcher"
	DATABASE_URL: str = "postgresql+asyncpg://user:pass@db:5432/pricewatcher"
	SECRET_KEY: str = "change_me_in_production"
	REDIS_URL: str = "redis://redis:6379/0"
	TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

	ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
	REFRESH_TOKEN_EXPIRE_DAYS: int = 7

	# Парсинг: таймауты, user-agent
	HTTP_TIMEOUT: int = 15
	USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

	class Config:
		env_file = ".env"


settings = Settings()