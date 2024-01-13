import telebot
import requests
import json

bot = telebot.TeleBot('YourBotToken From Bot_Father')
API = "ae12b3fe0b3973472139cbb2a14c8042"


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, рад тебя видеть! '
                                      f'Спасибо за то, что выбрал нашу службу погоды! '
                                      f'Напиши название города:')

@bot.message_handler(commands=['site'])
def site(message):
    bot.send_message(message.chat.id, f'https://vk.com/voldemarnif')

@bot.message_handler(commands=['telegram'])
def telegram(message):
    bot.send_message(message.chat.id, f'https://t.me/voldemarnif')

@bot.message_handler(commands=['github'])
def github(message):
    bot.send_message(message.chat.id, f'https://github.com/irving2019')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip()
    result = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if result.status_code == 200:
        data = json.loads(result.text)
        temperature = data['main']['temp']
        bot.reply_to(message, f'Сейчас в городе {city} {temperature} градусов')

        if temperature > 0:
            image = 'sun.jpg'
        else:
            image = 'snow.jpg'

        file = open('images/' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, 'Город указан не верно')



bot.polling(none_stop=True)
