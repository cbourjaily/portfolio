# Name: Christopher Vote
# Email: votec@oregonstate.edu
# Description: This program contains an implementation of a hash_map abstract data
#              type. The program uses the methodology of open addressing.
#              The hash_map contains the following public methods: get_size(), get_capacity,
#              put(), resize_table(), table_load(), empty_buckets(), get(), contains_key(),
#              remove(), get_keys_and_values(), and clear().

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
        This method adds a new key/value pair to the HashMap.
        It calls the _map_index() helper method to determine the proper index to place
        the key/value pair.
        In the case the index is occupied, it calls the helper method
        _quadratic_probe() to establish the appropriate open addressed index.
        If that index is occupied by another key/value pair with the same key,
        the key/value pair is updated with the new value.
        :param key: The unique identifying key of the element being added.
        :param value: The value attached to the new element.
        """

        if self.table_load() >= 0.5:
            self.resize_table(self.get_capacity() * 2)

        newEntry = HashEntry(key, value)
        index = self._map_index(key)

        current = self._buckets.get_at_index(index)
        if current is not None and not current.is_tombstone and current.key == key:
            current.value = value
            return

        # Handle the case in which the initial slot is empty.
        if current is None:
            self._buckets.set_at_index(index, newEntry)
            self._size = self._size + 1
            return

        firstTombstone = index if current.is_tombstone else None
        initialIndex = index

        # Begin quadratic probe to find the next free index or same key.
        j = 1
        while j < self._capacity:
            index = self._quadratic_probe(initialIndex, j)
            current = self._buckets.get_at_index(index)

            # Retrace back to the first tombstone in event of None, if such tombstone exists.
            if current is None:
                target = firstTombstone if firstTombstone is not None else index
                self._buckets.set_at_index(target, newEntry)
                self._size = self._size + 1
                return

            if current.is_tombstone:
                if firstTombstone is None:
                    firstTombstone = index

            # Check for key at each iteration.
            elif current.key == key:
                current.value = value
                return

            j = j + 1

    def resize_table(self, new_capacity: int) -> None:
        """
        This method is responsible for resizing the underlying DynamicArray data
        structure to a new capacity. The method first verifies that the proposed
        new_capacity is not less than the number of elements currently present in
        the table. If new_capacity is valid, the method resets the capacity to
        new_capacity if new_capacity is a prime, or else sets the capacity to the
        magnitude of the next prime number.
        :param new_capacity: The proxy for the new capacity to which the table is
        to be resized.
        """

        if new_capacity < self._size:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        elements = self.get_keys_and_values()
        self._buckets = DynamicArray()
        for _ in range(new_capacity):
            self._buckets.append(None)

        self._capacity = new_capacity
        self._size = 0

        for i in range(elements.length()):
            key, value = elements.get_at_index(i)
            self.put(key, value)

    def table_load(self) -> float:
        """
        This method provides the current load factor of the hash_table, which is
        determined on the basis of the average number of elements in each bucket.
        """

        if self._buckets.length() == 0:
            return 0.0
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        This method tallys the number of empty buckets and returns this count.
        :return: The number of empty buckets in the hash table.
        """

        count = 0
        for i in range(self._capacity):
            if self._buckets[i] is None or self._buckets[i].is_tombstone:
                count = count + 1
        return count

    def get(self, key: str) -> object:
        """
        This method retrieves an element associated with the provided key.
        If no element by that key exists in the hash table, None is returned.
        :param key: A unique key for identifying an element in the hash map.
        :return: The element associated with the key, or None if no such element
        exists.
        """

        index = self._map_index(key)

        # Use quadratic probing to iterate through potential indices.
        for j in range(self._capacity):
            probeIndex = self._quadratic_probe(index, j)
            entry = self._buckets.get_at_index(probeIndex)

            if entry is None:
                return None
            if not entry.is_tombstone and entry.key == key:
                return entry.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        This method checks if an element associated with a particular key is present
        in the hash table. If so, it returns True; otherwise, it returns False.
        :param key: A key value to be checked.
        :return: True if the key is associated with an existing value, otherwise false.
        """
        index = self._map_index(key)

        # Use quadratic probing to iterate through potential indices.
        for j in range(self._capacity):
            probeIndex = self._quadratic_probe(index, j)
            entry = self._buckets.get_at_index(probeIndex)

            if entry is None:
                return False
            if not entry.is_tombstone and entry.key == key:
                return True

        return False

    def remove(self, key: str) -> None:
        """
        This method takes a key and removes the element associated with the key,
        if such an element exists. Otherwise, the method does nothing.
        """
        index = self._map_index(key)

        # Use quadratic probing to iterate through potential indices.
        for j in range(self._capacity):
            probeIndex = self._quadratic_probe(index, j)
            entry = self._buckets.get_at_index(probeIndex)

            if entry is None:
                return

            if not entry.is_tombstone and entry.key == key:
                entry.is_tombstone = True
                self._size = self._size - 1
                return

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method retrieves the key/value pairs in the hash_map and
        returns them.
        :return: A DynamicArray containing the key/value in tuples of the form
        (key, value).
        """

        da = DynamicArray()
        for i in range(self._capacity):
            entry = self._buckets.get_at_index(i)
            if entry is not None and not entry.is_tombstone:
                da.append((entry.key, entry.value))
        return da


    def clear(self) -> None:
        """
        This method clears the contents of the hash map, without changing the underlying
        capacity of the table.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0


    def __iter__(self):
        """
        This method enables the HashMap to iterate across its contents.
        The attribute _index is used by the __next__ method to track the
        progress of the iteration across these contents.
        """

        self._index = 0
        return self

    def __next__(self):
        """
        This method increments through each object in the hash table. It does so
        by returning the next item in the hash map, based on the current location
        of the iterator.
        """

        while True:
            try:
                entry = self._buckets.get_at_index(self._index)
            except DynamicArrayException:
                raise StopIteration

            self._index += 1
            if entry is not None and not entry.is_tombstone:
                return entry

    def _map_index(self, key: str) -> int:
        """
        This method takes a key and maps it to the appropriate index.
        :param key: An identifier key for an element.
        :return: The index to which the key maps.
        """

        return self._hash_function(key) % self.get_capacity()

    def _quadratic_probe(self, index:int, offset:int) -> int:
        """
        This method receives an index and a probing offset and calculates
        the next index in a quadratic sequence.
        :param index: The current index when this method is called.
        :param offset: The base integer value in a quadratic sequence.
        :return:
        """

        return (offset * offset + index) % self._capacity

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
