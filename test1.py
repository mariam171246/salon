import telebot
from telebot import types
from config import api_token
import json

TOKEN = api_token
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Здравствуйте, приветствуем вас в нашем косметическом салоне!")

    keyboard = generate_keyboard()
    bot.send_message(message.chat.id, text="Выбери кнопку", reply_markup=keyboard)



def generate_keyboard():
    keyboard = types.InlineKeyboardMarkup() 

    for i in range(1, 5):
        button = types.InlineKeyboardButton(text=f"кнопка {i}", callback_data="Радость")
        keyboard.add(button)
    return keyboard  

#add - добавить
if __name__ == "__main__":
    bot.polling(none_stop=True)  