import asyncio
from aiogram import Bot, Dispatcher

from handlers import commands, fsm_commands, messages, start

from config_reader import config
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

bot = Bot(config.bot_token.get_secret_value() , default = DefaultBotProperties(parse_mode=ParseMode.HTML))

async def main(bot):
    dp = Dispatcher()
    
    dp.include_routers(
        commands.router,
        start.router,
        fsm_commands.router,
        messages.router
    )

    asyncio.create_task(commands.notify_price_changes())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    
if __name__ == "__main__":
    print("ready to work..")
    asyncio.run(main(bot))
