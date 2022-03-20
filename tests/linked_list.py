import unittest
from containers.linked_list import LinkedList


class LinkedListTest(unittest.TestCase):
    def setUp(self) -> None:
        self.list = LinkedList()

    def test(self):
        self.list.append('key', 'value')
        self.assertEqual(self.list.length, 1)
        self.assertEqual(self.list.get('key').value, 'value')

        self.list.append('key2', 'value2')
        self.assertEqual(self.list.length, 2)
        self.assertEqual(self.list.get('key2').value, 'value2')

        self.list.delete('key')
        self.assertEqual(self.list.length, 1)
        self.assertEqual(self.list.get('key'), None)

if __name__ == '__main__':
    unittest.main()
