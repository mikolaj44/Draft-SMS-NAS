from abc import abstractmethod

class MenuAction:
    description: str

    def __init__(self, description: str) -> None:
        self.description = description

    @abstractmethod
    def select(self):
        pass