import asyncio
import os
from dotenv import load_dotenv

from aiogram.filters import CommandStart, Command
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from buttons import btn, btn_dice

from asyncio import sleep

load_dotenv()

TOKEN = os.getenv('API_TOKEN')


dp = Dispatcher()


class StateAction(StatesGroup):
    action = State()
    dice = State()
    

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
    keyboard_dice = types.ReplyKeyboardMarkup(keyboard=btn_dice, resize_keyboard=True)
    await state.set_state(StateAction.dice)
    await message.answer('Обери максимальне число кубику(6, 12, 24):', reply_markup=keyboard_dice)
    

@dp.message(lambda message: message.text == '6')
async def comm_dice(message: types.Message):
    await message.answer('Кручу кубик...')
    asyncio.sleep(2)
    result = await message.answer_dice()
    await message.answer(f'Вам випало число {result}')
                 
  
async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())