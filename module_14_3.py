from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio
from config import *

# задачу 13_6 дополнить следующим:
# Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4".
# У всех кнопок назначьте callback_data="product_buying"
# Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию get_buying_list(message).
# Функция get_buying_list должна выводить надписи
# 'Название: Product<number> | Описание: описание <number> | Цена: <number * 100>' 4 раза.
# После каждой надписи выводите картинки к продуктам.
# В конце выведите ранее созданное Inline меню с надписью "Выберите продукт для покупки:".
# Callback хэндлер, который реагирует на текст "product_buying" и оборачивает функцию send_confirm_message(call).
# Функция send_confirm_message, присылает сообщение "Вы успешно приобрели продукт!"

bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

# В главную (обычную) клавиатуру меню добавьте кнопку "Купить".
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


inline_menu_catalog = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Снотворное", callback_data='product_buying'),
         InlineKeyboardButton(text="Успокоитель", callback_data='product_buying'),
         InlineKeyboardButton(text="Усилитель", callback_data='product_buying'),
         InlineKeyboardButton(text="Умножитель", callback_data='product_buying')]
    ], resize_keyboard=True)


def calories_calculate(data):
    calories_for_male = 10 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) + 5
    calories_for_female = 10 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) - 161
    return calories_for_male, calories_for_female


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# картинки к продуктам возьмем сразу из сети
list_img = ['https://www.google.com/imgres?q=fallout%20png%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B5%D1%82%D0%BA%D0%B8&imgurl=https%3A%2F%2Fstatic.wikia.nocookie.net%2Ffallout%2Fimages%2F6%2F68%2FFO4_Buffout.png%2Frevision%2Flatest%3Fcb%3D20220325191931%26path-prefix%3Dru&imgrefurl=https%3A%2F%2Ffallout.fandom.com%2Fru%2Fwiki%2F%25D0%2591%25D0%25B0%25D1%2584%25D1%2584%25D0%25B0%25D1%2583%25D1%2582_(Fallout_4)&docid=ucUrotmCyUGDpM&tbnid=4uQKGZrLE2RgUM&vet=12ahUKEwjhyKmE79aJAxUMLhAIHXhiDg4QM3oECBkQAA..i&w=652&h=652&hcb=2&ved=2ahUKEwjhyKmE79aJAxUMLhAIHXhiDg4QM3oECBkQAA',
            'https://www.google.com/imgres?q=fallout%20png%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B5%D1%82%D0%BA%D0%B8&imgurl=https%3A%2F%2Fw7.pngwing.com%2Fpngs%2F339%2F690%2Fpng-transparent-fallout-new-vegas-fallout-3-fallout-4-video-game-antitank-mine-video-game-first-aid-supplies-first-aid-kits-thumbnail.png&imgrefurl=https%3A%2F%2Fwww.pngwing.com%2Fru%2Ffree-png-iitmj&docid=C1MHPCNXjAGiOM&tbnid=oMbMcTOPKcF3-M&vet=12ahUKEwjhyKmE79aJAxUMLhAIHXhiDg4QM3oECH8QAA..i&w=360&h=374&hcb=2&itg=1&ved=2ahUKEwjhyKmE79aJAxUMLhAIHXhiDg4QM3oECH8QAA',
            'https://www.google.com/imgres?q=fallout%20png%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B5%D1%82%D0%BA%D0%B8&imgurl=https%3A%2F%2Fstatic.wikia.nocookie.net%2Ffallout%2Fimages%2F7%2F73%2FFallout4_Psycho.png%2Frevision%2Flatest%3Fcb%3D20220325192507%26path-prefix%3Dru&imgrefurl=https%3A%2F%2Ffallout.fandom.com%2Fru%2Fwiki%2F%25D0%259F%25D1%2581%25D0%25B8%25D1%2585%25D0%25BE-%25D1%2582%25D0%25B0%25D1%2582%25D1%258B&docid=06NQhpOmYchwSM&tbnid=MMK4mW7zFFLz-M&vet=12ahUKEwjhyKmE79aJAxUMLhAIHXhiDg4QM3oECBYQAA..i&w=765&h=765&hcb=2&ved=2ahUKEwjhyKmE79aJAxUMLhAIHXhiDg4QM3oECBYQAA',
            'https://www.google.com/imgres?q=fallout%20png%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B5%D1%82%D0%BA%D0%B8&imgurl=https%3A%2F%2Fgs11.ru%2Fstorage%2Ffallout-4%2Ffallout4-mentats.png&imgrefurl=https%3A%2F%2Fgs11.ru%2Ffallout-4%2Fpredmety%2Fapelsinovye-mentaty&docid=LettbrlhfnGGlM&tbnid=cZxJGoySuDsNLM&vet=12ahUKEwjhyKmE79aJAxUMLhAIHXhiDg4QM3oECHcQAA..i&w=794&h=567&hcb=2&itg=1&ved=2ahUKEwjhyKmE79aJAxUMLhAIHXhiDg4QM3oECHcQAA']

list_name_product = ["Снотворное", "Успокоитель", "Усилитель", "Умножитель"]

@dp.message_handler(text=["Купить"])
async def get_buying_list(message):
    for num in range(1, 5):
        await message.answer(f'Название: {list_name_product[num-1]}{num} | Описание: описание {num} | Цена: {num * 100}')
    # with open("","rb") as img:
    #    await message.answer_photo(img)
        await message.answer_photo(list_img[num-1])
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


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer(f"Ваш возраст: {data['age']}. Укажите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer(f"Ваш рост: {data['growth']}, Укажите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories_for_male, calories_for_female = calories_calculate(data)
    await message.answer(f"Норма калории для мужчин: {calories_for_male}\n"
                         f"Норма калории для женщин: {calories_for_female}")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
