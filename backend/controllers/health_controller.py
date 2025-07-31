# controllers/health_controller.py
from fastapi import APIRouter, Depends, HTTPException
from interface.health_service_interface import IHealthService
from application.health_service import HealthService
from infrastructure.postgres_checker import PostgresChecker

router = APIRouter()

def get_health_service() -> IHealthService:
    pg_checker = PostgresChecker(user="user", password="pass", database="db", host="host")
    return HealthService(pg_checker)

@router.get("/health")
async def health(service: IHealthService = Depends(get_health_service)):
    result = await service.check_health()
    if result["db_status"] == "error":
        raise HTTPException(status_code=503, detail="Database unreachable")
    return result
