from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from data.database import Database
from keyboards.reply import main_menu

router = Router()
db = Database("data/products.db")

@router.message(CommandStart())
async def start_command(message: Message):

    if message.from_user.id not in await db.table_exists():
        await db.create_user_table(message.from_user.id)
        await message.answer(
            "Привет! Я помогу отслеживать цены на товары.\n"
            "Используйте команды:\n"
            "/add \'ссылкa\' — добавить товар\n"
            "/mylist — посмотреть отслеживаемые товары\n"
            "/remove \'ID\' — удалить товар",
            reply_markup = main_menu
        )
    else: 
        await message.answer(
            "Привет! Я помогу отслеживать цены на товары.\n"
            "Используйте команды:\n"
            "/add \'ссылкa\' — добавить товар\n"
            "/mylist — посмотреть отслеживаемые товары\n"
            "/remove \'ID\' — удалить товар",
            reply_markup = main_menu
        )