# Приложение на Django Rest Framework (с использованием JSON:API), позволяющее управлять кошельками и транзакциями.


Данное приложение предоставляет REST API для работы с кошельками и транзакциями.

Кошелёк (Wallet) содержит поле label (название) и balance (текущий баланс).
Транзакция (Transaction) привязана к кошельку (wallet), имеет уникальный идентификатор txid и сумму amount.
При создании или обновлении транзакции баланс кошелька пересчитывается автоматически.


# Технологии:

Django 3.2+
Django Rest Framework
JSON:API
PostgreSQL (по умолчанию)


# Требования:
Python 3.10+
Docker и Docker Compose (если хотите запускать в контейнерах)
PostgreSQL (если локально без Docker)

# Установка и запуск (локально)

1) Клонируйте репозиторий:
```
git clone https://github.com/username/drf-wallet.git
cd drf-wallet
```
2) Создайте виртуальное окружение (опционально):
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
или
.venv\Scripts\activate  # Windows
```
3) Установите зависимости:
```
pip install -r requirements.txt
```
4) Настройте базу данных (PostgreSQL) и переменные окружения.

Создайте файл .env на подобии .env-example.

5) Выполните миграции:
```
python manage.py migrate
```
6) Запустите сервер:
```
python manage.py runserver
```
7) Проверьте работу:
Перейдите в браузере на http://127.0.0.1:8000/api/v1/wallets/ — должно отобразиться JSON-API (или Browsable API, если включено).


# Запуск в Docker
1) Убедитесь, что у вас установлены Docker и Docker Compose.
2) Проверьте/создайте файл .env с настройками (например, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, DATABASE_URL и т. д.).
3) Постройте образы:
```
docker-compose build
```
4) Запустите контейнеры:
```
docker-compose up
```
5) Выполните миграции:
```
docker-compose run web python manage.py migrate
```
6) Проверьте:
Перейдите в браузере на http://127.0.0.1:8000/api/v1/wallets/ — должно отобразиться JSON-API (или Browsable API, если включено).

# Структура URL
/api/v1/wallets/
- GET: список кошельков
- POST: создать новый кошелёк
/api/v1/wallets/<id>/
- GET, PUT, PATCH, DELETE для конкретного кошелька
/api/v1/wallets/<id>/transactions/
- Список транзакций конкретного кошелька (кастомный action)
/api/v1/transactions/
- GET: список транзакций
- POST: создать новую транзакцию
/api/v1/transactions/<id>/
- GET, PUT, PATCH, DELETE для конкретной транзакции
/health/
- Проверка состояния (возвращает «OK»)


# Запуск тестов
# Локально
```
python manage.py test
```
# В Docker
```
docker-compose run web python manage.py test
```
# Быстрый старт (Quick Start Guide)
1) Клонировать репозиторий:
```
git clone https://github.com/username/drf-wallet.git
cd drf-wallet
```
2) Создать виртуальное окружение и установить зависимости:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3) Настроить базу данных (локально) или использовать Docker.
4) Выполнить миграции:
```
python manage.py migrate
```
5) Запустить сервер:
```
python manage.py runserver
```
6) Перейти в браузере на http://127.0.0.1:8000/api/v1/wallets/ — должно открыться API.
