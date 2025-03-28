import telebot
import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help'])
def help_text(message):
    bot.reply_to(message, """
                 Вітаю, я - бот для допомоги тобі у повсякденному житті.
                 Зазвичай, мене використовують для генерації паролів, але я вмію і багато іншого.
                 Введи "/start" для початку роботи.
                 """)
    
    
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)
    
    
bot.infinity_polling()