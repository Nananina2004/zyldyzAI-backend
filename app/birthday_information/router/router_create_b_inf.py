

from fastapi import Depends
from pydantic import Field
from app.utils import AppModel
from typing import Any
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router
from ..service import Service, get_service


class CreateInformationRequest(AppModel):
    birthday: str
    birth_time: str
    location: str

    

class CreateInformationResponse(AppModel):
     id: Any = Field(alias="_id")


@router.post("/", response_model = CreateInformationResponse)
def create_birthday(
    input: CreateInformationRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    inf_id = svc.repository.create_birth(user_id, dict(input))
    return CreateInformationResponse(id=inf_id)
