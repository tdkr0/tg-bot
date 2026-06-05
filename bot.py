import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "BOT_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Курс валют")],
            [KeyboardButton(text="📋 Мои услуги")],
            [KeyboardButton(text="📞 Контакт")],
        ],
        resize_keyboard=True
    )
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я демо-бот. Выбери что тебя интересует:",
        reply_markup=keyboard
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Доступные команды:\n"
        "/start — начать\n"
        "/help — помощь"
    )
@dp.message(lambda m: m.text == "💰 Курс валют")
async def show_rates(message: types.Message):
    import requests
    from xml.etree import ElementTree as ET
    
    response = requests.get(
        "https://www.cbr.ru/scripts/XML_daily.asp",
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    response.encoding = 'windows-1251'
    root = ET.fromstring(response.text)
    
    rates = {}
    for valute in root.findall('Valute'):
        code = valute.find('CharCode').text
        if code in {'USD', 'EUR', 'CNY'}:
            value = float(valute.find('Value').text.replace(',', '.'))
            nominal = int(valute.find('Nominal').text)
            rates[code] = round(value / nominal, 2)
    
    text = "💱 Курсы ЦБ РФ сегодня:\n\n"
    text += f"🇺🇸 USD: {rates.get('USD', '—')} ₽\n"
    text += f"🇪🇺 EUR: {rates.get('EUR', '—')} ₽\n"
    text += f"🇨🇳 CNY: {rates.get('CNY', '—')} ₽"
    
    await message.answer(text)


@dp.message(lambda m: m.text == "📋 Мои услуги")
async def show_services(message: types.Message):
    await message.answer(
        "🛠 Мои услуги:\n\n"
        "• Парсинг данных с сайтов\n"
        "• Автоматизация на Python\n"
        "• Telegram-боты\n\n"
        "👉 kwork.ru/user/nassa4542"
    )


@dp.message(lambda m: m.text == "📞 Контакт")
async def show_contact(message: types.Message):
    await message.answer(
        "📬 Связаться со мной:\n\n"
        "Kwork: kwork.ru/user/nassa4542\n"
        "Telegram: @tdkr0"
    )


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())