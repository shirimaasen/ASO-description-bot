from aiogram import Router

from aiogram.types import CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from aiohttp import ClientSession

from bot.cbdata import GenerateCallbackFactory

router = Router()


@router.callback_query(GenerateCallbackFactory.filter())
async def generate(call: CallbackQuery,
                   callback_data: GenerateCallbackFactory,
                   session: ClientSession):
    async with ChatActionSender.typing(chat_id=call.message.chat.id, initial_sleep=0):
        gpt_responce = await session.post("/gpt/generate", json={
            "application_id": callback_data.application_id,
            "language": callback_data.language
        })
        gpt = await gpt_responce.json()
        await call.message.answer(
            callback_data.language + ":" + "<code>" + "\n".join(choice["text"] for choice in gpt["choices"]) + "</code>"
        )
