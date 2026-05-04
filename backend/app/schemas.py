from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    telegram_chat_id: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    url: HttpUrl
    name: Optional[str] = None
    price_selector: Optional[str] = None
    parse_interval_minutes: int = 1440
    notify_drop_percent: int = 5

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price_selector: Optional[str] = None
    parse_interval_minutes: Optional[int] = None
    notify_drop_percent: Optional[int] = None
    is_active: Optional[bool] = None

class ProductRead(ProductBase):
    id: int
    user_id: int
    last_parsed_at: Optional[datetime] = None
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class PriceHistoryRead(BaseModel):
    id: int
    product_id: int
    price: Decimal
    timestamp: datetime

    class Config:
        from_attributes = True

class ProductWithPrices(ProductRead):
    prices: List[PriceHistoryRead] = []

class SiteSelectorBase(BaseModel):
    domain_pattern: str
    price_selector: str
    name_selector: Optional[str] = None

class SiteSelectorCreate(SiteSelectorBase):
    pass

class SiteSelectorRead(SiteSelectorBase):
    id: int

    class Config:
        from_attributes = True