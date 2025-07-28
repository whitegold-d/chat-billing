from abc import ABC, abstractmethod


class BaseDatabase(ABC):
    @abstractmethod
    def init_db(self) -> None:
        raise NotImplementedError()

