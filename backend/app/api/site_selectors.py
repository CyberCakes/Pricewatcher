from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import SiteSelector, User
from app.schemas import SiteSelectorCreate, SiteSelectorRead
from app.dependencies import get_current_user, get_current_active_superuser

router = APIRouter(prefix="/site-selectors", tags=["site_selectors"])

@router.get("/", response_model=list[SiteSelectorRead])
async def list_selectors(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Доступно всем залогиненным (только чтение)
    result = await db.execute(select(SiteSelector))
    return result.scalars().all()

@router.post("/", response_model=SiteSelectorRead)
async def create_selector(
    selector_data: SiteSelectorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)  # только суперпользователь
):
    new_selector = SiteSelector(**selector_data.dict())
    db.add(new_selector)
    await db.commit()
    await db.refresh(new_selector)
    return new_selector