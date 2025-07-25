from fastapi import APIRouter, Depends, HTTPException
from application.health_service import HealthService
from infrastructure.postgres_checker import PostgresChecker

router = APIRouter()

# Factory function to instantiate dependencies (could be replaced by DI container)
def get_health_service():
    pg_checker = PostgresChecker(
        user="tuttino_user",
        password="tuttino_pass",
        database="tuttino_db",
        host="tuttino-postgres"
    )
    return HealthService(pg_checker)

@router.get("/health")
async def health(service: HealthService = Depends(get_health_service)):
    result = await service.check_health()
    if result["db_status"] == "error":
        raise HTTPException(status_code=503, detail="Database unreachable")
    return result
