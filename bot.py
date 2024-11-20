import asyncio
from aiogram import Bot, Dispatcher

from handlers import bot_messages
from database import Database

from config_reader import config
from aiogram.utils.markdown import hbold
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

bot = Bot(config.bot_token.get_secret_value() , default = DefaultBotProperties(parse_mode=ParseMode.HTML))

async def main(bot):
    dp = Dispatcher()

    db = Database("products.db")
    await db.create_tables()
    

    dp.include_routers(
        bot_messages.router
    )

    
    asyncio.create_task(bot_messages.notify_price_changes())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    
if __name__ == "__main__":
    print("ready to work..")
    asyncio.run(main(bot))
