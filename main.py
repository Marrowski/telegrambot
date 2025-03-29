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

from buttons import btn, btn_menu
from asyncio import sleep


load_dotenv()
TOKEN = os.getenv('API_TOKEN')

dp = Dispatcher()


class StateAction(StatesGroup):
    action = State()
    dice = State()
    menu = State()
    pass_len = State()
    

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
    
    
@dp.message(lambda message: message.text == 'Кинути кубик'.strip().capitalize())
async def roll_dice(message: types.Message, state=FSMContext):
    keyboard_dice = types.ReplyKeyboardMarkup(keyboard=btn_menu, resize_keyboard=True)
    await state.set_state(StateAction.dice)
    
    await message.answer('Кручу кубик...')
    await asyncio.sleep(2)
    
    result = await message.answer_dice()
    await asyncio.sleep(6)
    
    await message.answer(f'Вам випало число {result.dice.value}')
    await message.answer(reply_markup=keyboard_dice)
    
    
@dp.message(lambda message: message.text == 'Дізнатися поточну дату/час'.strip().capitalize())
async def get_time(message: types.Message, state=FSMContext):
    await state.set_state(StateAction.menu)
    keyboard_menu = types.ReplyKeyboardMarkup(keyboard=btn_menu, resize_keyboard=True)
    
    
    await message.answer(f'Зараз {datetime.datetime.now()}')
    await message.answer(reply_markup=keyboard_menu)
    
    
@dp.message(lambda message: message.text == 'Згенерувати рандомний пароль'.capitalize().strip())
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
        
        
        
    
    
    
    

  
async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    asyncio.run(main())