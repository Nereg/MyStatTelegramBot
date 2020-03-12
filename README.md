# Телеграм бот для [MyStat](https://mystat.itstep.org/ru/auth/login/index) ! [![CodeFactor](https://www.codefactor.io/repository/github/nereg/mystattelegrambot/badge)](https://www.codefactor.io/repository/github/nereg/mystattelegrambot)
## Что умеет ?
1. Показывать топ потока и группы с ссылочками на фотки ! (/top)
2. Уведомлять о новых домашках (/subscribe)
3. **Полная** информация о тебе (/me)
4. Логин в MyStat (/login)
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
* `docker run -d --name ИМЯ --mount type=bind,source="$(pwd)"/,target=/main/ АЙДИШНИК`

## Список : "скоро будет"
- [x] Логин в майстат (безопасный!)
- [ ] Авто получение кристаликов за тот QR код на дверях
- [ ] Более точные уведомления о домашках
- [ ] Практически любая **твоя** идея

## Полезная информация

Парсим .env файлы : https://pypi.org/project/python-dotenv/

Библиотека для телеграма: https://github.com/eternnoir/pyTelegramBotAPI

Виртуальные окружения (VENV)(упс не используеться :/ ): https://docs.python-guide.org/dev/virtualenvs/ 

MyStat API (собственного производста)(версия комита 3f691e6) : https://github.com/Nereg/MyStatAPI

Гайд по базе данных : https://habr.com/en/post/321510/

Планировщик задач : https://apscheduler.readthedocs.io/en/stable/

# Репозиторий использует лицензию [GNU GPLv3](/LICENSE) 

# English version is coming soon!
