from typing import Self

from beanie import Document
from pydantic import BaseModel


class Variable(BaseModel):
    language: str
    keywords: list[str]


class Application(Document):
    name: str
    description: str
    variables: list[Variable]
    user_id: int

    @classmethod
    async def get_by_user(
            cls,
            *,
            user_id: int,
            **kwargs
    ) -> list[Self]:
        return await cls.find(cls.user_id == user_id, **kwargs).to_list()

    async def get_prompt(self, language: str) -> str:
        keywords = None
        for variable in self.variables:
            if variable.language == language:
                keywords = variable.keywords
                break
        prompt = f"I want you to act as an ASO manager. I will give you a description of mobile game and a keyword " \
                 f"list. You will generate me an ASO description of my game based on the desctiption that I will give "\
                 f"you. Description will be optimized for mobile store and will have 3950-4000 symbols and will " \
                 f"contain keywords from the keyword list that I will give you. Also text will be devided to " \
                 f"paragraphs\n Description of my game: «{self.description}» Keywords: «{', '.join(keywords)}». "\
                 f"But change language to {language}"
        return prompt

    class Settings:
        name = "application"
