# Атомные привычки 
(Джанго проект со SPA веб-приложением и созданием бэкенд-сервера, который позволяет работать с телеграм ботом.)

## Установка
1. Клонируйте репозиторий:
git clone https://github.com/arturkoltyrin/atomic_habits_backend_part_spa_web_application.git

2. Создайте и активируйте виртуальное окружение:
python -m venv venv

3. Установите зависимости:
Убедитесь, что у вас установлен Poetry.
Затем выполните команду: poetry install

4. Запустите сервер разработки:
python manage.py runserver

## Технологии

- Python — основной язык программирования.
- Django — веб-фреймворк для создания приложения.
- Django REST Framework (DRF) — toolkit для построения REST API.
- PostgreSQL — база данных.
- Дополнительные библиотеки (указаны в pyproject.toml).



## Установка
Следуй этим шагам, чтобы установить и запустить проект локально:

## Склонируй репозиторий:

### Создай виртуальное окружение:
- python -m venv venv
- source venv/bin/activate  # Для Windows: venv\Scripts\activate

### Установи зависимости:
- pyproject.toml

### Применяй миграции:
- python manage.py migrate
### Создай суперпользователя (опционально, для доступа к админке):
- python manage.py csu
### Запусти сервер:
- python manage.py runserver
Сервер будет доступен по адресу http://127.0.0.1:8000/
### Выполните действия:
- Активируйте Redis (redis-server)
- Запустите во второй вкладке celery beat: celery -A config beat -l info -S django
- Запустите в терминале celery worker: celery -A config worker -l INFO
- В телеграм боте нажмите /start

## Структура проекта

- settings.py — конфигурация проекта, включая настройки DRF и аутентификации.
- urls.py — маршруты API.
- models.py — модели данных. 
- serializers.py — сериализаторы для преобразования данных.
- views.py — представления для обработки запросов.

## Лицензия
Этот проект распространяется под лицензией MIT. Подробности см. в файле LICENSE (если он есть в репозитории).