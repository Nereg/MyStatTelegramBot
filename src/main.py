import time , logging.config, sys, logging, sqlite3, API, telebot ,random 
from os import environ # for geting values from parsed env file
from dotenv import load_dotenv # for parsing .env files
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from telebot import types # buttons !!!
#own modules
from helpers import *
from strings import *
from dotenv import load_dotenv
from pathlib import Path  # python3 only

#-------------------------------------------------
#                   LOADING...
#-------------------------------------------------
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)
token = environ.get('token') # get token from .env
admin_id = environ.get('admin_id') # admin id 
password = environ.get('password') #default password
APIusername = environ.get('APIusername') #default username for MyStat
debug = environ.get('debug') #debug or not
if debug == 'true': # small little convertion 
        debug = True
else:
        debug = False

#-------------------------------------------------
#             PERIODICAL FUNCTIONS
#-------------------------------------------------
def CheckHomework():
        log = Logger('HomeworkCheck')
        token  = API.getKey(password,APIusername) # get token for default login data
        homeworks = API.GetHomeworks(token) #get count of homeworks
        current = homeworks[3]
        res = makeRequest('SELECT * FROM stuff WHERE Type=1')
        last = int(res[0][1])
        if (current > last):
                makeRequest('UPDATE stuff SET Data=? WHERE Type=1',(str(current)))
                log.debug('Yeah new hometasks !')
                args = ('1',notification_messages)
                scheduler.add_job(SendNotifications, 'interval', seconds=5,args=args,id='Sender')
                return
        elif (current == 0):
                makeRequest('UPDATE stuff SET Data=? WHERE Type=1',(str(0)))
                log.debug('Zero homeworks ! Yeah you done them !')
        else:
                log.debug('No new homework !')
                return

def SendNotifications(type,text):
        scheduler.remove_job('Sender') # yeah remove yourself :/
        log = Logger('NotificationSender')
        log.debug('Started sending notifications for {} type!'.format(type))
        List = makeRequest('SELECT * FROM subscriptions WHERE Type =?',(type))
        ids = []
        for user in List:
                ids.append(user[2])
        log.debug(f'Sending notifications to this ids: {ids}')
        for ChatId in ids:
                bot.send_message(int(ChatId),text[int(type)],parse_mode='html') 

def SendToAll(message):
        scheduler.remove_job('SendToAll')
        log = Logger('MassSender')
        log.debug('Started')
        sql = 'DELETE FROM users WHERE id NOT IN (SELECT *  FROM (SELECT MIN(id)FROM users GROUP BY TelegramChatId) temp)' #sql qury to delete all duplicates
        makeRequest(sql)
        log.debug('Cleared DB from clones!')
        log.debug('Sending messages with "{}" message'.format(message))
        List = makeRequest('SELECT * FROM users')
        #log.debug(List)
        ids = []
        for user in List:
                ids.append(user[1])
        log.debug(f'Sending notifications to this ids: {ids}')
        for ChatId in ids:
                bot.send_message(int(ChatId),message,parse_mode='html') 


#-------------------------------------------------
#                    INIT
#-------------------------------------------------
mainLogger = Logger('Main code')
bot = telebot.TeleBot(token) # init bot
mainLogger.debug('Inited bot!')
executors = {
    'default': {'type': 'threadpool', 'max_workers': 5},
}
scheduler = BackgroundScheduler()
job = scheduler.add_job(CheckHomework, 'interval', minutes=5)
scheduler.configure(executors=executors)#working just ok witjout storage and made MANY warnings when using so I remove storage
botname = "@"+bot.get_me().username 
#-------------------------------------------------
#                   COMMANDS
#-------------------------------------------------

@bot.message_handler(commands=['start'])
def handle_start(message):
        bot.send_message(message.chat.id,hello_message,parse_mode='html')
        if (isAdmin(message.from_user)):
                bot.send_message(message.chat.id,'<b>Воу палехче ты админ!</b>',parse_mode='html')
                bot.send_message(message.chat.id,'Вот список команд которые тебе доступны :\n/sendAll - прислать сообщение для всех пользователей бота! Даже с HTML но помоему нельзя вставить новую линию(но ты модешь это пофиксить ленивая ты задница)',parse_mode='html')
        makeRequest('INSERT INTO users (TelegramChatId,TelegramId) VALUES (?,?)',(message.chat.id,message.from_user.id)) #store chat id and user if for later use
        sql = 'DELETE FROM users WHERE id NOT IN (SELECT *  FROM (SELECT MIN(id)FROM users GROUP BY TelegramChatId) temp)' #sql qury to delete all duplicates
        makeRequest(sql)
        pass

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['help'])
def handle_help(message):
        bot.send_message(message.chat.id,help_message.format(admin_id),parse_mode='html') 
        if (isAdmin(message.from_user)):
                bot.send_message(message.chat.id,'<b>Воу палехче ты админ!</b>',parse_mode='html')
                bot.send_message(message.chat.id,'Вот список команд которые тебе доступны :\n/sendAll - прислать сообщение для всех пользователей бота! Даже с HTML но помоему нельзя вставить новую линию(но ты модешь это пофиксить ленивая ты задница)',parse_mode='html')
        pass

#-------------------------------------------------
#                    TOP
#-------------------------------------------------

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['top'])
def handle_top(message):
        markup = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True)
        itembtn1 = types.KeyboardButton('Топ потока')
        itembtn2 = types.KeyboardButton('Топ группы')
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id,'Хочешь узнать топ группы ?',parse_mode='html',reply_markup=markup)
        pass

@bot.message_handler(commands=['subscribe'])
def handle_subscribe(message):
        markup = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True)
        itembtn1 = types.KeyboardButton('Подписка на новые домашки')
        markup.add(itembtn1)
        bot.send_message(message.chat.id,subscribe_help_message,parse_mode='html',reply_markup=markup) 
        pass

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['share'])
def handle_top(message):
        link = "t.me/"+bot.get_me().username
        bot.send_message(message.chat.id,share_message.format(link,link),parse_mode='html')
        pass
#-------------------------------------------------
#                  TEST COMMANDS
#-------------------------------------------------

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['test'],func=lambda message:isAdmin(message.from_user)) # hah very easy check for admin
def test(message):  
        markup = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True)
        itembtn1 = types.KeyboardButton('Топ потока')
        itembtn2 = types.KeyboardButton('Топ группы')
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id,botname,reply_markup=markup)
        pass
#-------------------------------------------------
#                  ADMIN COMMANDS
#-------------------------------------------------
# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['sendAll'],func=lambda message:isAdmin(message.from_user)) # hah very easy check for admin
def sendAll(message): 
        params = message.text
        params = params.split()
        text = ""
        i = 0
        for word in params: 
                if i ==0:
                        i +=1
                        continue
                text += " "+word
                i += 1
        scheduler.add_job(SendToAll, 'interval', seconds=10,args=[text],id='SendToAll')
        bot.send_message(message.chat.id,'Ща будет сделано админ! Если че там хтмл разметочка есть ) ')
        pass

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['status'],func=lambda message:isAdmin(message.from_user)) # hah very easy check for admin
def status(message): 
        StatusText = "Зарегистрировано в боте: {} плебеев\nПодписано на уведомления: {}\nНу и как ты блин видишь я работаю !"
        regCount = makeRequest("SELECT COUNT(*) FROM users")
        notifyCount = makeRequest("SELECT COUNT(*) FROM subscriptions")
        bot.send_message(message.chat.id,StatusText.format(regCount[0][0],notifyCount[0][0]))
        pass

#-------------------------------------------------
#                  DEFAULT HANDLER
#-------------------------------------------------
@bot.message_handler(regexp=".") # see https://docs.python.org/2/library/re.html#regular-expression-syntax
def handleDefault(message): 
        text = message.text
        if (text == "Топ группы"):
                Mymessage = 'Топ группы :\n'
                global password,APIusername
                token = API.getKey(password,APIusername)
                top = API.GetClassLeaderboard(token)
                for place in top:
                        Mymessage = Mymessage + 'Место {}: <a href="{}">{}</a> Очков: {}'.format(place['position'],place['photo_path'],place['full_name'],place['amount']) + '\n'
                bot.send_message(message.chat.id,Mymessage,parse_mode='html',disable_web_page_preview=True)
        elif (text == "Топ потока"):
                Mymessage = 'Топ потока :\n'
                token = API.getKey(password,APIusername)
                top = API.GetStreamLeaderboard(token)
                for place in top:
                        Mymessage = Mymessage + 'Место {}: <a href="{}">{}</a>'.format(place['position'],place['photo_path'],place['full_name']) + '\n'
                bot.send_message(message.chat.id,Mymessage,parse_mode='html',disable_web_page_preview=True) 
        elif (text == "Подписка на новые домашки"):
                bot.send_message(message.chat.id,'Окей!\nМаякну если будут новые домашние задания!',parse_mode='html')
                makeRequest('INSERT INTO subscriptions (Type,ChatId) VALUES (?,?)',(1,message.chat.id))
        else:
                bot.send_message(message.chat.id,error_messages[random.randint(0,2)])
                pass
        pass

#-------------------------------------------------
#                    START!
#-------------------------------------------------
scheduler.start() #start scheduler 
bot.polling() # START BOT !
mainLogger.debug('Stopped all systems!')