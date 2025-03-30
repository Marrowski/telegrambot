import requests
from aiogram.types import Message
from aiogram import types
import os

from dotenv import load_dotenv

load_dotenv()

async def get_weather_req(city: str):
    global response
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params={'q': city, 'lang': 'ua', 
                                                                                            'APPID': os.getenv('API_TOKEN_WEATHER')})
        return response.json()
    except ValueError:
        return ('Місто не знайдено. Спробуй ще раз.')
        
        
async def execute_weather(message: types.Message):
    city = message.text
    data = await get_weather_req(city)
    try:
        main = data.get('main', {})
        wind = data.get('wind', {})
        
        temp = round(main.get('temp', 0) - 273.15, 2)
        temp_min = round(main.get("temp_min", 0) - 273.15, 2)
        temp_max = round(main.get("temp_max", 0) - 273.15, 2)
        wind_speed = round(wind.get("speed", 0), 2)
        
    except requests.exceptions.RequestException:
        await message.answer(f'Помилка отримання погоди! Код {response.status_code}')
    
    else:
        await message.answer (f'Погода у {city}:\n'
                             f'Температура {temp}°C\n'
                             f'Мінімальна температура {temp_min}°C\n'
                             f'Максимальна температура {temp_max}°C\n'
                             f'Швидкість вітру: {wind_speed} м/с')
        
        