from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.client.session import aiohttp
from aiogram.types import TelegramObject
from pydantic import AnyHttpUrl


class GPTMiddleware(BaseMiddleware):
    def __init__(self, base_url: AnyHttpUrl):
        super().__init__()
        self.base_url = base_url
        self.headers = {'accept': 'application/json'}

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with aiohttp.ClientSession(base_url=self.base_url, headers=self.headers, trust_env=True, ) as session:
            data["session"] = session
            return await handler(event, data)
