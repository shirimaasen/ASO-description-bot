from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException

from ...server import schemas
from ...server.models import User

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def read_users(
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    """
    Get all Users.
    """
    return await User.find_all(skip, limit).to_list()


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(
    user_id: int
) -> User:
    """
    Get User by id.
    """
    if user := await User.find_one(User.id == user_id):
        return user
    else:
        raise HTTPException(
            status_code=400, detail="User doesn't exists"
        )


@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    payload: schemas.UserCreate,
) -> User:
    user = await User(
        id=payload.id
    ).create()
    return user
