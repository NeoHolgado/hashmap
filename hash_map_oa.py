# Name: Neo Holgado
# OSU Email: holgadon@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/05/2024
# Description: Implementation of a HashMap using open addressing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map.
        If the key already exists, its value will be replaced by the new value.
        If the key doesn't already exist, a new key/value pair will be added.
        """
        # Check if resizing is necessary
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Calculate the initial index and setup counter
        index = self._hash_function(key) % self._capacity
        probe_counter = 0

        # Use quadratic probing to find an open slot
        while probe_counter < self._capacity:
            # Calculate probing index
            probe_index = (index + probe_counter ** 2) % self._capacity
            bucket = self._buckets.get_at_index(probe_index)

            # If the slot is empty, add the key/value pair
            if bucket is None:
                self._buckets.set_at_index(probe_index, HashEntry(key, value))
                self._size += 1
                return

            # If the key already exists, update the value
            if bucket.key == key:
                bucket.value = value
                return

            # Move to the next probe index
            probe_counter += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table.
        All active key/value pairs must be put into the new table.
        """
        # Check if new capacity is not less than size
        if new_capacity < self._size:
            return

        # Make sure that the new capacity is a prime number
        prime_capacity = self._next_prime(new_capacity)

        # Save current buckets and reinitialize the table
        old_buckets = self._buckets
        self._buckets = DynamicArray()
        self._capacity = prime_capacity
        self._size = 0
        for _ in range(prime_capacity):
            self._buckets.append(None)

        # Rehash active entries
        for num in range(old_buckets.length()):
            bucket = old_buckets.get_at_index(num)
            if bucket and not bucket.is_tombstone:
                self.put(bucket.key, bucket.value)

    def table_load(self) -> float:
        """
        Calculates and returns the hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        # Initialize empty bucket counter
        empty_bucket_counter = 0

        # Check if the value of each bucket is None
        for num in range(self._buckets.length()):
            if self._buckets.get_at_index(num) is None:
                empty_bucket_counter += 1

        return empty_bucket_counter

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        If the key is not in the hash map, returns None
        """
        # Calculate the initial index and setup counter
        index = self._hash_function(key) % self._capacity
        probe_counter = 0

        # Search for the key
        while probe_counter < self._capacity:
            probe_index = (index + probe_counter ** 2) % self._capacity

            # If the bucket is empty, key is not in map
            bucket = self._buckets.get_at_index(probe_index)
            if bucket is None:
                return None

            # If the key is in the map, return its value
            if bucket.key == key and not bucket.is_tombstone:
                return bucket.value

            # Continue probing
            probe_counter += 1

        # If all other conditions don't pass, return None
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns true if the key is in the hash map, otherwise galse
        """
        # Calculate the initial index and setup counter
        index = self._hash_function(key) % self._capacity
        probe_counter = 0

        # Search for the key
        while probe_counter < self._capacity:
            probe_index = (index + probe_counter ** 2) % self._capacity

            # If the bucket is empty, key is not in map
            bucket = self._buckets.get_at_index(probe_index)
            if bucket is None:
                return False

            # If the key is in the map, return True
            if bucket.key == key and not bucket.is_tombstone:
                return True

            # Continue probing
            probe_counter += 1

        # If all other conditions don't pass, return False
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the has map, the method does nothing
        """
        # Calculate the initial index and setup counter
        index = self._hash_function(key) % self._capacity
        probe_counter = 0

        # Search for the key
        while probe_counter < self._capacity:
            probe_index = (index + probe_counter ** 2) % self._capacity

            # If the bucket is empty, key is not in map
            bucket = self._buckets.get_at_index(probe_index)
            if bucket is None:
                return

            # If the key is in the map, remove it
            if bucket.key == key and not bucket.is_tombstone:
                bucket.is_tombstone = True
                self._size -= 1
                return

            # Continue probing
            probe_counter += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a da where each index contains a tuple of a key/value pair
        stored in the hash map
        """
        # Initialize the resulting array
        key_value_arr = DynamicArray()

        # Iterate through all the buckets
        for num in range(self._capacity):
            bucket = self._buckets.get_at_index(num)

            # Check if the bucket is not none, append the pair to the array
            if bucket is not None and not bucket.is_tombstone:
                key_value_arr.append((bucket.key, bucket.value))

        return key_value_arr

    def clear(self) -> None:
        """
        Clears the contents of the hash map
        """
        # Reset all buckets to none
        for num in range(self._capacity):
            self._buckets.set_at_index(num, None)

        # Reset the size to 0
        self._size = 0

    def __iter__(self):
        """
        Enables the hash map to iterate across itself
        """
        return HashMapIterator(self)

    def get_bucket(self, index: int) -> int:
        """
        Returns the bucket at the given index
        """
        return self._buckets.get_at_index(index)


class HashMapIterator:
    """
    Hash map iterator class
    """
    def __init__(self, hash_map: HashMap) -> None:
        self._hash_map = hash_map
        self._current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        """
        Returns the next active item in the hash map
        """
        # Iterate through the hash map
        while self._current_index < self._hash_map.get_capacity():
            # Find the bucket at current index
            bucket = self._hash_map.get_bucket(self._current_index)
            self._current_index += 1

            # Make sure the bucket isn't empty, then set key and value
            if bucket is not None:
                self.key, self.value = bucket.key, bucket.value
                return self

        # Stop iteration if all buckets have been processed
        raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
