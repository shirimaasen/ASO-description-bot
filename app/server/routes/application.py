from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException

from ...server.models import Application, Variable

from ...server import schemas
from ...server.schemas.application import ApplicationUpdate

router = APIRouter(prefix="/application", tags=["application"])


@router.get("/", response_model=list[schemas.Application], response_model_by_alias=False)
async def read_applications(
    skip: int = 0,
    limit: int = 100,
    user_id: int | None = None
) -> list[Application]:
    """
    Get all Applications.
    """
    if user_id:
        applications = await Application.get_by_user(user_id=user_id, skip=skip, limit=limit)
    else:
        applications = await Application.find_all(skip, limit).to_list()
    return applications


@router.get("/{application_id}", response_model=schemas.Application, response_model_by_alias=False)
async def read_application(
    application_id: PydanticObjectId
) -> Application:
    """
    Get Application by id.
    """
    if application := await Application.get(application_id):
        return application
    else:
        raise HTTPException(
            status_code=400, detail="Application doesn't exists"
        )


@router.post("/", response_model=schemas.Application)
async def create_application(
    *,
    payload: schemas.ApplicationCreate,
) -> Application:
    application = await Application(**payload.dict()).create()
    return application


@router.post("/{application_id}/variable", response_model=schemas.Application, tags=["variable"])
async def add_variables(application_id: PydanticObjectId, variables: Variable) -> Application:
    if application := await Application.get(application_id):
        application.variables.append(variables)
        await application.save()
        return application


@router.put("/", response_model=schemas.Application)
async def add_variables(application_update: ApplicationUpdate) -> Application:
    if application := await Application.get(application_update.id):
        if application_update.name:
            application.name = application_update.name
        if application_update.description:
            application.description = application_update.description
        if application_update.variables:
            application.variables = application_update.variables
        await application.replace()
        return application
