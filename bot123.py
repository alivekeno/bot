import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command


TOKEN = "7620703873:AAH88qgsCJMg-TMsT6kZDiBwCNYEiTC_Lx0"
GEMINI_API_KEY = "AIzaSyCuAlmNOfiMQfVvRYViMaqmyDi0REf89C0"
MODEL_NAME = "gemini-2.0-pro-exp-02-05"

HELP_COMMAND = """
/help - список команд
/start - начать работу с ботом
/ask - задать вопрос ИИ
"""

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настройка API Gemini
genai.configure(api_key=GEMINI_API_KEY)


async def on_startup():
    print("Бот запущен!")


async def query_llm(user_message: str) -> str:
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(user_message)
        return response.text.strip()
    except Exception as e:
        return f"Ошибка при запросе к ИИ: {e}"


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(HELP_COMMAND)


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer('салам пополам!',)


@dp.message()
async def ask_command(message: Message):
    response = await query_llm(message.text)
    await message.answer(response)


async def main():
    await on_startup()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())