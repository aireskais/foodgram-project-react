# Продуктовый менеджер(описание проекта):
Сайт(и API), на котором пользователи могут публиковать рецепты, добавлять 
чужие рецепты в избранное и подписываться на публикации других авторов.\n
Сервис «Список покупок» позволит пользователям создавать список продуктов,
которые нужно купить для приготовления выбранных блюд.

# Как запустить проект локально:

Клонировать репозиторий и перейти в него в командной строке:
```
git@github.com:aireskais/foodgram-project-react.git
```
Создать и запустить виртуальное окружение:
```
python -m venv venv
python -m pip install --upgrade pip --user
pip install Django==4.0.2
source venv/Scripts/activate
```
Установить зависимости
```
pip install -r requirements.txt
```
Создать и запустить миграции, создать суперпользователя
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser 
```
Заполнить БД тестовыми данными(ингредиенты и теги):
```
python manage.py import_data
```
Запустить
```
python manage.py runserver
```

# Автор проекта:
[Андрис](https://github.com/aireskais)
