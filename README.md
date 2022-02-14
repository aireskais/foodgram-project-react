![example workflow](https://github.com/aireskais/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Продуктовый помощник([ссылка на запущенный проект](http://andrisfood.ddns.net:9900/)):
Сайт(и API), на котором пользователи могут публиковать рецепты, добавлять 
чужие рецепты в избранное и подписываться на публикации других авторов.
Сервис «Список покупок» позволит пользователям создавать список продуктов,
которые нужно купить для приготовления выбранных блюд.

# Как запустить проект на своем сервере:

Клонировать репозиторий(а можно только 2 файла, см. ниже):
```
git@github.com:aireskais/foodgram-project-react.git
```
Залить на свой сервер файлы docker-compose.yml и nginx.conf(редачим под свой сервер), прямо в корень:
```
scp my_file username@host:<путь-на-сервере>
```

Прописываем секреты:
```
DOCKER_USERNAME=<логин для докера>
DOCKER_PASSWORD=<пароль>
HOST=<IP сервера>
USER=<пользователь на сервере>
SSH_KEY=<приватный ключ от компьтера, у которого есть доступ на сервер>
PASSPHRASE=<защитный пароль для ssh ключа, если есть>
TELEGRAM_TO=<Id бота в телегра, для отправки уведомления об успешном деплое>
TELEGRAM_TOKEN=<токен для бота>
DB_ENGINE=<django.db.backends.postgresql или любой другой>
DB_NAME=<postgres или любой другой>
POSTGRES_USER=<ваш пользователь>
POSTGRES_PASSWORD=<пароль для вашего пользователя>
DB_HOST=db
DB_PORT=5432
```

Запустить билд:
```
sudo docker-compose up -d
```
Запустить миграции, создать суперпользователя, собрать статику: 
```
sudo docker-compose exec api python manage.py migrate
sudo docker-compose exec api python manage.py createsuperuser
sudo docker-compose exec api python manage.py collectstatic --no-input
```
Заполнить БД тестовыми данными(ингредиенты и теги):
``` 
sudo docker-compose exec api python manage.py import_data
```
Все, можно переходить сюда:

[Продуктовый помощник](http://andrisfood.ddns.net:9900/)


# Автор проекта:
[Андрис](https://github.com/aireskais)
