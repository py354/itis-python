""" Интерфейсы контейнеров """

from abc import ABC, abstractmethod
from typing import Iterable, Tuple, Union


class BaseMap(ABC):
    """ Интерфейс Map """

    @abstractmethod
    def __setitem__(self, key: str, value: Union[int, str]) -> None:
        ...

    @abstractmethod
    def __getitem__(self, key: str) -> Union[int, str]:
        ...

    @abstractmethod
    def __delitem__(self, key: str) -> None:
        ...

    @abstractmethod
    def __iter__(self) -> Iterable[Tuple[str, Union[int, str]]]:
        ...

    def __contains__(self, key: str) -> bool:
        try:
            _ = self[key]
            return True
        except KeyError:
            return False

    def __eq__(self, other: 'BaseMap') -> bool:
        if len(self) != len(other):
            return False

        for key, value in self:
            if key not in other or other[key] != value:
                return False
        return True

    def __bool__(self) -> bool:
        return len(self) != 0

    @abstractmethod
    def __len__(self):
        ...

    def items(self) -> Iterable[Tuple[str, Union[int, str]]]:
        """ Возвращает данные словаря """
        for pair in self:
            yield pair

    def values(self) -> Iterable[Union[int, str]]:
        """ Возвращает значения словаря """
        for pair in self:
            yield pair[1]

    def keys(self) -> Iterable[str]:
        """ Возвращает ключи словаря """
        for pair in self:
            yield pair[0]

    @classmethod
    def fromkeys(cls, iterable, value=None) -> 'BaseMap':
        """ Устанавливает значение value по ключам из iterable """
        store = cls()
        for k in iterable:
            store[k] = value
        return store

    def update(self, other) -> None:
        """ Обновляет данные по other (другому словарю) """
        if hasattr(other, 'keys'):
            for k in other.keys():
                self[k] = other[k]
        else:
            for k in other:
                self[k] = other[k]

    def get(self, key, default=None):
        """ Возвращает значение или default """
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key, *args) -> Union[int, str]:
        """ Удаляет key и возвращает его значение или переданный аргумент (иначе ошибка) """
        if key in self:
            value = self[key]
            del self[key]
            return value
        if len(args) != 0:
            return args[0]
        raise KeyError

    def popitem(self) -> Tuple[str, Union[int, str]]:
        """ Удаляет key и возвращает (ключ, значение), иначе None """
        for key, value in self:
            del self[key]
            return key, value

    def setdefault(self, key, default: Union[int, str] = None) -> Union[int, str]:
        """ Возвращает значение по ключу при наличии, иначе устанавливает значение в default """
        if key not in self:
            self[key] = default
        return self[key]

    def clear(self):
        """ Очищает объект """
        for key in self.keys():
            del self[key]

    def write(self, path: str) -> None:
        """ Сериализует словарь в файл """
        with open(path, 'w', encoding='utf-8') as file:
            file.write(self.to_string())

    @classmethod
    def read(cls, path: str) -> 'BaseMap':
        """ Десереализует словарь из файла """
        my_obj = cls()

        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()
            my_obj.from_string(text)

        return my_obj

    def to_string(self) -> str:
        """ Сериализует словарь в строку """
        data = ''
        for key, value in self:
            if isinstance(value, str):
                value = f'"{value}"'
            data += f'{key}: {value}\n'
        return data

    def from_string(self, data: str):
        """ Десереализует словарь из строки """
        for line in data.splitlines():
            key, value = line.split(': ')
            if value[0] == '"' and value[-1] == '"':
                value = value[1:-1]
            else:
                value = int(value)
            self[key] = value
