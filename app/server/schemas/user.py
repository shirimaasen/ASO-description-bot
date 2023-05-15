from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    id: int


class User(UserCreate):
    id: int = Field(alias="_id")

    class Config:
        alias_generator = lambda alias: alias.replace('_', '')
        orm_mode = True
