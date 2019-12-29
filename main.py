import telebot # maintelegram library
from os import environ # for geting values from parsed env file
from dotenv import load_dotenv # for parsing .env files
import API # My MyStat API!
load_dotenv() 

token = environ.get('token') # get token from .env

bot = telebot.TeleBot(token) # init bot

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling() # START BOT !