# domain/home_service_interface.py
from abc import ABC, abstractmethod

class IHomeService(ABC):
    @abstractmethod
    async def get_message(self) -> dict:
        pass
