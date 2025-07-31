# controllers/home_controller.py
from fastapi import APIRouter, Depends

from application.home_service import HomeService
from interface.services.home_service_interface import IHomeService

router = APIRouter()

def get_home_service() -> IHomeService:
    return HomeService()

@router.get("/home")
async def home(service: IHomeService = Depends(get_home_service)):
    return await service.get_message()
