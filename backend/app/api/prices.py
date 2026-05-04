from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import User, Product, PriceHistory
from app.schemas import PriceHistoryRead, ProductWithPrices
from app.dependencies import get_current_user
from typing import List
from datetime import datetime, timedelta

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/history/{product_id}", response_model=List[PriceHistoryRead])
async def get_price_history(
		product_id: int,
		days: int = 30,
		db: AsyncSession = Depends(get_db),
		current_user: User = Depends(get_current_user)
):
	# Проверка прав
	prod_result = await db.execute(select(Product).where(Product.id == product_id, Product.user_id == current_user.id))
	if not prod_result.scalar_one_or_none():
		raise HTTPException(404, "Product not found")

	since = datetime.utcnow() - timedelta(days=days)
	result = await db.execute(
		select(PriceHistory)
		.where(PriceHistory.product_id == product_id, PriceHistory.timestamp >= since)
		.order_by(PriceHistory.timestamp)
	)
	return result.scalars().all()


@router.get("/product/{product_id}/full", response_model=ProductWithPrices)
async def get_product_with_prices(
		product_id: int,
		days: int = 30,
		db: AsyncSession = Depends(get_db),
		current_user: User = Depends(get_current_user)
):
	prod_result = await db.execute(select(Product).where(Product.id == product_id, Product.user_id == current_user.id))
	product = prod_result.scalar_one_or_none()
	if not product:
		raise HTTPException(404, "Product not found")

	since = datetime.utcnow() - timedelta(days=days)
	prices_result = await db.execute(
		select(PriceHistory)
		.where(PriceHistory.product_id == product_id, PriceHistory.timestamp >= since)
		.order_by(PriceHistory.timestamp)
	)
	product.prices = prices_result.scalars().all()
	return product