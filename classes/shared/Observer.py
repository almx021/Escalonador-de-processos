import abc

class Observer(abc.ABC):
    def alert(self, event: str):
        ...