import time , logging.config, sys, logging, sqlite3, API, telebot
from os import environ # for geting values from parsed env file
from dotenv import load_dotenv # for parsing .env files
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
#own modules
from helpers import *
from strings import *


#-------------------------------------------------
#                   LOADING...
#-------------------------------------------------

load_dotenv() 
token = environ.get('token') # get token from .env
admin_id = environ.get('admin_id') # admin id 
password = environ.get('password') #default password
APIusername = environ.get('APIusername') #default username for MyStat
debug = environ.get('debug') #debug or not
logging_path = environ.get('logging_path') #debug or not
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
args = ('1',notification_messages)
job = scheduler.add_job(CheckHomework, 'interval', seconds=20)
scheduler.configure(executors=executors)#working just ok witjout storage and made MANY warnings when using so I remove storage
botname = "@"+bot.get_me().username 
#-------------------------------------------------
#                   COMMANDS
#-------------------------------------------------

@bot.message_handler(commands=['start'])
def handle_start(message):
        bot.send_message(message.chat.id,hello_message,parse_mode='html')
        if (isAdmin(message.from_user)):
                bot.send_message(message.chat.id,'<b>Ты админ!</b>',parse_mode='html')
        makeRequest('INSERT INTO users (TelegramChatId,TelegramId) VALUES (?,?)',(message.chat.id,message.from_user.id)) #store chat id and user if for later use
        pass

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['help'])
def handle_help(message):
        bot.send_message(message.chat.id,help_message.format(admin_id),parse_mode='html') 
        pass

#-------------------------------------------------
#                    TOP
#-------------------------------------------------

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['top'])
def handle_top(message):
        bot.send_message(message.chat.id,'Хочешь узнать топ группы ? /group Хочешь узнать топ паралели ? /stream',parse_mode='html')
        pass

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['group'])
def handle_group_top(message):
        Mymessage = 'Топ группы :\n'
        global password,APIusername
        token = API.getKey(password,APIusername)
        top = API.GetClassLeaderboard(token)
        for place in top:
                Mymessage = Mymessage + 'Место {}: <a href="{}">{}</a> Очков: {}'.format(place['position'],place['photo_path'],place['full_name'],place['amount']) + '\n'
        bot.send_message(message.chat.id,Mymessage,parse_mode='html',disable_web_page_preview=True)
        pass

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['stream'])
def handle_stream_top(message):
        Mymessage = 'Топ потока :\n'
        global password,APIusername
        token = API.getKey(password,APIusername)
        top = API.GetStreamLeaderboard(token)
        for place in top:
                Mymessage = Mymessage + 'Место {}: <a href="{}">{}</a>'.format(place['position'],place['photo_path'],place['full_name']) + '\n'
        bot.send_message(message.chat.id,Mymessage,parse_mode='html',disable_web_page_preview=True) 
        pass

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['notify'])
def handle_notify(message):
        bot.send_message(message.chat.id,notify_message,parse_mode='html') 
        pass

@bot.message_handler(commands=['subscribe'])
def handle_subscribe(message):
        params = message.text
        params = params.split()
        if 'homeworks' in params:
                bot.send_message(message.chat.id,'Окей!\nМаякну если будут новые домашние задания!',parse_mode='html')
                makeRequest('INSERT INTO subscriptions (Type,ChatId) VALUES (?,?)',(1,message.chat.id))
        else:
                bot.send_message(message.chat.id,subscribe_help_message,parse_mode='html') 
        pass
#-------------------------------------------------
#                  TEST COMMANDS
#-------------------------------------------------

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['test'])
def test(message):  
        bot.send_message(message.chat.id,botname)
        pass


#-------------------------------------------------
#                    START!
#-------------------------------------------------
scheduler.start() #start scheduler 
bot.polling() # START BOT !
mainLogger.debug('Stopped all systems!')