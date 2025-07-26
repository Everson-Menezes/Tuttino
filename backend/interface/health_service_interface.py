from abc import ABC, abstractmethod

class IHealthService(ABC):
    @abstractmethod
    async def check_health(self) -> dict:
        pass
