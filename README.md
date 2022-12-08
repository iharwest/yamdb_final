# API_YaMDB
![yamdb_workflow](https://github.com/iharwest/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
Описание проекта
----------
Проект сервиса API для YaMDB - социальной сети, которая собирает отзывы и оценки пользователей 
на произведения. Пользователи оставляют отзывы в текстовом формате. Оценка ставится в диапазоне от 1 до 10.
На основании оценок рассчиывается общий рейтинг произведения.
Произведения делятся на категории и жанры.
Новые жанры, категории и произведения может добавлять только администратор.
Для авторизации пользователей используется код подтверждения.Для аутентификации пользователей используются JWT-токены. 

Реализован REST API CRUD для моделей проекта, для аутентификации примненяется JWT-токен.
В проекте реализованы пермишены, фильтрации, сортировки и поиск по запросам клиентов, реализована пагинация ответов от API, установлено ограничение количества запросов к API.
Проект разворачивается в трех Docker контейнерах: web-приложение, postgresql-база данных и nginx-сервер.

Системные требования
----------
* Python 3.6+
* Docker
* Works on Linux, Windows, macOS

Стек технологий
----------
* Python 3.8
* Django 2.2
* Django Rest Framework
* Simple-JWT
* PostreSQL
* Nginx
* gunicorn
* Docker
* DockerHub

Запуск проекта (Linux и macOS)
----------
Cоздать и открыть файл .env с переменными окружения.
Заполнить ```.env``` файл с переменными окружения по примеру:
```
DB_ENGINE=django.db.backends.postgresql

DB_NAME=postgres

POSTGRES_PASSWORD=postgres

POSTGRES_USER=postgres

DB_HOST=db

DB_PORT=5432

SECRET_KEY=************
```
Установить и запустить приложения в контейнерах:
```
docker-compose up -d
```
Запустить миграции, создать суперюзера, собрать статику и заполнить БД:
```
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser

docker-compose exec web python manage.py collectstatic --no-input 

docker-compose exec web python manage.py loaddata fixtures.json
```
Документация к проекту
----------
Документация для API после установки доступна по адресу 

```http://158.160.9.62/redoc/```