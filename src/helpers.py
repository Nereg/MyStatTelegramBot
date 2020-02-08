#some helper functions
#TODO : make all this in one class to set some values from main code (but I can get config values)
import logging , sqlite3 ,sys,telebot
from os import environ # for geting values from parsed env file
#-------------------------------------------------
#               HELPER FUNCTIONS
#-------------------------------------------------

def makeRequest(SQL,params=[]): # wow universal ! 
        conn = sqlite3.connect(environ.get('db_path')) # yeah hardcoded 
        cursor = conn.cursor()
        cursor.execute(SQL,params)
        # Если мы не просто читаем, но и вносим изменения в базу данных - необходимо сохранить транзакцию
        conn.commit()
        results = cursor.fetchall()
        conn.close() # close connection to DB! (but I don`t think that this is good idea)
        return results

# ================== Logger ================================ (from https://stackoverflow.com/a/57021857/11544952 + some changes) TODO add logging from APS shelduer
def Logger(name):
        logging_path = environ.get('logging_path')
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

def isAdmin(user):
        adminId = int(environ.get('admin_id'))
        userId = user.id
        print(userId)
        print(adminId)
        if (userId == adminId):
                return True
        else:
                return False

