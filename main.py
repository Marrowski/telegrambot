import asyncio
import os
from dotenv import load_dotenv

import random
import string
import datetime

from aiogram.filters import CommandStart, Command
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from buttons import btn, btn_menu, btn_weather, btn_popular_city
from weather import get_weather_req, execute_weather
from asyncio import sleep


load_dotenv()
TOKEN = os.getenv('API_TOKEN')

dp = Dispatcher()


class StateAction(StatesGroup):
    action = State()
    dice = State()
    menu = State()
    pass_len = State()
    weather = State(),
    waiting_for_city = State()
    

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f'Вітаю, {message.from_user.full_name}\
        Я - бот, який допоможе тобі у повсякденному житті.\
        Наразі я маю декілька корисних функцій, які можуть тобі знадобитись\
        Використовуй /help для отримання довідки та команд.')
    

@dp.message(Command('help'))
async def help_command(message: types.Message, state: FSMContext):
    
    keyboard = types.ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True)
    
    await state.set_state(StateAction.action)
    await message.answer('Обери, будь ласка, дію', reply_markup=keyboard)
    
    
@dp.message(lambda message: message.text == 'Кинути кубик')
async def roll_dice(message: types.Message, state=FSMContext):
    keyboard_dice = types.ReplyKeyboardMarkup(keyboard=btn_menu, resize_keyboard=True)
    await state.set_state(StateAction.dice)
    
    await message.answer('Кручу кубик...')
    await asyncio.sleep(2)
    
    result = await message.answer_dice()
    await asyncio.sleep(6)
    
    await message.answer(f'Вам випало число {result.dice.value}')
    await message.answer(reply_markup=keyboard_dice)
    
    
@dp.message(lambda message: message.text == 'Дізнатися поточну дату/час')
async def get_time(message: types.Message, state=FSMContext):
    await state.set_state(StateAction.menu)
    keyboard_menu = types.ReplyKeyboardMarkup(keyboard=btn_menu, resize_keyboard=True)
    
    
    await message.answer(f'Зараз {datetime.datetime.now()}')
    await message.answer(reply_markup=keyboard_menu)
    
    
@dp.message(lambda message: message.text == 'Згенерувати рандомний пароль')
async def generate_password(message: types.Message, state=FSMContext):
    await message.answer(f'Введіть, будь ласка довжину паролю(1-9):')
    
    
@dp.message(lambda message: message.text.isdigit())
async def len_pass(message: types.Message, state=FSMContext):
    await state.set_state(StateAction.pass_len)
    pass_len = int(message.text)    
    random_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=pass_len))
    
    try:
        len(str(pass_len)) > 9 
    except Exception:
        await message.answer(f'Довжина паролю не може бути більше 9 символів!')
    else: 
        await message.answer(random_pass)
        

@dp.message(Command('weather'))
async def get_weather(message: types.Message, state=FSMContext):
    await state.set_state(StateAction.weather)
    keyboard_menu = types.ReplyKeyboardMarkup(keyboard=btn_weather, resize_keyboard=True)
    await message.answer(f'{message.from_user.first_name}, тут ти можеш дізнатися погоду для твого міста,або вибрати із популярних.')
    await message.answer(reply_markup=keyboard_menu)


@dp.message(lambda message: message.text == 'Дізнатися погоду для свого міста')
async def get_weather_city(message: types.Message, state=FSMContext):
    await message.answer(f'{message.from_user.first_name}, введи своє місто, або вибери з популярних')
    await state.set_state(StateAction.waiting_for_city)
    

@dp.message(StateAction.waiting_for_city)
async def process_req_city(message: types.Message, state:FSMContext):
    await execute_weather(message)
    await state.clear()
  
async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    asyncio.run(main())