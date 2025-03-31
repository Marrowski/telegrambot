from aiogram import Bot, Dispatcher, types

btn = [
        [
        types.KeyboardButton(text='Дізнатися поточну дату/час'),
        types.KeyboardButton(text='Кинути кубик'),
        types.KeyboardButton(text='Згенерувати рандомний пароль')
    ]
    ]

btn_back = [[
    types.KeyboardButton(text='Назад до меню')
]]

btn_weather = [[
    types.KeyboardButton(text='Дізнатися погоду для свого міста'),
    types.KeyboardButton(text='Популярні міста')
]]

btn_popular_city = [[
    types.KeyboardButton(text='Київ'),
    types.KeyboardButton(text='Нью Йорк'),
    types.KeyboardButton(text='Париж')
]]

btn_main = [[
    types.KeyboardButton(text='Меню'),
    types.KeyboardButton(text='Погода')
]]


