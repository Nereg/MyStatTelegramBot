import telebot # maintelegram library
import API # My MyStat API!
import sqlite3# DB !!!
import logging # logging
import sys
import logging.config
from os import environ # for geting values from parsed env file
from dotenv import load_dotenv # for parsing .env files
from logging.handlers import TimedRotatingFileHandler

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
#                    INIT
#-------------------------------------------------

bot = telebot.TeleBot(token) # init bot
if debug:
        db_path = 'test.sqlite'
else:
        db_path = 'main.sqlite'

#-------------------------------------------------
#                    TEXT
#-------------------------------------------------

hello_message = '<b>Приветсвую !</b>\nКороче да я бот\nМой создатель: <b>Олег Кисиль</b>!\nТы можешь к нему обращаться если будут какие либо вопросы.\nТак-же если хочешь узнать как работает этот бот можешь посмотреть исзодный код на <a href="https://github.com/Nereg/MyStatTelegramBot">github</a>\n<b>Удачи!</b>'

help_message = '<b>Нужна помощь?</b>\nНе проблемма!\n Я имею несколько команд и вот их списокю\n/help - выводит эту помощь\nТак-же если думаешь что какая то моя часть работает неправильно или я не отвечаю можешь обратьться к моему\n Кстати вот <a href="tg://user?id={}">ссылочка</a> на него'.format(admin_id)

#-------------------------------------------------
#               HELPER FUNCTIONS
#-------------------------------------------------

def makeRequest(SQL,params=[]): # wow universal ! 
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(SQL,params)
        # Если мы не просто читаем, но и вносим изменения в базу данных - необходимо сохранить транзакцию
        conn.commit()
        results = cursor.fetchall()
        conn.close() # close connection to DB! (but I don`t think that this is good idea)
        return results

# ================== Logger ================================ (from https://stackoverflow.com/a/57021857/11544952 + some changes)
def Logger(name):
        #print to file
        file_name = logging_path+'main.log'
        formatter = logging.Formatter(fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                      datefmt='%Y/%m/%d %H:%M:%S') # %I:%M:%S %p AM|PM format
        logging.basicConfig(filename = '%s' %(file_name),format= '%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                      datefmt='%Y/%m/%d %H:%M:%S', filemode = 'w', level = logging.DEBUG)
        log_obj = logging.getLogger(name)
        log_obj.setLevel(logging.DEBUG)

        # console printer
        screen_handler = logging.StreamHandler(stream=sys.stdout) #stream=sys.stdout is similar to normal print
        screen_handler.setFormatter(formatter)
        logging.getLogger(name).addHandler(screen_handler)

        return log_obj
    # =======================================================

#-------------------------------------------------
#                   COMMANDS
#-------------------------------------------------

@bot.message_handler(commands=['start'])
def handle_start(message):
        bot.send_message(message.chat.id,hello_message,None,None,None,'html') # yeah so sad just for html
        pass

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['help'])
def handle_help(message):
        bot.send_message(message.chat.id,help_message,None,None,None,'html') # yeah so sad just for html
        pass

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['top'])
def handle_top(message):
        bot.send_message(message.chat.id,'Хочешь узнать топ группы ? /group Хочешь узнать топ паралели ? /stream',None,None,None,'html') # yeah so sad just for html
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
        bot.send_message(message.chat.id,Mymessage,True,None,None,'html') # yeah so sad just for html also disabling links preview
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
        bot.send_message(message.chat.id,Mymessage,True,None,None,'html',False) # yeah so sad just for html
        pass

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['test'])
def test(message):     
        log = Logger('test')
        log.debug('test!')
        print(makeRequest('SELECT * FROM main'))
        pass


#-------------------------------------------------
#                    START!
#-------------------------------------------------

bot.polling() # START BOT !