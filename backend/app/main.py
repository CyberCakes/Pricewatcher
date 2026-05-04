from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, products, prices, site_selectors
from app.database import engine, Base
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(prices.router, prefix="/api")
app.include_router(site_selectors.router, prefix="/api")

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "PriceWatcher API", "docs": "/docs"}