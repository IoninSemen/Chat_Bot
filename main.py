import logging
import asyncio
from config import API_TOKEN
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import text
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота с использованием DefaultBotProperties
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)  # Установка HTML-парсера по умолчанию
)
dp = Dispatcher()

# Обработка команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создание клавиатуры
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Привет"))
    builder.add(KeyboardButton(text="Помощь"))
    builder.adjust(2)  # Расположение кнопок в 2 колонки

    await message.answer(
        text("Привет! Я твой первый бот на **aiogram 3.x**!"),
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

# Обработка текстовых сообщений
@dp.message(lambda message: message.text == "Привет")
async def greet(message: types.Message):
    await message.answer("Привет! Как дела?")

@dp.message(lambda message: message.text == "Помощь")
async def help_command(message: types.Message):
    await message.answer("Чем могу помочь?")

# Обработка всех остальных сообщений
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Вы написали: {message.text}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())  # Запуск асинхронной функции main()