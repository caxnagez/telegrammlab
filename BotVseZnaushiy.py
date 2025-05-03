import telebot
import json
import random
from telebot import types
from telebot import apihelper

TOKEN = '7904803262:AAEHryGLGAJxBVukauXf3kPfsgLX_Q6pzoU'
bot = telebot.TeleBot(TOKEN)

# джесон вопросы
quiz_data = {
    "test": [
        {
            "question": "В каком году была война 1812 года?",
            "answer": "1812"
        },
        {
            "question": "Где стоит статуя бляхамухи? В городе....",
            "answer": "Краснодар"
        },
        {
            "question": "Кто написал мангу Berserk?",
            "answer": "Кэнтаро Миура"
        },
        {
            "question": "Say my name ... you goddam right",
            "answer": "Haisenberg"
        },
        {
            "question": "Вопрос от Жака Фреско. Шёл ёж?",
            "answer": "Что?"
        }
    ]
}

with open('hist.json', 'w', encoding='utf-8') as f:
    json.dump(quiz_data, f, ensure_ascii=False, indent=4)

user_data = {}

@bot.message_handler(commands=['start'])
def start_quiz(message):
    try:
        with open('hist.json', 'r', encoding='utf-8') as file:
            quiz_data = json.load(file)
        
        questions = quiz_data['test']
        random.shuffle(questions)
        
        user_data[message.chat.id] = {
            'questions': questions[:5],
            'current_question': 0,
            'score': 0
        }
        
        ask_question(message.chat.id)
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

def ask_question(chat_id):
    user = user_data.get(chat_id)
    if not user or user['current_question'] >= len(user['questions']):
        finish_quiz(chat_id)
        return
    
    question = user['questions'][user['current_question']]['question']
    bot.send_message(chat_id, question)

@bot.message_handler(commands=['stop'])
def stop_quiz(message):
    if message.chat.id in user_data:
        del user_data[message.chat.id]
    bot.send_message(message.chat.id, "Тест прерван. Нажмите /start, чтобы начать заново.")

@bot.message_handler(func=lambda message: True)
def check_answer(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        return
    
    user = user_data[chat_id]
    if user['current_question'] >= len(user['questions']):
        return
    
    correct_answer = user['questions'][user['current_question']]['answer']
    user_answer = message.text.strip()
    
    if user_answer.lower() == correct_answer.lower():
        user['score'] += 1
        bot.send_message(chat_id, "Попал!")
    else:
        bot.send_message(chat_id, f"Мимо. Правильный ответ: {correct_answer}")
    
    user['current_question'] += 1
    ask_question(chat_id)

def finish_quiz(chat_id):
    user = user_data.get(chat_id)
    if not user:
        return
    
    total = len(user['questions'])
    score = user['score']
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/start'))
    
    bot.send_message(
        chat_id,
        f"Тест завершен!\nПравильных ответов: {score} из {total}",
        reply_markup=markup
    )
    
    del user_data[chat_id]

apihelper.delete_webhook(TOKEN)

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()