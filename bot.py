from aiogram import Bot, Dispatcher, types, executor
from collections import defaultdict

bot = Bot(token="YOUR_TELEGRAM_BOT_TOKEN")
dp = Dispatcher(bot)

user_scores = defaultdict(int)

@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    await message.answer("Добро пожаловать в Crypto Clicker!\nНажимай кнопку ниже 👇", reply_markup=click_kb())

@dp.callback_query_handler(lambda c: c.data == 'click')
async def click_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_scores[user_id] += 1
    await callback.answer(f"💰 Токены: {user_scores[user_id]}")
    await callback.message.edit_reply_markup(reply_markup=click_kb())

def click_kb():
    buttons = [
        [types.InlineKeyboardButton("💸 Собрать токен", callback_data='click')]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

if __name__ == '__main__':
    executor.start_polling(dp)
