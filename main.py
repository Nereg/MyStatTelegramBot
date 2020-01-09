import time , logging.config, sys, logging, sqlite3, API, telebot
from os import environ # for geting values from parsed env file
from dotenv import load_dotenv # for parsing .env files
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

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
#                    TEXT
#-------------------------------------------------

hello_message = '<b>Приветсвую !</b>\nКороче да я бот\nМой создатель: <b>Олег Кисиль</b>!\nТы можешь к нему обращаться если будут какие либо вопросы.\nТак-же если хочешь узнать как работает этот бот можешь посмотреть исзодный код на <a href="https://github.com/Nereg/MyStatTelegramBot">github</a>\n<b>Удачи!</b>'

help_message = '<b>Нужна помощь?</b>\nНе проблемма!\n Я имею несколько команд и вот их списокю\n/help - выводит эту помощь\nТак-же если думаешь что какая то моя часть работает неправильно или я не отвечаю можешь обратьться к моему\n Кстати вот <a href="tg://user?id={}">ссылочка</a> на него'.format(admin_id)

notify_message = '<b>Уведомления</b>\nПока что в боте есть только один тип уведомлений : о новом дз.\n Скоро появятся и другие\nА пока подпишись на эти с помощью: /subscribe\n(Кстати скоро должны появиться более точные уведомления о новых дзшках! Только они потребуют логина в майстат)'

subscribe_help_message = '<b>На какие уведомления ты хочешь подписаться?</b>\n/subscribe homeworks - уведомления о новых домашних заданиях'

notification_messages = ['',
        "Появилось новое домашнее задание!",
]

#-------------------------------------------------
#                    INIT
#-------------------------------------------------

bot = telebot.TeleBot(token) # init bot
if debug:
        db_path = 'test.sqlite'
else:
        db_path = 'main.sqlite'

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': {'type': 'threadpool', 'max_workers': 5},
}
scheduler = BackgroundScheduler()
args = ('1',notification_messages)
job = scheduler.add_job(CheckHomework, 'interval', seconds=20)
scheduler.configure(jobstores=jobstores, executors=executors)

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

        #integrate telobot
        telebot.logger.addHandler(screen_handler)
        telebot.logger.setLevel(logging.DEBUG)
        return log_obj
    # =======================================================

#-------------------------------------------------
#                   COMMANDS
#-------------------------------------------------

@bot.message_handler(commands=['start'])
def handle_start(message):
        bot.send_message(message.chat.id,hello_message,parse_mode='html')
        makeRequest('INSERT INTO users (TelegramChatId,TelegramId) VALUES (?,?)',(message.chat.id,message.from_user.id)) #store chat id and user if for later use
        pass

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['help'])
def handle_help(message):
        bot.send_message(message.chat.id,help_message,parse_mode='html') 
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
        pass


#-------------------------------------------------
#                    START!
#-------------------------------------------------
scheduler.start() #start scheduler 
bot.polling() # START BOT !