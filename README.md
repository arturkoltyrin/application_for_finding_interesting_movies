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

5. Подключение БД и Redis
SECRET_KEY=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
LOCATION=

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