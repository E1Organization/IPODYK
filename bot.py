import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
from database import Database
from price_tracker import PriceTracker

# Ваш токен Telegram-бота
TOKEN = "7648782067:AAEDXelkWKzNj4nJQRcBAKSWBTnlpsqgNKY"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Инициализация базы данных и трекера цен
db = Database("products.db")
price_tracker = PriceTracker(db)


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Привет! Я помогу отслеживать цены на товары.\n"
        "Используйте команды:\n"
        "/add <ссылка> — добавить товар\n"
        "/list — посмотреть отслеживаемые товары\n"
        "/remove <ID> — удалить товар"
    )


@dp.message(Command("add"))
async def add_product(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Пожалуйста, отправьте команду в формате /add <ссылка на товар>")
        return
    url = args[1]
    product_id = await db.add_product(url, message.from_user.id)
    if product_id:
        await message.reply(f"✅ Товар добавлен для отслеживания. ID: {hbold(product_id)}")
    else:
        await message.reply("❌ Не удалось добавить товар. Проверьте ссылку и попробуйте снова.")


@dp.message(Command("list"))
async def list_products(message: Message):
    products = await db.get_user_products(message.from_user.id)
    if not products:
        await message.reply("📋 Ваш список отслеживаемых товаров пуст.")
    else:
        response = "📋 Ваши отслеживаемые товары:\n"
        for p in products:
            response += f"ID: {hbold(p['id'])}, URL: {p['url']}, Текущая цена: {hbold(p['price'])} ₽\n"
        await message.reply(response)


@dp.message(Command("remove"))
async def remove_product(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Пожалуйста, отправьте команду в формате /remove <ID товара>")
        return
    product_id = int(args[1])
    if await db.remove_product(product_id, message.from_user.id):
        await message.reply(f"✅ Товар с ID {hbold(product_id)} удален из отслеживания.")
    else:
        await message.reply("❌ Не удалось удалить товар. Проверьте ID и попробуйте снова.")


async def notify_price_changes():
    while True:
        changes = await price_tracker.check_prices()
        for change in changes:
            user_id = change['user_id']
            message = (
                f"⚠️ Цена на товар изменилась!\n"
                f"{hbold('Товар')}: {change['url']}\n"
                f"Старая цена: {hbold(change['old_price'])} ₽, Новая цена: {hbold(change['new_price'])} ₽\n"
                f"Изменение: {hbold(change['change_percent'])}%"
            )
            await bot.send_message(user_id, message)
        await asyncio.sleep(3600)  # Проверять каждые 60 минут


async def main():
    # Фоновая задача уведомлений
    asyncio.create_task(notify_price_changes())

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
