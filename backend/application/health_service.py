from interface.services.health_service_interface import IHealthService
from infrastructure.postgres_checker import PostgresChecker

class HealthService(IHealthService):
    def __init__(self, pg_checker: PostgresChecker):
        self.pg_checker = pg_checker

    async def check_health(self) -> dict:
        db_ok = await self.pg_checker.is_healthy()
        status = "ok" if db_ok else "error"
        return {
            "app_status": "ok",
            "db_status": status
        }
