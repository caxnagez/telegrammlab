import telebot
import requests
from io import BytesIO
from urllib.parse import quote

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
KEY = 'd053f8e4-fb49-498a-8dbe-0ba34403c7c4'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне название места или адрес, и я пришлю тебе карту с этим местом.")

def generate_map_url(location, api_key):
    encoded_location = quote(location)
    url = f"https://static-maps.yandex.ru/1.x/?ll={location['lon']},{location['lat']}&size=600,400&z=15&l=map&pt={location['lon']},{location['lat']},pm2rdm&apikey={api_key}"
    return url

@bot.message_handler(func=lambda message: True)
def handle_location_request(message):
    try:
        geocoder_url = f"https://geocode-maps.yandex.ru/1.x/?apikey={KEY}&geocode={message.text}&format=json"
        response = requests.get(geocoder_url)
        response.raise_for_status()
        data = response.json()
        found = int(data['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found'])
        if found == 0:
            bot.reply_to(message, "Извините, ничего не найдено. Попробуйте уточнить запрос.")
            return
        geo_object = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        address = geo_object['metaDataProperty']['GeocoderMetaData']['text']
        pos = geo_object['Point']['pos'].split()
        location = {'lon': pos[0], 'lat': pos[1]}
        map_url = generate_map_url(location, KEY)
        map_response = requests.get(map_url)
        map_response.raise_for_status()
        bot.send_photo(
            message.chat.id,
            photo=BytesIO(map_response.content),
            caption=f"* {address}\nКоординаты: {location['lat']}, {location['lon']}",
            parse_mode='Markdown'
        )
        
    except requests.exceptions.HTTPError as http_err:
        bot.reply_to(message, f"Ошибка при обращении к сервису карт: {http_err}")
    except requests.exceptions.RequestException as req_err:
        bot.reply_to(message, f"Проблемы с подключением: {req_err}")
    except Exception as e:
        bot.reply_to(message, f"Произошла непредвиденная ошибка: {e}")

if __name__ == '__main__':
    bot.remove_webhook()
    print("Бот запущен...")
    bot.infinity_polling()