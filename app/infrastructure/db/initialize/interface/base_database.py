from abc import ABC, abstractmethod


class BaseDatabase(ABC):
    @abstractmethod
    async def initialize_db(self) -> None:
        raise NotImplementedError()