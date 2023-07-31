from kerykeion import KrInstance, MakeSvgInstance, Report
from fastapi import Depends, Response, HTTPException
from app.utils import AppModel
from cairosvg import svg2png
from typing import Any
from fastapi.responses import JSONResponse

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router
from ..service import Service, get_service
from io import BytesIO




@router.post("/createChart")
def make_my_natal_chart(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    inf = svc.repository.get_inf_by_user_id(user_id)
    birthday = inf["birthday"]
    birth_time = inf["birth_time"]
    location = inf["location"]
    year, month, day = birthday.split("-")
    user = user_id + ""
    hour, minute = birth_time.split(":")
    person = KrInstance(user, int(year), int(month), int(day), int(hour), int(minute), location)

    name = MakeSvgInstance(person, chart_type="Natal", new_output_directory="app/charts/svgs")
    svg_content = name.makeSVG()
    file_path = f"app/charts/svgs/{user}NatalChart.svg"
    
    binary_svg = svg_to_bytesio(file_path)
    png_bytes = svg2png(bytestring=binary_svg)
    png_bytes_io = BytesIO(png_bytes)

    url = svc.s3_service.upload_file(png_bytes_io, f"{user}_chart.png")
    
    inserted_id = svc.repository.create_svg(user_id, url)
    if inserted_id:
        return JSONResponse(content={"message": "Chart created successfully."}, status_code=200)
    else:
        raise HTTPException(status_code=500, detail="Failed to create chart.")



def svg_to_bytesio(svg_file_path):
    with open(svg_file_path, 'rb') as file:
        svg_bytes = file.read()
    
    return svg_bytes


@router.get("/getChart")
def get_my_natal_chart(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
)-> dict[str, str]:
    user_id = jwt_data.user_id
    url = svc.repository.get_svg_url(user_id)
    if url is None:
        return Response(status_code=404)
    return {"message": url}