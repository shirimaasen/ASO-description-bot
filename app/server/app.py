from fastapi import FastAPI

from app.server.core.config import settings
from app.server.routes.openai_generate import router as openai_generate_router
from app.server.routes.application import router as application_router
from app.server.routes.user import router as user_router

from app.server.database import init as init_db

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

if settings.BACKEND_CORS_ORIGINS:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(openai_generate_router)
app.include_router(application_router)
app.include_router(user_router)
