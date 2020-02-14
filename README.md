# Телеграм бот для [MyStat](https://mystat.itstep.org/ru/auth/login/index) ! [![CodeFactor](https://www.codefactor.io/repository/github/nereg/mystattelegrambot/badge)](https://www.codefactor.io/repository/github/nereg/mystattelegrambot)
## Что умеет ?
1. Показывать топ потока и группы с ссылочками на фотки !
2. Уведомлять о новых домашках
# Ссылка на оффициального [бота](https://t.me/testmystatbot)
## И это все ?!
Пока что да. Но! 
Во-первых, ты модешь предложить новые фитчи [сдесь](https://github.com/Nereg/MyStatTelegramBot/issues) либо написать [мне](https://t.me/OlegKusil) в личку !
Во-вторых, этот проект Open Source! Это значит что ВЕСЬ код доступен всем! И ты можешь добавить к этому боту все что ты пожелаешь! А потом предложить эти исправления или фитчи сдесь! Гайда пока что по этому нету но просто загугли Git (система на которой работает это репозиторий).
## Ну раз код всем доступен то я могу запустить своего бота ?
Да, верно ! Как ? 
### 1 путь
* Скачать (или склонировать) этот репозиторий
* Перейти в скачаную папку
* Отредактировать [example.env](/example.env)
* Переименовать его в .env
* `pip install -r requirements.txt`
* `py ./migration.py`
* Перейти в src
* `py main.py`
### 2 путь
* Установить [Docker](https://en.wikipedia.org/wiki/Docker_(software))
* Скачать (или склонировать) репозиторий
* Перейти в скачаную папку
* Отредактировать [example.env](/example.env)
* Переименовать его в .env
* `docker build .`
* Подождать пока появиться надпись: `Successfully built АЙДИШНИК`
* `docker run -d --name ЛЮБОЕ_ИМЯ АЙДИШНИК`

## Полезная информация

Парсим .env файлы : https://pypi.org/project/python-dotenv/

Библиотека для телеграма: https://github.com/eternnoir/pyTelegramBotAPI

Виртуальные окружения (VENV)(упс не используеться :/ ): https://docs.python-guide.org/dev/virtualenvs/ 

MyStat API (собственного производста)(версия комита 291f3d4) : https://github.com/Nereg/MyStatAPI

Гайд по базе данных : https://habr.com/en/post/321510/

Планировщик задач : https://apscheduler.readthedocs.io/en/stable/

# English version is coming soon!
