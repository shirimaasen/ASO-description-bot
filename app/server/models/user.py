from beanie import Document


class User(Document):
    id: int

    class Settings:
        name = "user"
