import random
import string
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

from dotenv import load_dotenv 

load_dotenv()

# --- НАСТРОЙКИ ---
API_TOKEN = os.getenv('BOT_TOKEN')
DEPOSIT_BIG = 5000  # Цена для стола на 4-х
DEPOSIT_SMALL = 2000  # Цена для стола на 2-х
PAYMENT_URL = "https://your-payment-link.com" # Ссылка на оплату

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для генерации случайного кода
def generate_code(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Большой стол (на 4-х)", callback_data="table_big"))
    builder.row(types.InlineKeyboardButton(text="Маленький стол (на 2-х)", callback_data="table_small"))
    
    await message.answer(
        "Добро пожаловать! Какой столик вы хотите забронировать?",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data.startswith("table_"))
async def process_booking(callback: types.CallbackQuery):
    table_type = callback.data.split("_")[1]
    price = DEPOSIT_BIG if table_type == "big" else DEPOSIT_SMALL
    code = generate_code()
    
    text = (
        f"Вы выбрали {'большой' if table_type == 'big' else 'маленький'} столик.\n"
        f"Сумма депозита: **{price} руб.**\n\n"
        f"Для оплаты перейдите по ссылке ниже.\n"
        f"⚠️ **ВАЖНО:** В комментарии к платежу обязательно укажите этот код: `{code}`"
    )
    
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Оплатить депозит", url=PAYMENT_URL))
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
