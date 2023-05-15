import re


def application_text(name: str, description: str, variables: list[dict[str, list[str]]] | None = None, *args, **kwargs) \
        -> str:
    text = f"{name}\n\n{description}\n\n"
    if variables:
        text += '\n'.join(f"{variable['language']}: {', '.join(variable['keywords'])}" for variable in variables)
    return text


def pars_keywords(message_text: str) -> list | None:
    if keywords := list(map(lambda text: text.strip(), message_text.split(','))):
        return keywords


def pars_variable(message_text: str) -> dict | None:
    language_raw, keywords_raw = message_text.split(':', 1)
    if language := re.findall(r"(\w+)", language_raw):
        language = language[0]
    if keywords := pars_keywords(keywords_raw):
        return {"language": language, "keywords": keywords}
    else:
        return None
