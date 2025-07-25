from domain.home_service_interface import IHomeService

class HomeService(IHomeService):
    async def get_message(self) -> dict:
        return {"message": "API is online and running"}
