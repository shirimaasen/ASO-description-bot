from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class Variable(BaseModel):
    language: str
    keywords: list[str]


class ApplicationBase(BaseModel):
    name: str | None
    description: str | None
    variables: list[Variable] | None


class ApplicationCreate(ApplicationBase):
    name: str
    description: str
    variables: list[Variable] = []
    user_id: int

    class Config:
        schema_extra = {
            "example": {
                "name": "PC Creator 2",
                "description": "PC Creator 2 is a computer simulator where you can build your own computer, install "
                               "operational systems and computer software and games. You can also serve clients that "
                               "want to build or upgrade their computers",
                "variables": [
                    {
                        "language": "english",
                        "keywords": [
                            "computer", "gaming", "customer"
                        ]
                    },
                    {
                        "language": "german",
                        "keywords": [
                            "computer", "spiele", "kunden"
                        ]
                    }
                ],
                "user_id": 584775562
            }
        }


class ApplicationUpdate(ApplicationBase):
    id: PydanticObjectId


class Application(ApplicationCreate):
    id: PydanticObjectId = Field(alias='_id')

    class Config:
        orm_mode = True
