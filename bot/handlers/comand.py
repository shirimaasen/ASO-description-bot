from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiohttp import ClientSession

from .create_application import start_create_application

router = Router()


@router.message(Command("start"))
async def start_command(message: Message,
                        session: ClientSession,
                        state: FSMContext):
    await session.post("/user", json={"id": message.from_user.id})
    await start_create_application(message, state)
