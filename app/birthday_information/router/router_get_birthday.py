from fastapi import Depends, Response
from pydantic import Field
from app.utils import AppModel
from typing import Any
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router
from ..service import Service, get_service


class GetInformationResponse(AppModel):
    birthday: str
    birth_time: str
    location: str

    
@router.get("/birthday", response_model = GetInformationResponse)
def get_my_birthday(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
)-> dict[str, str]:
    user_id = jwt_data.user_id
    inf = svc.repository.get_inf_by_user_id(user_id)
    if inf is None:
        return Response(status_code=404)
    return GetInformationResponse(**inf)