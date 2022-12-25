from abc import ABC, abstractmethod


class Component(ABC):
    """ Demons component. """
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def state(self) -> str:
        pass
