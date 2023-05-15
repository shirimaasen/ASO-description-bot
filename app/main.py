import uvicorn

from server.core.config import settings


def run_dev_server() -> None:
    uvicorn.run(
        "server.app:app",  # path to the FastAPI application
        host="127.0.0.1" if settings.DEBUG else "0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    run_dev_server()
