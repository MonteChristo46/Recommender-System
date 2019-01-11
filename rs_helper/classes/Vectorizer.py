from abc import ABC, abstractmethod


class Vectorizer(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def vectorize(self, **kwargs) -> list:
        pass