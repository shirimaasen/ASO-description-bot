import logging
from pathlib import Path
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, MongoDsn, validator

from app import __version__

# This adds support for 'mongodb+srv' connection schemas when using e.g. MongoDB Atlas
MongoDsn.allowed_schemes.add("mongodb+srv")


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "ClosedAI"
    PROJECT_VERSION: str = __version__
    DEBUG: bool = True
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = []

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "logs/closedai.log"

    @validator("LOG_LEVEL")
    def log_level_validator(cls, v: str) -> str:  # noqa
        v = v.upper()
        if not hasattr(logging, v):
            raise ValueError(f"Invalid log level: {v!r}")
        return v

    @validator("LOG_FILE_PATH")
    def check_log_file_path(cls, v: str) -> str:  # noqa
        if not v.endswith(".log"):
            raise ValueError(f"Invalid log file path: {v!r} (must end with .log)")
        Path(v).parent.mkdir(parents=True, exist_ok=True)
        return v

    # Custom validators that have 'pre' set to 'True', will be called before
    # all standard pydantic validators.
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls,  # noqa
        v: Union[str, List[str]],
    ) -> Union[str, List[str]]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    MONGODB_URI: MongoDsn = "mongodb+srv://nazar:BnoYOb0wQIfFcc7m@cluster0.lco9zcb.mongodb.net/" \
                            "?retryWrites=true&w=majority"  # type: ignore[assignment]
    MONGODB_DB_NAME: str = "closedai"

    class Config:
        case_sensitive = True


settings = Settings()
