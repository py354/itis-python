from containers.hash_map import HashMap

import unittest


class MapTestMixin(unittest.TestCase):
    """ Тесты реализации Map (setitem, getitem, delitem) """
    def setUp(self):
        self.hash_map = dict()

    def test_map_methods(self):
        self.hash_map[1] = 10
        self.assertEqual(self.hash_map[1], 10)
        self.assertEqual(len(self.hash_map), 1)

        self.hash_map[1] = 100
        self.assertEqual(self.hash_map[1], 100)
        self.assertEqual(len(self.hash_map), 1)

        del self.hash_map[1]
        self.assertEqual(len(self.hash_map), 0)

    def test_raise_key_error(self):
        with self.assertRaises(KeyError):
            i = self.hash_map[1]


class HashMapTest(MapTestMixin, unittest.TestCase):
    def setUp(self):
        self.hash_map = HashMap()

    def test_resize(self):
        self.hash_map = HashMap()
        self.hash_map[1] = 10
        self.hash_map[2] = 10
        self.hash_map[3] = 10
        self.hash_map[4] = 10
        self.hash_map[5] = 10
        self.hash_map[6] = 10
        self.hash_map[7] = 10
        self.assertEqual(self.hash_map.capacity, 10)  # load 70%

        self.hash_map[8] = 10
        self.assertEqual(self.hash_map.capacity, 20)  # increase capacity (load > 0.75)

        del self.hash_map[1]
        del self.hash_map[2]
        del self.hash_map[3]
        del self.hash_map[4]
        del self.hash_map[5]
        del self.hash_map[6]
        del self.hash_map[7]
        self.assertEqual(self.hash_map.capacity, 10)  # decrease capacity (load < 0.1)


class TreeMapTest(MapTestMixin, unittest.TestCase):
    map_cls = dict


if __name__ == '__main__':
    unittest.main()
