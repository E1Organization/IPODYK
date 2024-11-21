from aiogram import Router
from aiogram.types import Message

router = Router()

#тригерится на мусор
@router.message()
async def echo(message: Message):
    await message.reply(
        "⚠️Неизвестная команда⚠️\n"
        "/add \'ссылкa\' — добавить товар\n"
        "/mylist — посмотреть отслеживаемые товары\n"
        "/remove \'ID\' — удалить товар"
    )