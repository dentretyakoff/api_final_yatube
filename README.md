# Проект Yatube - ресурс для публикации постов.
Простой блог, на котром пользователи могу публиковать посты, оставлять комментарии, подписываться на авторов.
Django 3.2, DRF 3.12, ReDoc

## Установка и настройка
- Клонируйте репозиторий: `git clone git@github.com:dentretyakoff/api_final_yatube.git`
- Перейдите в директорию проекта: `cd ваш-каталог/api_final_yatube/`
- Создайте и активируйте виртуальное окружение: `python3 -m venv venv`
- Установите зависимости: `pip install -r requirements.txt`
- Выполните миграции: `python3 manage.py migrate`

## Использование
- Запустите приложение: `python3 manage.py runserver`
- Создайте суперпользователя: `python3 manage.py createsuperuser`
- Получите для него токен: `http://127.0.0.1:8000/api/v1/jwt/create/`
    - в теле запроса необходимо передать `username` и `password`
    ```
        {
        "username": "admin",
        "password": "very_strong_password"
        }
    ```
- Создайте новый пост: `http://127.0.0.1:8000/api/v1/posts/`
    - в теле запроса передайте:
        {
            "text": "Пост №1",
            "image": "image_in_base64",
        }

Подробнее о запросах к API в документации `http://127.0.0.1:8000/redoc/`

Лицензия
[MIT License](https://opensource.org/licenses/MIT)