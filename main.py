import logging
from aiogram import Bot, Dispatcher, executor, types

from oxfordLookup import getDefinitions
from googletrans import Translator
translator = Translator()

API_TOKEN = '5206641265:AAGZr0yA9fNT153QoF6B68_kC3la3rla1MY'
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Salom!\nMen English va Uzbek tarjimon!🤖\nMenga Uzbekcha yoki Englishcha so'z yozing.")

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(" admin https://t.me/sasomiddinov bilan boglaning")

@dp.message_handler()
async def tarjimon(message: types.Message):
    print(message)
    lang = translator.detect(message.text).lang
    if len(message.text.split()) > 2:
        dest = 'ru' if lang == 'en' else 'en'
        await message.reply(translator.translate(message.text, dest).text)
    else:
        if lang=='en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text, dest='en').text

        lookup = getDefinitions(word_id)
        if lookup:
            await message.reply(f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])
        else:
            await message.reply("Bunday so'z topilmadi😔")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)