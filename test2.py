import telebot
from telebot import types
from config import api_token


TOKEN = api_token
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Бот запущен")
    
    keyboard = generate_keyboard() 
    bot.send_message(message.chat.id, text="Выбери своё настроение", reply_markup=keyboard)
    

@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):

    if "word" in call.data:
        data= call.data.replace("word: ", "")
        bot.send_message(call.message.chat.id, text=f"Вы выбрали настроение {data}")

         
def generate_keyboard():

    mood = ["Радость", "Грусть", "Спокойствие", "Удивление"]
    keyboard = types.InlineKeyboardMarkup() 


    #for i in mood:
       # n = f"word: {i}"
       # button = types.InlineKeyboardButton(text={i}, callback_data = "...")
       # keyboard.add(button)
    
    for i in mood:
        data = f"word: {i}"
        button = types.InlineKeyboardButton(text=f"{i}", callback_data = data)
        keyboard.add(button)
    return keyboard

    



# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
