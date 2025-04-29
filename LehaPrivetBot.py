import telebot
from datetime import datetime
import random
import time
from telebot import types

TOKEN = '7904803262:AAEHryGLGAJxBVukauXf3kPfsgLX_Q6pzoU'
bot = telebot.TeleBot(TOKEN)

def dice_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🎲 1d6')
    btn2 = types.KeyboardButton('🎲🎲 2d6')
    btn3 = types.KeyboardButton('🔮 1d20')
    btn4 = types.KeyboardButton('🔙 Назад')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def timer_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('⏱ 30 сек')
    btn2 = types.KeyboardButton('⏱ 1 мин')
    btn3 = types.KeyboardButton('⏱ 5 мин')
    btn4 = types.KeyboardButton('🔙 Назад')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я многофункциональный бот. Доступные команды:\n"
                         "/time - текущее время\n"
                         "/date - текущая дата\n"
                         "/dice - бросить кубики\n"
                         "/timer - установить таймер")

@bot.message_handler(commands=['time'])
def send_time(message):
    bot.reply_to(message, f"Текущее время: {datetime.now().strftime('%H:%M:%S')}")

@bot.message_handler(commands=['date'])
def send_date(message):
    bot.reply_to(message, f"Сегодня: {datetime.now().strftime('%d.%m.%Y')}")

@bot.message_handler(commands=['dice'])
def dice_command(message):
    bot.send_message(message.chat.id, "Выберите тип кубика:", reply_markup=dice_keyboard())

@bot.message_handler(func=lambda m: m.text in ['🎲 1d6', '🎲🎲 2d6', '🀄 1d20'])
def handle_dice(message):
    if message.text == '🎲 1d6':
        result = random.randint(1, 6)
        bot.send_message(message.chat.id, f"Результат: {result}", reply_markup=dice_keyboard())
    elif message.text == '🎲🎲 2d6':
        result1, result2 = random.randint(1, 6), random.randint(1, 6)
        bot.send_message(message.chat.id, f"Результаты: {result1} и {result2}", reply_markup=dice_keyboard())
    elif message.text == '🀄 1d20':
        result = random.randint(1, 20)
        bot.send_message(message.chat.id, f"Результат: {result}", reply_markup=dice_keyboard())

@bot.message_handler(commands=['timer'])
def timer_command(message):
    bot.send_message(message.chat.id, "Выберите время:", reply_markup=timer_keyboard())

@bot.message_handler(func=lambda m: m.text in ['⏱ 30 сек', '⏱ 1 мин', '⏱ 5 мин'])
def handle_timer(message):
    chat_id = message.chat.id
    if message.text == '⏱ 30 сек':
        delay = 30
    elif message.text == '⏱ 1 мин':
        delay = 60
    elif message.text == '⏱ 5 мин':
        delay = 300

    bot.send_message(chat_id, f"Таймер установлен на {message.text.split()[1]}!", reply_markup=timer_keyboard())
    
    def timer_thread(chat_id, delay):
        time.sleep(delay)
        bot.send_message(chat_id, "⏰ Время вышло!")

    import threading
    threading.Thread(target=timer_thread, args=(chat_id, delay)).start()

# ===== Обработка кнопки "Назад" =====
@bot.message_handler(func=lambda m: m.text == '🔙 Назад')
def back_command(message):
    bot.send_message(message.chat.id, "Главное меню", reply_markup=types.ReplyKeyboardRemove())

# ===== Эхо-режим =====
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f'Я получил сообщение "{message.text}"')

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()