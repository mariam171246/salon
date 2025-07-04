import telebot
import logging
import json
from config import api_token
from datetime import date, time, datetime
from telebot import types
from datetime import date, timedelta



#pip install pyTeleBotAPI

TOKEN = api_token

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Здравствуйте, приветствуем вас в нашем косметическом салоне!")
    

@bot.message_handler(commands=['show_dates'])
def handle_schedule(message):
    """выбор даты"""
     
    #отправляем клавиатуру с кнопками
    keyboard = generate_date_schedule()
    bot.send_message(message.chat.id, "Выберите день:", reply_markup=keyboard)

def generate_date_schedule(): #!!!!!!!!!!!!
    keyboard = types.InlineKeyboardMarkup()

    # получаем кнопки для указанной даты
    days = []

    for i in range(7):
        days.append(date.today() + timedelta(days=3 + i))

    #создаем кнопки и добавляем их на клавиатуру
    for button_text in days:
            callback_data = f"day: {button_text}"
            button = types.InlineKeyboardButton(text=f"{button_text}", callback_data=callback_data)
            keyboard.add(button)

    return keyboard

#функция для генерации клавиатуры с временем
def generate_time_keyboard(chosen_date):
    keyboard = types.InlineKeyboardMarkup()
    #получаем кнопки и добавляем их на клавиатуру
    times = ["10:00", "12:00", "15:00", "17:00"]

    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for appointment in data ["appointments"]:
            if appointment["date"] == chosen_date.strip():
                times.remove(appointment["time"])
    if times == []:
        return
   

     #создаеи кнопки и добавляем их на клавиатуру
    for time in times:
        callback_data = f"meeting: {chosen_date} {time}"
        button = types.InlineKeyboardButton(text=time, callback_data=callback_data)
        keyboard.add(button)

    return keyboard  

@bot.message_handler(commands=['add_review'])
def handle_review(message):
    bot.send_message(message.chat.id, "Напишите отзыв:")
    bot.register_next_step_handler(message, save_review)

#функции для сохранения отзыва
def save_review(message):
    client_id = message.chat.id
    review_text = message.text
    #запись отзыва в файл
    add_review(client_id, review_text)
    bot.send_message(message.chat.id, "Спасибо за ваш отзыв!") 


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    if "day" in call.data:
        date= call.data.replace("day: ", "")
        bot.send_message(call.message.chat.id, text=f"Вы выбрали дату {date}")
        #отправляем клавиатуру с доступным временем для выбранной даты
        

        keyboard = generate_time_keyboard(date)
        if not keyboard:
            bot.send_message(call.message.chat.id, "Нет свободных часов в этот день")
        else:
            # отправляем клавиатуру с доступным временем для выбранной даты
            bot.send_message(call.message.chat.id, "Выберите время:", reply_markup=keyboard)
            return    

    elif call.data.startswith("meeting:"):
        data = call.data.replace("meeting:", "")
        chosen_date, chosen_time = data.split()[0], data.split()[1]
        add_appointment(chosen_date, chosen_time, call.message.chat.id)
        bot.send_message(call.message.chat.id, f"Вы записаны на {chosen_date} в {chosen_time}. Ждём вас!")    

        
       


def add_appointment(date, time, client):
    #открыть файл
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        #добавим запсь в список саписей
        new_appointment = {'date': date, 'time': time, 'client': client}
        data['appointments'].append(new_appointment)

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


def add_review(client, text):
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        new_review = {'client': client, 'text': text}    
        data['review'].append(new_review)    

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)    



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    #add_appointment("12.03.25", "12:00", "Петрова А.")
    bot.polling(non_stop=True)
