""" Реализация LinkedList для использования в HashMap """

from typing import Optional


class ListNode:
    """ Узел для LinkedList """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next_node: Optional[ListNode] = None

    def set_next_node(self, next_node: Optional['ListNode']):
        """ Устанавливает следующий узел в списке """
        self.next_node = next_node

    def __eq__(self, other) -> bool:
        return self.key == other.key


class LinkedList:
    """ Реализация LinkedList для использования в HashMap """

    def __init__(self):
        self.length = 0
        self.head: Optional[ListNode] = None
        self.tail: Optional[ListNode] = None

    def append(self, key, value):
        """ Добавление в конец """
        self.length += 1

        if self.tail:
            self.tail.set_next_node(ListNode(key, value))
            self.tail = self.tail.next_node
        else:
            self.head = ListNode(key, value)
            self.tail = self.head

    def get(self, key) -> Optional[ListNode]:
        """ Получение узла по ключу """
        node = self.head
        while node:
            if node.key == key:
                return node
            node = node.next_node
        return None

    def __iter__(self):
        node = self.head
        while node:
            yield node.key, node.value
            node = node.next_node

    def delete(self, key) -> bool:
        """ Удаление узла по ключу """
        if self.head is None:
            return False

        # если искомый элемент - первый
        if self.head.key == key:
            self.length -= 1
            if self.head.next_node is None:
                self.head = None
                self.tail = None
            else:
                self.head = self.head.next_node
            return True

        # если искомый элемент - не первый
        node = self.head
        while node.next_node:
            next_node = node.next_node
            if next_node.key == key:
                self.length -= 1
                if next_node == self.tail:
                    self.tail = node
                node.set_next_node(next_node.next_node)
                return True
            node = node.next_node

        return False
