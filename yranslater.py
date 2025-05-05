import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from googletrans import Translator

API_TOKEN = "7436585258:AAEKJpssHgxbIh5WwvAL2YvlAZCOL0v6Vwk"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
translator = Translator()

user_directions = {}

language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Русский → Турецкий")],
        [KeyboardButton(text="Турецкий → Русский")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите направление перевода"
)
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я переводчик между русским и турецким. Выберите направление:",
        reply_markup=language_keyboard
    )

@dp.message(lambda msg: msg.text in ["Русский → Турецкий", "Турецкий → Русский"])
async def choose_direction(message: types.Message):
    user_directions[message.from_user.id] = message.text
    await message.answer(f"Вы выбрали: {message.text}. Введите текст для перевода.")

@dp.message()
async def translate_text(message: types.Message):
    direction = user_directions.get(message.from_user.id)
    if not direction:
        await message.answer("Пожалуйста, выберите направление перевода.", reply_markup=language_keyboard)
        return

    src, dest = ("ru", "tr") if direction == "Русский → Турецкий" else ("tr", "ru")
    translated = translator.translate(message.text, src=src, dest=dest)
    await message.answer(f"Перевод:\n{translated.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
