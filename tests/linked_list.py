""" Тесты для LinkedList """

import unittest
from maps.linked_list import LinkedList


class LinkedListTest(unittest.TestCase):
    """ Тесты для LinkedList """

    def setUp(self) -> None:
        self.list = LinkedList()

    def test(self):
        """ Тесты для LinkedList """

        self.list.append('key', 'value')
        self.assertEqual(self.list.length, 1)
        self.assertEqual(self.list.get('key').value, 'value')

        self.list.append('key2', 'value2')
        self.assertEqual(self.list.length, 2)
        self.assertEqual(self.list.get('key2').value, 'value2')

        self.assertEqual(list(self.list), [('key', 'value'), ('key2', 'value2')])

        self.list.delete('key')
        self.assertEqual(self.list.length, 1)
        self.assertEqual(self.list.get('key'), None)

        self.assertEqual(list(self.list), [('key2', 'value2')])


if __name__ == '__main__':
    unittest.main()
