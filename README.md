# Telegraph Clone

Клон [телеграфа](http://telegra.ph/), фичи:
- размещение постов
- генерация для каждога поста уникального URL
- посты хранятся в БД (sqlite)

# Запуск (локально)

## Устанавливаем зависимости:
```#!bash

pip install -r requirements.txt

```
## Создаем БД(sqlite)
```#!bash

python db_schema.py

```
## Запускаем сервер
```#!bash

python server.py

```
## Готово!
идем на локальный адрес [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

# Готовая версия на Heroku
Посты хранятся не более 30мин [здесь](https://dry-dawn-40056.herokuapp.com/)

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
