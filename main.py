import logging

from aiogram import Bot, Dispatcher, executor, types
from pyowm import OWM

from pyowm.utils.config import get_default_config

owm = OWM('YOU TOKEN')
mgr = owm.weather_manager()
config_dict = get_default_config()
config_dict['language'] = 'ru'


API_TOKEN = 'YOU TOKEN'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=['text'])
async def send_echo(message: types.Message):
    observation = mgr.weather_at_place(message.text)
    w = observation.weather
    temp = w.temperature('celsius')['temp']
    status = w.detailed_status
    await message.reply('В городе ' + message.text + ' сейчас ' + status + '\n')
    await message.answer('Температура сейчас в районе ' + str(temp) + '\n\n')
    if temp < 10:
        await message.answer('Сейчас ппц как холодно, одевайся как танк!')
    elif temp < 20:
        await message.answer('Сейчас холодно оденься потеплее.')
    else:
        await message.answer('Температура норм, одевай, что угодно.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
