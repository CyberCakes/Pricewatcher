# PriceWatcher — умный трекер цен конкурентов

**PriceWatcher** — это веб-приложение для мониторинга цен на товары с любых сайтов (Ozon, Wildberries, Яндекс.Маркет, любые интернет-магазины). Пользователь добавляет ссылку на товар, сервис периодически парсит цену, строит график изменений и отправляет Telegram-уведомления при снижении цены.

Проект демонстрирует навыки **Data Engineering**, **асинхронного парсинга**, **очередей задач**, **визуализации данных** и **full-stack разработки**.

---

## 🚀 Основные возможности

- ✅ **Добавление товаров** – по URL, с возможностью указать CSS-селектор цены вручную или использовать автоматический по домену.
- ✅ **Автоматический парсинг** – фоновые задачи Celery проверяют цены с заданной периодичностью (от часа до нескольких дней).
- ✅ **История цен** – все изменения сохраняются в PostgreSQL, можно посмотреть график за любой период.
- ✅ **Telegram-уведомления** – мгновенное оповещение, когда цена снижается более чем на заданный процент.
- ✅ **Дашборд с графиками** – интерактивный график изменения цены (React + Recharts).
- ✅ **Универсальный парсер** – поддерживает любой сайт через сохранение CSS-селекторов в базе данных.
- ✅ **REST API** – полная документация Swagger (доступна после запуска).

---

## 🧱 Технологический стек

### Бэкенд
- Python 3.11, FastAPI (асинхронный фреймворк)
- SQLAlchemy 2.0 (async) + Alembic
- PostgreSQL (хранение товаров, цен, селекторов)
- Celery + Redis (очередь задач и периодический парсинг)
- BeautifulSoup4 + httpx (парсинг HTML)
- Aiogram (Telegram бот для уведомлений)

### Фронтенд
- React 18, Vite
- Axios (HTTP клиент)
- Recharts (графики)
- React Router (маршрутизация)

### Инфраструктура
- Docker + Docker Compose (полная контейнеризация)

---

## 📋 Требования

- Docker и Docker Compose (рекомендуемый способ)
- Или локально: Python 3.11+, Node.js 18+, PostgreSQL, Redis

---

## 🛠️ Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/your-username/pricewatcher.git
cd pricewatcher
```
### 2. Настройка переменных окружения
Скопируйте пример конфигурации:

```bash
cp backend/.env.example backend/.env
Отредактируйте backend/.env:

Укажите SECRET_KEY (сгенерируйте любой сложную строку)

При желании добавьте TELEGRAM_BOT_TOKEN
```
### 3. Запуск через Docker Compose
```bash
После запуска будут доступны:
docker-compose up --build
```
Фронтенд: http://localhost:3000

API бэкенда: http://localhost:8000

Документация API: http://localhost:8000/docs

### 4. Локальный запуск (без Docker)
### Бэкенд:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
### Фронтенд:
```bash
cd frontend
npm install
npm run dev
```
### Важно: 
при локальном запуске нужно отдельно запустить PostgreSQL, Redis и Celery worker (команда celery -A app.tasks.celery_app worker --beat).

