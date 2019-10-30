from abc import ABC, abstractmethod
from data_structures import Message


class BaseMessenger(ABC):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def is_active(self) -> bool:
        pass

    @abstractmethod
    def get_message(self) -> Message:
        pass

    @abstractmethod
    def transition(self, arg) -> None:
        pass
