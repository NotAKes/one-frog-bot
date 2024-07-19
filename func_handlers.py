from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, types
from aiogram import Router
import datetime
from parseit import parser
from config import cities

router = Router()


@router.message(F.text == "О боте")
async def github_func(message: types.Message):
    url_buttons = InlineKeyboardBuilder()
    url_buttons.row(
        types.InlineKeyboardButton(text='Сообщить об ошибке', url='https://github.com/NotAKes/one-frog-bot_bot/issues'))
    url_buttons.row(types.InlineKeyboardButton(text='Github проекта', url='https://github.com/NotAKes/one-frog-bot'))
    url_buttons.row(types.InlineKeyboardButton(text='Написать разработчику', url='t.me/notakees'))
    await message.answer('Выберите ссылку🔗', reply_markup=url_buttons.as_markup(), )


@router.message(F.text == "Москва")
async def place_msk_func(message: types.Message):
    global place
    place = ''
    place = cities["MSK"]
    await choosetime_func(message)


@router.message(F.text == "Орехово-Зуево")
async def place_oz_func(message: types.Message):
    global place
    place = ''
    place = cities["OZ"]
    await choosetime_func(message)


@router.message(F.text == "Астана")
async def place_ast_func(message: types.Message):
    global place
    place = ''
    place = cities["AST"]
    await choosetime_func(message)


@router.message(F.text == "С.Петербург")
async def place_spb_func(message: types.Message):
    global place
    place = ''
    place = cities["SPB"]
    await choosetime_func(message)


@router.message(F.text == "Минск")
async def place_minsk_func(message: types.Message):
    global place
    place = ''
    place = cities["MINSK"]
    await choosetime_func(message)


@router.message(F.text == "Сегодня🕓")
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


@router.message(F.text == "Завтра🕓")
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


@router.message(F.text == "3 дня🗓")
async def threedays(message: types.Message):
    if place:
        for date in range(2, 5):
            await message.answer(
                f" <b>Прогноз погоды на {datetime.datetime.strftime((datetime.datetime.now() + datetime.timedelta(days=date - 1)).date(), "%d.%m.%Y")}</b> \n"
                f"\n{parser(date, list_=place)}", parse_mode="html")
    else:
        await message.reply("Место не выбрано")
        await choose_place(message)


@router.message(F.text == "Неделя🗓")
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
@router.message(Command("menu"))
async def call_menu(message: types.Message):
    await menu(message)


# Команда /place
@router.message(Command("place"))
async def call_place(message: types.Message):
    await choose_place(message)


# Команда /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет!👋 Я бот, определяющий погоду:")
    await menu(message)


@router.message(F.text == "Прогноз погоды")
async def choose_place(message: types.Message):
    inp = [
        [
            types.KeyboardButton(text="Москва"),
            types.KeyboardButton(text="С.Петербург"),
            types.KeyboardButton(text="Орехово-Зуево"),
            types.KeyboardButton(text="Астана"),
            types.KeyboardButton(text="Минск")
        ],

    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=inp,
        resize_keyboard=True,
        input_field_placeholder="Выберите регион из списка доступных"
    )
    await message.answer(
        f"Выберите регион из списка доступных:\n\n 🇷🇺 Москва, С.Петербург, Орехово-Зуево\n 🇧🇾 Минск \n 🇰🇿 Астана \n {"-" * 40} \nДля выбора напишите название города или нажмите на кнопку",
        reply_markup=keyboard)


@router.message()
async def unknown_message(message: types.Message):
    await message.answer(
        "Похоже, я не знаю эту команду. Используйте /menu. Если вы думаете что произошла ошибка, то напишите @notakees")


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


async def menu(message: types.Message):
    inp = [
        [
            types.KeyboardButton(text="О боте"),
            types.KeyboardButton(text="Прогноз погоды")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=inp,
        resize_keyboard=True,
        input_field_placeholder="Выберите функцию"
    )
    await message.answer("Выберите функцию⚙️", reply_markup=keyboard)
