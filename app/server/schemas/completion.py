from pydantic import BaseModel


class Choice(BaseModel):
    finish_reason: str
    index: int
    logprobs: str | None
    text: str


class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class Completion(BaseModel):
    choices: list[Choice]
    created: int
    id: str
    object: str
    usage: Usage
