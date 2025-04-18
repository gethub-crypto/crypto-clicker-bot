import os
import threading
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from collections import defaultdict
from flask import Flask

# Flask-заглушка для Render
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'

def run_web():
    app.run(host='0.0.0.0', port=10000)

# Telegram Bot
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)
user_scores = defaultdict(int)

def click_kb():
    buttons = [
        [types.InlineKeyboardButton("💸 Собрать токен", callback_data='click')]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    await message.answer("Добро пожаловать в Crypto Clicker!\nНажимай кнопку ниже 👇", reply_markup=click_kb())

@dp.callback_query_handler(lambda c: c.data == 'click')
async def click_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_scores[user_id] += 1
    await callback.answer(f"💰 Токены: {user_scores[user_id]}")
    await callback.message.edit_reply_markup(reply_markup=click_kb())

if __name__ == '__main__':
    threading.Thread(target=run_web).start()
    executor.start_polling(dp, skip_updates=True)
    
