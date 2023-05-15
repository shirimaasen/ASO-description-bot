import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web

from bot.handlers import comand, create_application, generate, menu
from bot.middlewares.gpt import GPTMiddleware
from bot.configreader import config


async def main():
    # Logging to stdout
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Creating bot and its dispatcher
    bot = Bot(token=config.bot_token, parse_mode="HTML")

    if config.redis_dsn:
        from aiogram.fsm.storage.redis import RedisStorage
        dp = Dispatcher(storage=RedisStorage.from_url(config.redis_dsn))

    else:
        from aiogram.fsm.storage.memory import MemoryStorage
        dp = Dispatcher(storage=MemoryStorage())

    # Register middlewares
    dp.message.middleware(GPTMiddleware(config.gpt_url))
    dp.callback_query.middleware(GPTMiddleware(config.gpt_url))

    dp.include_router(comand.router)
    dp.include_router(create_application.router)
    dp.include_router(generate.router)
    dp.include_router(menu.router)

    try:
        if not config.webhook_domain:
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        else:
            # Suppress aiohttp access log completely
            aiohttp_logger = logging.getLogger("aiohttp.access")
            aiohttp_logger.setLevel(logging.CRITICAL)
            # Setting webhook
            await bot.set_webhook(
                url=f"{config.webhook_domain}{config.webhook_path}",
                drop_pending_updates=True,
                allowed_updates=dp.resolve_used_update_types()
            )

            # Creating an aiohttp application
            app = web.Application()
            SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=config.webhook_path)
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, host=config.app_host, port=config.app_port)
            await site.start()

            # Running it forever
            await asyncio.Event().wait()
    finally:
        await bot.session.close()


asyncio.run(main())
