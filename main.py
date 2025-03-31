import asyncio
import os
from dotenv import load_dotenv

import random
import string
import datetime

from aiogram.filters import CommandStart, Command, StateFilter
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from buttons import btn, btn_back, btn_weather
from weather import get_weather_req, execute_weather
from asyncio import sleep


load_dotenv()
TOKEN = os.getenv('API_TOKEN')

storage = MemoryStorage()

dp = Dispatcher(storage=storage)


class StateAction(StatesGroup):
    main = State()
    paswd = State()
    wait_for_input = State()
    weather = State()
    waiting_for_city = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    keyboard_menu = types.ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True)
    await message.answer(f'Вітаю, {message.from_user.full_name}!\n'
                        'Я - бот, який допоможе тобі у повсякденному житті.\n'
                        'Наразі я маю декілька корисних функцій, які можуть тобі знадобитись.\n'
                        'Використовуй /help для отримання довідки та команд, або скористайся кнопками.',
                        reply_markup=keyboard_menu)
    await state.set_state(StateAction.main)


@dp.message(StateFilter(StateAction.main))
async def help_command(message: types.Message, state: FSMContext):
    if message.text == 'Кинути кубик':
        await message.answer('🎲 Кручу кубик...')
        await asyncio.sleep(2)
    
        result = await message.answer_dice()
        await asyncio.sleep(6)
        
        await message.answer(f'Вам випало число {result.dice.value}')
        
        
    elif message.text == 'Дізнатися поточну дату/час'.strip():
        await message.answer(f'⏳ Зараз {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        
    elif message.text == 'Згенерувати рандомний пароль'.strip():
        await message.answer(f'🔐 Введіть, будь ласка довжину паролю(1-9):')
        await state.set_state(StateAction.paswd)
        
    
    
@dp.message(StateAction.paswd)
async def generate_password(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('❌ Будь ласка, введіть число від 1 до 9!')
        return

    pass_len = int(message.text)  

    if pass_len < 1 or pass_len > 9:
        await message.answer('❌ Довжина паролю повинна бути від 1 до 9 символів!')
        return  

    random_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=pass_len))
    await message.answer(f'🔐 Ваш пароль: `{random_pass}`', parse_mode="Markdown")
    await state.set_state(StateAction.main)
     

    
        
@dp.message(Command('weather'))
async def get_weather(message: types.Message, state=FSMContext):
    await state.set_state(StateAction.weather)
    keyboard_menu = types.ReplyKeyboardMarkup(keyboard=btn_weather, resize_keyboard=True)
    await message.answer(f'{message.from_user.first_name}, тут ти можеш дізнатися погоду для твого міста,або вибрати із популярних.')
    await message.answer('Обери, будь ласка, дію...',reply_markup=keyboard_menu)


@dp.message(lambda message: message.text == 'Дізнатися погоду для свого міста')
async def get_weather_city(message: types.Message, state=FSMContext):
    await message.answer(f'{message.from_user.first_name}, введи своє місто, або вибери з популярних')
    await state.set_state(StateAction.waiting_for_city)
    

@dp.message(StateAction.waiting_for_city)
async def process_req_city(message: types.Message, state:FSMContext):
    await execute_weather(message)
    await state.set_state(StateAction.main)
 
  
async def main() -> None:
    bot = Bot(TOKEN)
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    asyncio.run(main())