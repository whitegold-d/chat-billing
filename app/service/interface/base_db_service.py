from abc import ABC, abstractmethod


class BaseDBService(ABC):
    @abstractmethod
    async def init_db(self) -> None:
        raise NotImplementedError()