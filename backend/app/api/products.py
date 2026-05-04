from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.database import get_db
from app.models import User, Product
from app.schemas import ProductCreate, ProductRead, ProductUpdate
from app.dependencies import get_current_user
from app.tasks.parsing import parse_product_now  # Celery задача
from typing import List

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductRead])
async def list_products(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Product).where(Product.user_id == current_user.id, Product.is_active == True))
    return result.scalars().all()

@router.post("/", response_model=ProductRead)
async def create_product(
    prod_data: ProductCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_product = Product(user_id=current_user.id, **prod_data.dict())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    # Один раз пройти парсинг при создании (опционально)
    background_tasks.add_task(parse_product_now.delay, new_product.id)
    return new_product

@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Product).where(Product.id == product_id, Product.user_id == current_user.id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(404, "Product not found")
    return product

@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    update_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Product).where(Product.id == product_id, Product.user_id == current_user.id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(404, "Product not found")
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(product, field, value)
    await db.commit()
    await db.refresh(product)
    return product

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Product).where(Product.id == product_id, Product.user_id == current_user.id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(404, "Product not found")
    await db.delete(product)
    await db.commit()
    return {"ok": True}