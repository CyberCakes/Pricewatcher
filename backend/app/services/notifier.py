import asyncio
from aiogram import Bot
from app.config import settings
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN) if settings.TELEGRAM_BOT_TOKEN else None

async def send_telegram_alert(user_id: int, product_name: str, new_price: float, old_price: float, db: AsyncSession):
    if not bot:
        return
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user or not user.telegram_chat_id:
        return
    drop_percent = (old_price - new_price) / old_price * 100
    message = (
        f"🔔 Цена на товар *{product_name}* снизилась!\n"
        f"Было: {old_price:.2f} руб.\n"
        f"Стало: {new_price:.2f} руб.\n"
        f"Снижение: {drop_percent:.1f}%"
    )
    try:
        await bot.send_message(chat_id=user.telegram_chat_id, text=message, parse_mode="Markdown")
    except Exception as e:
        print(f"Telegram send error: {e}")