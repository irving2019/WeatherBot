import telebot
import json
import requests
import datetime

from config import TOKEN, API

bot = telebot.TeleBot(TOKEN, parse_mode=None)
HELLO = "Добрый день, укажите город для получения информации о погоде"


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, HELLO)


@bot.message_handler(content_types=["text"])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    data = json.loads(res.text)
    days = datetime.datetime.now()

    txt = f'''
    
    В городе {city} на данный момент\n 
    
    {days.day}.{days.month}.{days.year} в {days.hour}:{days.minute}:{days.second}
    
    Температура: {data["main"]["temp"]}°C
    При скорости ветра: {data["wind"]["speed"]}м/с
    Чувствуется как: {data["main"]["feels_like"]}°C
    Влажность: {data["main"]["humidity"]}%
    Облачность: {data["clouds"]["all"]}%
    '''

    bot.reply_to(message, txt)



bot.polling(none_stop=True)