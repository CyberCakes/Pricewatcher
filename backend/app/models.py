from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    telegram_chat_id = Column(String, nullable=True)  # для уведомлений
    created_at = Column(DateTime, default=datetime.utcnow)

    products = relationship("Product", back_populates="owner", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    url = Column(String, nullable=False)
    name = Column(String, nullable=True)   # может заполняться после первого парсинга
    price_selector = Column(String, nullable=True)  # пользовательский CSS/XPath (если не автоподбор)
    parse_interval_minutes = Column(Integer, default=1440)  # 1 раз в день
    last_parsed_at = Column(DateTime, nullable=True)
    notify_drop_percent = Column(Integer, default=5)  # уведомлять при снижении на %
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    owner = relationship("User", back_populates="products")
    prices = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")

class PriceHistory(Base):
    __tablename__ = "price_history"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    product = relationship("Product", back_populates="prices")

class SiteSelector(Base):
    __tablename__ = "site_selectors"
    id = Column(Integer, primary_key=True)
    domain_pattern = Column(String, nullable=False, unique=True)  # регулярка для домена
    price_selector = Column(Text, nullable=False)  # CSS селектор цены
    name_selector = Column(Text, nullable=True)   # CSS селектор названия (опционально)