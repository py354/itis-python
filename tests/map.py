from containers.hash_map import HashMap
from containers.tree_map import TreeMap

import unittest


class MapTestMixin(unittest.TestCase):
    """ Тесты реализации Map (setitem, getitem, delitem) """
    def setUp(self):
        self.map = dict()

    def test_map_methods(self):
        self.map[1] = 10
        self.assertEqual(self.map[1], 10)
        self.assertEqual(len(self.map), 1)

        self.map[1] = 100
        self.assertEqual(self.map[1], 100)
        self.assertEqual(len(self.map), 1)

        del self.map[1]
        self.assertEqual(len(self.map), 0)

    def test_raise_key_error(self):
        with self.assertRaises(KeyError):
            i = self.map[1]


class HashMapTest(MapTestMixin, unittest.TestCase):
    def setUp(self):
        self.map = HashMap()

    def test_resize(self):
        self.map = HashMap()
        self.map[1] = 10
        self.map[2] = 10
        self.map[3] = 10
        self.map[4] = 10
        self.map[5] = 10
        self.map[6] = 10
        self.map[7] = 10
        self.assertEqual(self.map.capacity, 10)  # load 70%

        self.map[8] = 10
        self.assertEqual(self.map.capacity, 20)  # increase capacity (load > 0.75)

        del self.map[1]
        del self.map[2]
        del self.map[3]
        del self.map[4]
        del self.map[5]
        del self.map[6]
        del self.map[7]
        self.assertEqual(self.map.capacity, 10)  # decrease capacity (load < 0.1)


class TreeMapTest(MapTestMixin, unittest.TestCase):
    def setUp(self):
        self.map = TreeMap()

    def test_sort(self):
        self.map[2] = 10
        self.map[1] = 10
        self.map[4] = 10
        self.map[3] = 10
        self.assertEqual(list(self.map.sorted_range()), [
            (1, 10), (2, 10), (3, 10), (4, 10)
        ])

if __name__ == '__main__':
    unittest.main()
