from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
import asyncio
import logging
import datetime
import os
from dotenv import load_dotenv, find_dotenv
from parseit import parser
from config import cities

# логгирование
logging.basicConfig(level=logging.INFO, filename="logs.log", filemode="w",
                    format="[%(asctime)s] %(levelname)s %(message)s")

# переменные места и времени
date = ''

MOSCOW = cities[0]
MINSK = cities[1]
SPB = cities[2]
AST = cities[3]

place = ''

# начало логики бота
load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


@dp.message(F.text == "Github проекта")
async def github_func(message: types.Message):
    await message.answer("https://github.com/NotAKes/AOWBee_bot")


@dp.message(F.text == "Москва 🇷🇺")
async def timeMSK_func(message: types.Message):
    global place
    place = ''
    place = MOSCOW
    await choosetime_func(message)


@dp.message(F.text == "Астана 🇰🇿")
async def timeAST_func(message: types.Message):
    global place
    place = ''
    place = AST
    await choosetime_func(message)


@dp.message(F.text == "С.Петербург 🇷🇺")
async def timeSPB_func(message: types.Message):
    global place
    place = ''
    place = SPB
    await choosetime_func(message)


@dp.message(F.text == "Минск 🇧🇾")
async def timeMIN_func(message: types.Message):
    global place
    place = ''
    place = MINSK
    await choosetime_func(message)


@dp.message(F.text == "Сегодня🕓")
async def today(message: types.Message):
    global date
    date = 1
    if place:
        await message.reply(
            f" <b>Прогноз погоды на {datetime.datetime.strftime((datetime.datetime.now()).date(), "%d.%m.%Y")}\n</b>"
            f"\n"
            f"{parser(date, list_=place)}", parse_mode="html")
    else:
        await message.reply("Место не выбрано")
        await choose_place(message)


@dp.message(F.text == "Завтра🕓")
async def yesterday(message: types.Message):
    global date
    date = 2
    if place:
        await message.reply(
            f"<b>Прогноз погоды на {datetime.datetime.strftime((datetime.datetime.now() + datetime.timedelta(days=1)).date(), "%d.%m.%Y")}</b>\n"
            f"\n"
            f"{parser(date, list_=place)}", parse_mode="html")
    else:
        await message.reply("Место не выбрано")
        await choose_place(message)


@dp.message(F.text == "3 дня🗓")
async def threedays(message: types.Message):
    if place:
        for date in range(2, 5):
            await message.answer(
                f" <b>Прогноз погоды на {datetime.datetime.strftime((datetime.datetime.now() + datetime.timedelta(days=date - 1)).date(), "%d.%m.%Y")}</b> \n"
                f"\n{parser(date, list_=place)}", parse_mode="html")
    else:
        await message.reply("Место не выбрано")
        await choose_place(message)


@dp.message(F.text == "Неделя🗓")
async def week(message: types.Message):
    if place:
        for date in range(2, 9):
            await message.answer(
                f" <b>Прогноз погоды на {datetime.datetime.strftime((datetime.datetime.now() + datetime.timedelta(days=date - 1)).date(), "%d.%m.%Y")}</b> \n"
                f"\n"
                f"{parser(date, list_=place)}", parse_mode="html")
    else:
        await message.reply("Место не выбрано")
        await choose_place(message)


# Команда /menu
@dp.message(Command("menu"))
async def call_menu(message: types.Message):
    await menu(message)


# Команда /place
@dp.message(Command("place"))
async def call_place(message: types.Message):
    await choose_place(message)


# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет!👋 Я бот, определяющий погоду:")
    await menu(message)


async def menu(message: types.Message):
    inp = [
        [
            types.KeyboardButton(text="Github проекта"),
            types.KeyboardButton(text="Прогноз погоды")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=inp,
        resize_keyboard=True,
        input_field_placeholder="Выберите функцию"
    )
    await message.answer("Выберите функцию⚙️", reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)


@dp.message(F.text == "Прогноз погоды")
async def choose_place(message: types.Message):
    inp = [
        [
            types.KeyboardButton(text="Москва 🇷🇺"),
            types.KeyboardButton(text="Минск 🇧🇾"),
            types.KeyboardButton(text="С.Петербург 🇷🇺"),
            types.KeyboardButton(text="Астана 🇰🇿")
        ],

    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=inp,
        resize_keyboard=True,
        input_field_placeholder="Выберите регион из списка доступных"
    )
    await message.answer("Выберите регион из списка доступных:", reply_markup=keyboard)


async def choosetime_func(message: types.Message):
    inp = [
        [
            types.KeyboardButton(text="Сегодня🕓"),
            types.KeyboardButton(text="Завтра🕓"),
            types.KeyboardButton(text="3 дня🗓"),
            types.KeyboardButton(text="Неделя🗓")
        ],

    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=inp,
        resize_keyboard=True,
        input_field_placeholder="Выберите время предсказания..."
    )
    await message.answer("Выберите время🕓", reply_markup=keyboard)


if __name__ == "__main__":
    asyncio.run(main())
