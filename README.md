## Приложение для поиска интересных фильмов
(Джанго проект)

### Установка
1. Клонируйте репозиторий:
git clone https://github.com/arturkoltyrin/application_for_finding_interesting_movies.git

2. Создайте и активируйте виртуальное окружение:
python -m venv venv

3. Установите зависимости:
pip install -r requirements.txt

4. Установите и запустите Redis
redis-server

5. Подключите БД
Убедитесь, что PostgreSQL установлен и запущен.
Используйте утилиту pgAdmin для запуска сервера.

Создайте файл .env и заполните его по образцу .env.sample:

SECRET_KEY='django-insecure-1m9k*p=m=4ujak=alqo^b%+p$5u^ra3vu5+2*+a!1k(6oeeq0v'
POSTGRES_USER = postgres
POSTGRES_PASSWORD = <пароль>
POSTGRES_HOST = localhost
POSTGRES_PORT = 5432
LOCATION=<локальный путь>

6. Примените миграции:
python manage.py migrate

7. Добавление тестовых данных:
python manage.py test_data

8. Создайте суперпользователя:
python manage.py createsuperuser

9. Запустите сервер разработки:
python manage.py runserver

10. Использование веб-интерфейса:
Главная страница http://127.0.0.1:8000/movies/