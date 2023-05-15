from beanie import PydanticObjectId
from fastapi import APIRouter, Body

from ...server.models.application import Application
from ...server.schemas.completion import Completion

import openai

router = APIRouter(prefix="/gpt", tags=["gpt"])


@router.post("/generate", response_description="Generate from a saved application")
async def generate_gpt_answer(application_id: PydanticObjectId = Body(), language: str = Body()) -> Completion:
    application = await Application.get(application_id)
    openai.api_key = "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"
    completions = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=await application.get_prompt(language),
        max_tokens=1_000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return completions
