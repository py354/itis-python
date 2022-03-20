from abc import ABC, abstractmethod


class Map(ABC):
    @abstractmethod
    def __setitem__(self, key, value):
        pass

    @abstractmethod
    def __delitem__(self, key):
        pass

    @abstractmethod
    def __getitem__(self, item):
        pass
