import logging
import sys
import asyncio
import datetime
import math

import requests

from config import TOKEN, API

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

HELP = '''
/help - справка

Просто отправь название своего города и получишь текущую погоду
в своём городе'''

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_heandler(message: Message) -> None:
    await message.answer(HELP)


@dp.message()
async def get_weather(message: Message) -> None:
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5"
                                f"/weather?q=city&lang=ru&units=metric&appid={API}")
        data = response.json()
        city = data["name"]  # получение города от пользователям
        current_temperature = data["main"]["temp"]  # получение текущей температуры
        humidity = data["main"]["humidity"]  # Влажность
        pressure = data["main"]["pressure"]  # Давление
        wind = data["wind"]["speed"]  # Скорость ветра

        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        length_of_the_day = (datetime.datetime.fromtimestamp(data["sys"]["sunset"])
                             - datetime.datetime.fromtimestamp(data["sys"]["sunrise"]))

    except:
        await message.reply("Проверьте название города")

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    weather_description = get_weather.data["weather"][0]["main"]

    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = "Не верный запрос, укажите корректное название города"

    await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
     f"Погода в городе: {city}\nТемпература: {current_temperature}°C {wd}\n"
     f"Влажность: {humidity}%\nДавление: {math.ceil(pressure/1.333)} мм.рт.ст\nВетер: {wind} м/с \n"
     f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
     f"Хорошего дня!"
)


@dp.message()
async def main() -> None:
    bot = Bot(TOKEN)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main)