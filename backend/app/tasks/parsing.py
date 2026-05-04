from celery import shared_task
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, update
from app.config import settings
from app.models import Product, PriceHistory, User
from app.services.parser import extract_price_from_url
from app.services.notifier import send_telegram_alert
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@shared_task
async def parse_product_now(product_id: int):
	async with AsyncSessionLocal() as db:
		result = await db.execute(select(Product).where(Product.id == product_id))
		product = result.scalar_one_or_none()
		if not product or not product.is_active:
			return
		price = await extract_price_from_url(product.url, db, product.price_selector)
		if price is None:
			logger.warning(f"Could not parse price for {product.url}")
			return

		# Сохраняем историю
		new_price = PriceHistory(product_id=product.id, price=price, timestamp=datetime.utcnow())
		db.add(new_price)

		# Получаем предыдущую цену (последнюю до текущего момента)
		prev_result = await db.execute(
			select(PriceHistory).where(PriceHistory.product_id == product_id).order_by(
				PriceHistory.timestamp.desc()).limit(1).offset(1)
		)
		prev_price = prev_result.scalar_one_or_none()

		# Проверяем снижение
		if prev_price and prev_price.price > price:
			drop = (prev_price.price - price) / prev_price.price * 100
			if drop >= product.notify_drop_percent:
				await send_telegram_alert(product.user_id, product.name or product.url, price, prev_price.price, db)

		product.last_parsed_at = datetime.utcnow()
		await db.commit()


@shared_task
async def parse_all_due_products():
	async with AsyncSessionLocal() as db:
		now = datetime.utcnow()
		# Ищем товары, которые нужно обновить
		result = await db.execute(
			select(Product).where(Product.is_active == True).where(
				(Product.last_parsed_at == None) |
				(Product.last_parsed_at + timedelta(minutes=Product.parse_interval_minutes) <= now)
			)
		)
		products = result.scalars().all()
		for p in products:
			parse_product_now.delay(p.id)
	logger.info(f"Scheduled parsing for {len(products)} products")