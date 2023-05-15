from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from ..server.core.config import settings
from ..server.models import gather_documents


async def init() -> None:
    client = AsyncIOMotorClient(str(settings.MONGODB_URI))
    await init_beanie(
        database=getattr(client, settings.MONGODB_DB_NAME),
        document_models=gather_documents(),  # type: ignore[arg-type]
    )
