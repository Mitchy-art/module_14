from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import get_all_products


api = '7783483077:AAHzY1BOlciBVZn47bkB8ypltBNBauBCmhw'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

menu = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
menu.add(button1, button2, button3)

Line_menu2 = InlineKeyboardMarkup()
button4 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
button5 = InlineKeyboardButton(text="Product2", callback_data="product_buying")
button6 = InlineKeyboardButton(text="Product3", callback_data="product_buying")
button7 = InlineKeyboardButton(text="Product4", callback_data="product_buying")
Line_menu2.add(button4, button5, button6, button7)

Line_menu = InlineKeyboardMarkup()
button8 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button9 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
Line_menu.add(button8, button9)


@dp.message_handler(commands=['start'])
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=menu)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=Line_menu)


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    products = get_all_products()
    number = 1
    for product in products:
        title, description,price = product
        await message.answer(f'Название: {title} | Описание: {description} | Цена: {price}')
        picture = f'picture/vit_{product[number]}.jpg'
        with open(picture, 'rb') as img:
            await message.answer_photo(img)
            number += 1
    await message.answer("Выберите продукт для покупки:", reply_markup=Line_menu2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    print('Введите свой возраст:')
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


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