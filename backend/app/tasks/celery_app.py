from celery import Celery
from app.config import settings

celery_app = Celery(
    "pricewatcher",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.parsing", "app.tasks.notifications"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "parse-all-products": {
            "task": "app.tasks.parsing.parse_all_due_products",
            "schedule": 60.0,  # каждую минуту проверяем, какие товары пора парсить
        },
    }
)