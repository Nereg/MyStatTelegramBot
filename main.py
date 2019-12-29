import telebot # maintelegram library
from os import environ # for geting values from parsed env file
from dotenv import load_dotenv # for parsing .env files
import API # My MyStat API!
load_dotenv() 

token = environ.get('token') # get token from .env

bot = telebot.TeleBot(token) # init bot


# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['start'])
def handle_start_help(message):
        bot.send_message(message.chat.id,'<b>Приветсвую !</b>\ngdfgf\n',None,None,None,'html') # yeah so sad just for html
        pass

bot.polling() # START BOT !