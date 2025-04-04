import unittest
from hash_map_sc import HashMap, hash_function_1

class TestHashMap(unittest.TestCase):

    def setUp(self):
        # Set up a fresh HashMap instance before each test
        self.map = HashMap(10, hash_function_1)

    def test_empty_buckets_initial(self):
        # Test the initial state of empty buckets
        self.assertEqual(self.map.empty_buckets(), 10, "All buckets should initially be empty.")

    def test_empty_buckets_after_insertion(self):
        # Insert a single key-value pair
        self.map.put("key1", 1)
        # Verify the number of empty buckets decreases
        self.assertEqual(self.map.empty_buckets(), 9, "One bucket should now be occupied.")

    def test_empty_buckets_with_collisions(self):
        # Insert keys that hash to the same bucket
        self.map.put("key1", 1)
        self.map.put("key2", 2)  # Assume key2 collides with key1
        # Verify the number of empty buckets doesn't change
        self.assertEqual(self.map.empty_buckets(), 9, "Collisions should not increase empty buckets.")

    def test_empty_buckets_with_multiple_insertions(self):
        # Insert multiple key-value pairs
        keys = [f"key{i}" for i in range(5)]
        for key in keys:
            self.map.put(key, i)
        # Verify the number of empty buckets
        self.assertEqual(self.map.empty_buckets(), 5, "Five buckets should now be occupied.")

    def test_empty_buckets_after_removal(self):
        # Insert and then remove a key
        self.map.put("key1", 1)
        self.map.remove("key1")
        # Verify the bucket becomes empty again
        self.assertEqual(self.map.empty_buckets(), 10, "Removing a key should make the bucket empty.")

    def test_empty_buckets_after_resize(self):
        # Insert keys to trigger resizing
        for i in range(15):  # Exceeds initial capacity
            self.map.put(f"key{i}", i)
        # Verify empty buckets after resize
        expected_capacity = 23  # Assuming resize doubles to next prime
        expected_empty_buckets = expected_capacity - 15
        self.assertEqual(self.map.empty_buckets(), expected_empty_buckets,
                         f"Empty buckets should match the new capacity minus number of elements.")

if __name__ == '__main__':
    unittest.main()