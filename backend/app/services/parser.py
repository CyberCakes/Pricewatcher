import re
from decimal import Decimal
from typing import Optional
import httpx
from bs4 import BeautifulSoup
from app.config import settings
from app.models import SiteSelector
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def extract_price_from_url(url: str, db: AsyncSession, custom_selector: Optional[str] = None) -> Optional[
	Decimal]:
	"""
	Получает HTML страницы, ищет цену по селектору (сперва кастомный, потом автоматом по домену)
	"""
	# Определяем домен
	domain_match = re.search(r'https?://([^/]+)', url)
	if not domain_match:
		return None
	domain = domain_match.group(1)

	# Ищем подходящий селектор в БД
	selector = custom_selector
	if not selector:
		# Ищем по доменному паттерну
		result = await db.execute(select(SiteSelector).where(url
		~ SiteSelector.domain_pattern))
		site_selector = result.scalar_one_or_none()
		if site_selector:
			selector = site_selector.price_selector

	if not selector:
		# Нет селектора — парсинг невозможен
		return None

	async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as client:
		response = await client.get(url, headers={"User-Agent": settings.USER_AGENT})
		if response.status_code != 200:
			return None
		soup = BeautifulSoup(response.text, 'lxml')
		price_element = soup.select_one(selector)
		if not price_element:
			return None
		price_text = price_element.get_text(strip=True)
		# Извлечение числа из текста (поддерживает запятые, пробелы)
		price_match = re.search(r'(\d+[.,]?\d*)', price_text.replace(' ', ''))
		if not price_match:
			return None
		price_str = price_match.group(1).replace(',', '.')
		return Decimal(price_str)
