from typing import Optional
from containers.interfaces import Map


class TreeNode(Map):
    """ Реализация узла бинарного дерева """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left_node: Optional[TreeNode] = None
        self.right_node: Optional[TreeNode] = None

    def __len__(self):
        """ Рекурсивное вычисление размера """
        result = 1

        if self.left_node is not None:
            result += len(self.left_node)

        if self.right_node is not None:
            result += len(self.right_node)

        return result

    def __setitem__(self, key, value):
        """ Рекурсивное установка элемента """

        if self.key == key:
            self.value = value
            return

        if self.key > key:
            if self.left_node is None:
                self.left_node = TreeNode(key, value)
            else:
                self.left_node[key] = value
        else:
            if self.right_node is None:
                self.right_node = TreeNode(key, value)
            else:
                self.right_node[key] = value

    def __delitem__(self, key):
        """ Рекурсивное удаление элемента """
        if self.key == key:
            raise Exception

        if self.key > key:
            if self.left_node is None:
                return
            elif self.left_node.key == key:
                self.left_node = TreeNode.union(self.left_node.left_node, self.left_node.right_node)
            else:
                del self.left_node[key]
        else:
            if self.right_node is None:
                return
            elif self.right_node.key == key:
                self.right_node = TreeNode.union(self.right_node.left_node, self.right_node.right_node)
            else:
                del self.right_node[key]

    def __getitem__(self, key):
        """ Рекурсивный поиск элемента """
        if self.key == key:
            return self.value

        if self.key > key:
            if self.left_node is None:
                return None
            return self.left_node[key]
        else:
            if self.right_node is None:
                return None
            return self.right_node[key]

    def sorted_range(self):
        """ Итератор по отсортированным ключам """

        if self.left_node is not None:
            for item in self.left_node.sorted_range():
                yield item

        yield self.key, self.value

        if self.right_node is not None:
            for item in self.right_node.sorted_range():
                yield item
    __iter__ = sorted_range

    @staticmethod
    def union(left: Optional['TreeNode'], right: Optional['TreeNode']) -> Optional['TreeNode']:
        """ Объединение двух деревьев (далеко не оптимальное)"""
        if left is None:
            return right

        if right is None:
            return left

        new_node = left
        for key, value in right:
            new_node[key] = value
        return new_node


class TreeMap(Map):
    """ Реализация Map с бинарным деревом (обертка над TreeNode) """
    def __init__(self):
        self.root: Optional[TreeNode] = None

    def __len__(self):
        """ Рекурсивное вычисление размера """

        if self.root is None:
            return 0
        else:
            return len(self.root)

    def __setitem__(self, key, value):
        """ Рекурсивное установка элемента """

        if self.root is not None:
            self.root[key] = value
        else:
            self.root = TreeNode(key, value)

    def __delitem__(self, key):
        """ Рекурсивное удаление элемента """

        if self.root is None:
            return

        if self.root.key == key:
            # если нужно удалить корень
            self.root = TreeNode.union(self.root.left_node, self.root.right_node)
        else:
            del self.root[key]

    def __getitem__(self, key):
        """ Рекурсивный поиск элемента """

        if self.root is not None:
            return self.root[key]
        raise KeyError

    def sorted_range(self):
        """ Итератор по отсортированным ключам """

        if self.root:
            return self.root.sorted_range()
        return StopIteration
    __iter__ = sorted_range
