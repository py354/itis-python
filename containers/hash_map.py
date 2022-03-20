from typing import List
from containers.interfaces import Map
from containers.linked_list import LinkedList


class HashMap(Map):
    LOAD_FACTOR_TO_INCREASE = 0.75
    LOAD_FACTOR_TO_DECREASE = 0.1

    def __init__(self, capacity=10):
        self.length = 0
        self.capacity = capacity
        self.buckets: List[LinkedList] = [LinkedList() for _ in range(capacity)]

    def __iter__(self):
        for bucket in self.buckets:
            for item in bucket:
                yield item

    def __resize(self, capacity):
        self.capacity = capacity
        new_buckets = [LinkedList() for _ in range(capacity)]
        for key, value in self:
            new_buckets[hash(key) % capacity].append(key, value)

    def __setitem__(self, key, value):
        bucket = self.buckets[hash(key) % self.capacity]
        node = bucket.get(key)
        if node is None:
            bucket.append(key, value)
            self.length += 1

            if self.length / self.capacity > HashMap.LOAD_FACTOR_TO_INCREASE:
                self.__resize(self.capacity * 2)
        else:
            node.value = value

    def __delitem__(self, key):
        bucket = self.buckets[hash(key) % self.capacity]
        if bucket.delete(key):
            self.length -= 1

            if self.length / self.capacity < HashMap.LOAD_FACTOR_TO_DECREASE:
                self.__resize(self.capacity // 2)

    def __getitem__(self, key):
        bucket = self.buckets[hash(key) % self.capacity]
        node = bucket.get(key)
        if node is None:
            raise KeyError
        else:
            return node.value

    def __len__(self):
        return self.length
