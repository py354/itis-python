from typing import List
from containers.interfaces import Map
from containers.linked_list import LinkedList


class HashMap(Map):
    """ Реализация Map на основе хеш-таблицы из ячеек LinkedList """

    LOAD_FACTOR_TO_INCREASE = 0.75
    LOAD_FACTOR_TO_DECREASE = 0.1

    def __init__(self, capacity=10):
        self.length = 0
        self.capacity = capacity
        self.buckets: List[LinkedList] = [LinkedList() for _ in range(capacity)]

    def __iter__(self):
        """ Итерация по словарю (ключ, значение) """
        for bucket in self.buckets:
            yield from bucket

    def __resize(self, capacity):
        """ Пересоздание таблицы с новым размером """
        self.capacity = capacity
        new_buckets = [LinkedList() for _ in range(capacity)]
        for key, value in self:
            new_buckets[hash(key) % capacity].append(key, value)

    def __setitem__(self, key, value):
        """ Добавление или изменение элемента по ключу """
        bucket = self.buckets[hash(key) % self.capacity]
        node = bucket.get(key)
        if node:
            node.value = value
        else:
            bucket.append(key, value)
            self.length += 1

            if self.length / self.capacity > HashMap.LOAD_FACTOR_TO_INCREASE:
                self.__resize(self.capacity * 2)

    def __delitem__(self, key):
        """ Удаление элемента по ключу """
        bucket = self.buckets[hash(key) % self.capacity]
        if bucket.delete(key):
            self.length -= 1

            if self.length / self.capacity < HashMap.LOAD_FACTOR_TO_DECREASE:
                self.__resize(self.capacity // 2)

    def __getitem__(self, key):
        """ Получение элемента по ключу """
        bucket = self.buckets[hash(key) % self.capacity]
        node = bucket.get(key)
        if node:
            return node.value
        raise KeyError

    def __len__(self):
        return self.length
