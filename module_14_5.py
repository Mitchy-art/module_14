from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import get_all_products
from crud_functions_14_5 import *

api = '7783483077:AAHzY1BOlciBVZn47bkB8ypltBNBauBCmhw'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
button4 = KeyboardButton(text='Регистрация')
kb.add(button1, button2, button3, button4)

Inkb2 = InlineKeyboardMarkup()
button5 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
button6 = InlineKeyboardButton(text="Product2", callback_data="product_buying")
button7 = InlineKeyboardButton(text="Product3", callback_data="product_buying")
button8 = InlineKeyboardButton(text="Product4", callback_data="product_buying")
Inkb2.add(button5, button6, button7, button8)

Inkb = InlineKeyboardMarkup()
button9 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button10 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
Inkb.add(button9, button10)


@dp.message_handler(commands=['start'])
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.reply('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=Inkb)


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    products = get_all_products()
    number = 1
    for product in products:
        title = product[1]
        description = product[2]
        price = product[3]
        await message.answer(f'Название: {title} | Описание: {description} | Цена: {price}')
        picture = f'picture/vit_{product[0]}.jpg'
        with open(picture, 'rb') as img:
            await message.answer_photo(img)
            number += 1
    await message.answer("Выберите продукт для покупки:", reply_markup=Inkb2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    data = await state.get_data()
    name = is_included(data['username'])
    if name is True:
        if name is True:
            await state.update_data(username=message.text)
            await message.answer("Введите свой email:")
            await RegistrationState.email.set()
        else:
            await message.answer("Пользователь существует, введите другое имя")
            await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer('Вы прошли регистрацию')
    await state.finish()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    print('Введите свой возраст:')
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    weight = int(data['weight'])
    growth = int(data['growth'])
    age = int(data['age'])
    calory = 10 * weight + 6, 25 * growth - 5 * age - 161
    await message.answer(f'Ваша норма каллорий равна {calory}')
    await state.finish()


@dp.message_handler()
async def all_message(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
