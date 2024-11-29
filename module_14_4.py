from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio
from config import *
import re
from crud_functions import initiate_db, get_all_products

product = get_all_products()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Рассчитать"),
            KeyboardButton(text="Информация")
        ],
        [KeyboardButton(text="Купить")]
    ], resize_keyboard=True)

inline_menu = InlineKeyboardMarkup(resize_keyboard=True)
inl_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inl_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_menu.row(inl_button1, inl_button2)

inline_menu_catalog = InlineKeyboardMarkup(resize_keyboard=True)
for button in range(len(product)):
    inline_menu_catalog.insert(InlineKeyboardButton(text=product[button][0], callback_data='product_buying'))


def calories_calculate(data):
    calories_for_male = 10 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) + 5
    calories_for_female = 10 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) - 161
    return calories_for_male, calories_for_female


@dp.message_handler(text=["Купить"])
async def get_buying_list(message):
    await message.answer_photo(
        'https://www.google.com/imgres?q=png%20%D1%84%D1%80%D1%83%D0%BA%D1%82%20%D0%BE%D0%B2%D0%BE%D1%89&imgurl=https%3A%2F%2Fpng.klev.club%2Fuploads%2Fposts%2F2024-03%2Fthumbs%2Fpng-klev-club-p-frukti-ovoshchi-png-22.png&imgrefurl=https%3A%2F%2Fpng.klev.club%2F1348-frukty-ovoschi.html&docid=wWZcpjnK6hpPEM&tbnid=bpXdDPY5am4uzM&vet=12ahUKEwiA897V5NuJAxUxGxAIHalTBdAQM3oECB0QAA..i&w=600&h=360&hcb=2&ved=2ahUKEwiA897V5NuJAxUxGxAIHalTBdAQM3oECB0QAA')
    for unit in product:
        await message.answer(f"Название: {unit[0]} | Описание: {unit[1]} | Цена: {unit[2]}")
    # with open("","rb") as img:
    #    await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=inline_menu_catalog)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=start_menu)


@dp.message_handler(text=["Рассчитать"])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_menu)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес(кг)+6,25 x рост(см)–5 x возраст(г)–161\n'
                              '10 x вес(кг)+6,25 x рост(см)–5 x возраст(г)–5')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Укажите свой возраст:")
    await call.answer()
    await UserState.age.set()


str_warning = "Задавайте только целые числа"
age_growth_weight = dict()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()

    match = re.match(r'\d{1,3}', data['age'])
    if match is not None:
        age_growth_weight['age'] = int(match[0])
        await message.answer(f"Ваш возраст: {match[0]}. Укажите свой рост:")
        await UserState.growth.set()
    else:
        await message.answer(str_warning)


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()

    match = re.match(r'\d{1,3}', data['growth'])
    if match is not None:
        age_growth_weight['growth'] = int(match[0])
        await message.answer(f"Ваш рост: {match[0]}, Укажите свой вес:")
        await UserState.weight.set()
    else:
        await message.answer(str_warning)


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    match = re.match(r'\d{1,3}', data['weight'])
    if match is not None:
        await message.answer(f"Ваш вес: {match[0]}")
        age_growth_weight['weight'] = int(match[0])
        calories_for_male, calories_for_female = calories_calculate(age_growth_weight)
        await message.answer(f"Норма калории для мужчин: {calories_for_male}")
        await message.answer(f"Норма калории для женщин: {calories_for_female}")
        await state.finish()
    else:
        await message.answer(str_warning)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

