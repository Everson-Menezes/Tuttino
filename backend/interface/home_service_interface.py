from abc import ABC, abstractmethod

class IHomeService(ABC):
    @abstractmethod
    async def get_message(self) -> dict:
        pass
