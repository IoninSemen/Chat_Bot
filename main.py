import logging
import asyncio
import sqlite3
from config import API_TOKEN
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.markdown import text
from aiogram.client.default import DefaultBotProperties

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота с использованием DefaultBotProperties
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT
)
""")
conn.commit()

# Обработка команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот, который может вывести теги всех пользователей чата. Используй команду /tags.")

async def save_user(user_id: int, username: str):
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()

@dp.message(Command("tags"))
async def cmd_tags(message: types.Message):
    if message.chat.type in ["group", "supergroup"]:
        cursor.execute("SELECT username FROM users WHERE username IS NOT NULL")
        users = cursor.fetchall()

        tags = [f"@{user[0]}" for user in users]

        if tags:
            await message.answer("Теги всех пользователей, которые писали в чате:\n" + "\n".join(tags))
        else:
            await message.answer("Пока никто не писал в чате.")
    else:
        await message.answer("Эта команда работает только в групповых чатах.")

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    if username:
        await save_user(user_id, username)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())