# Foodgram - Продуктовый помощник
![Foodgram workflow](https://github.com/Edw125/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)  

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

## Описание проекта
Foodgram - это удобный сервис для публикации рецептов. Пользователи могут создавать свои рецепты, 
смотреть рецепты других пользователей, подписываться на публикации других пользователей, добавлять 
понравившиеся рецепты в «Избранное», перед походом в магазин скачивать в PDF сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.

## Сайт
Сайт доступен по ссылке:
[http://foodgram.servehttp.com/](http://foodgram.servehttp.com/)

## Документация к API
API документация доступна по ссылке (создана с помощью redoc):
[http://foodgram.servehttp.com/api/docs/](http://foodgram.servehttp.com/api/docs/)

## Установка проекта локально
* Склонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/edw125/foodgram-project-react.git
cd foodgram-project-react
```

* Cоздать и активировать виртуальное окружение:
```bash
python -m venv env
```
```bash
source env/bin/activate
```

* Cоздайте файл `.env` в директории `/infra/` с содержанием:
```
SECRET_KEY = ${django-secret-key}
ALLOWED_HOSTS = ${localhost 127.0.0.1 backend}
SENTRY_DSN = ${https://example.ingest.sentry.io/5445412}
DB_ENGINE = django.db.backends.postgresql
DB_NAME = postgres
POSTGRES_USER = postgres
POSTGRES_PASSWORD = postgres
DB_HOST = db
DB_PORT = 5432
```

* Перейти в директорию и установить зависимости из файла requirements.txt:
```bash
cd backend/
pip install -r requirements.txt
```

* Выполните миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

* Запустите сервер:
```bash
python manage.py runserver
```

## Запуск проекта в Docker контейнере
* Установите Docker

Параметры запуска описаны в файлах `docker-compose.yml` и `nginx.conf` которые находятся в директории `infra/`.  
При необходимости добавьте/измените адреса проекта в файле `nginx.conf`

* Запустите docker compose:
```bash
docker-compose up -d --build
```  

  > После сборки появятся 3 контейнера:
  > 1. контейнер базы данных **db**
  > 2. контейнер приложения **backend**
  > 3. контейнер web-сервера **nginx**

* Примените миграции:
```bash
docker-compose exec backend python manage.py migrate
```
* Загрузите ингредиенты:
```bash
docker-compose exec backend python manage.py load_ingrs
```
* Загрузите теги:
```bash
docker-compose exec backend python manage.py load_tags
```
* Создайте администратора:
```bash
docker-compose exec backend python manage.py createsuperuser
```
* Соберите статику:
```bash
docker-compose exec backend python manage.py collectstatic --noinput
```
* Дополнительные команды очистки докера:
```bash
docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
docker rmi $(docker images -a -q)
docker volume prune
```

## Авторы
https://github.com/Edw125 -   Бэкенд и деплой сервиса Foodgram

https://github.com/yandex-praktikum - Фронтенд сервиса Foodgram