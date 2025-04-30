import telebot
from telebot import types

TOKEN = "7904803262:AAEHryGLGAJxBVukauXf3kPfsgLX_Q6pzoU"
bot = telebot.TeleBot(TOKEN)

hall_descriptions = {
    "entrance": "Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!",
    "exit": "Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!",
    "hall1": "Зал 1, обстрактные картины сигаретным пеплом",
    "hall2": "Зал 2, великие умы КемГУ с конца",
    "hall3": "Зал 3, зал в честь статуи БляхиМухи в Краснодаре",
    "hall4": "Зал 4, выставка конструкторов лего"
}

navigation = {
    "entrance": {"Зал 1": "hall1"},
    "hall1": {"Зал 2": "hall2", "Выход": "exit"},
    "hall2": {"Зал 3": "hall3"},
    "hall3": {"Зал 1": "hall1", "Зал 4": "hall4"},
    "hall4": {"Зал 1": "hall1"},
    "exit": {}
}

user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_states[message.chat.id] = "entrance"
    show_location(message.chat.id)


def show_location(chat_id):
    current_location = user_states[chat_id]
    description = hall_descriptions[current_location]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    if current_location == "exit":
        bot.send_message(chat_id, description)
        markup.add(types.KeyboardButton('/start'))
        bot.send_message(chat_id, "Нажмите /start для новой экскурсии.", reply_markup=markup)
        return

    buttons = []
    for name, location in navigation[current_location].items():
        buttons.append(types.KeyboardButton(name))

    markup.add(*buttons)

    navigation_text = "\n\nОтсюда вы можете перейти в:\n"
    for name in navigation[current_location].keys():
        navigation_text += f"- {name}\n"

    bot.send_message(chat_id, description + navigation_text, reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_navigation(message):
    chat_id = message.chat.id
    current_location = user_states.get(chat_id, "entrance")

    for name, location in navigation[current_location].items():
        if message.text == name:
            user_states[chat_id] = location
            show_location(chat_id)
            return

    if message.text == '/start':
        start(message)
    else:
        bot.send_message(chat_id, "Пожалуйста, используйте кнопки для навигации.")


if __name__ == '__main__':
    print("started")
    bot.polling()