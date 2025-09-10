# Name: Christopher Vote
# Email: votec@oregonstate.edu
# Description: This program contains an implementation of a hash_map abstract data
#              type using single chaining. The hash table is implemented on a DynamicArray
#              data structure. Also included is a SinglyLinkedList data structure for collision
#              handling.
#              The hash_map contains the following public methods: get_size(), get_capacity,
#              put(), resize_table(), table_load(), empty_buckets(), get(), contains_key(),
#              remove(), get_keys_and_values(), and clear().
#              Also included in the file is an implementation of a find_mode() function, which
#              takes an array of values and determines the mode(s) among the elements and returns
#              this value or values, along with the attendant frequency of occurrence.
#              DynamicArray data structure and determines the mode of its values.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        This method takes a key and a value, and updates this particular key/value
        pair within the data structure.
        :param key: A key assigned to a value for purposes of efficient lookup.
        :param value: A value of an object in the hash_map.
        """

        if self.table_load() >= 1.0:
            self.resize_table(self.get_capacity() * 2)

        index = self._map_index(key)
        bucket = self._buckets.get_at_index(index)
        node = bucket.contains(key)

        if node is not None:
            node.value = value
        else:
            bucket.insert(key, value)
            self._size = self._size + 1

    def resize_table(self, new_capacity: int) -> None:
        """
        This method receives an integer representing the new desired size
        of the table, and executes the resizing.
        The method is responsible for maintaining the key/value pairs associated
        with the elements already in the hash_map. The new capacity must always
        be a prime number.
        :param new_capacity: The capacity to which the table is being resized. If
        it is not a prime number, the method will adjust the integer value of this
        parameter to the next prime number.
        """

        if new_capacity < 1:
            return
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        elements = self.get_keys_and_values()

        self._buckets = DynamicArray()
        for _ in range(new_capacity):
            self._buckets.append(LinkedList())

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
        return self._size / self._buckets.length()

    def empty_buckets(self) -> int:
        """
        This method provides a tally of the number of empty buckets
        currently present in the hash_map.
        :return: The number of empty buckets.
        """

        count = 0
        for i in range(self.get_capacity()):
            if self._buckets.get_at_index(i).length() == 0:
                count = count + 1
        return count

    def get(self, key: str) -> object:
        """
        This method returns a value associated with the key which has been
        passed to the method as a parameter. If the key does not exist in
        the hash_map, the method returns None.
        :param key: The key of the value being retrieved.
        :return: The value if it exists, otherwise None.
        """

        index = self._map_index(key)
        node = self._buckets.get_at_index(index).contains(key)
        return node.value if node else None

    def contains_key(self, key: str) -> bool:
        """
        This checks whether a particular key exists within the hash_map.
        :param key: A key being checked to determine if it is present.
        :return: True if the key is present, otherwise False.
        """

        return self._buckets.get_at_index(self._map_index(key)).contains(key) is not None

    def remove(self, key: str) -> None:
        """
        This method removes a value associated with a particular key in the
        hash map. If the key is not present, the method simply exits the operation.
        :param key: Key to be removed from the hashmap.
        """

        if self._buckets.get_at_index(self._map_index(key)).remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method retrieves the key/value pairs in the hash_map and
        returns them.
        :return: A DynamicArray containing the key/value in tuples of the form
        (key, value).
        """

        da = DynamicArray()
        for i in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(i)
            for node in bucket:
                da.append((node.key, node.value))
        return da

    def clear(self) -> None:
        """
        This method clears the contents of the hash map, while leaving the capacity of the
        hash map unchanged.
        """

        for i in range(self._buckets.length()):
            self._buckets.set_at_index(i, LinkedList())
        self._size = 0

    def _map_index(self, key):
        """
        This method takes a key and maps it to the appropriate index.
        :param key: An identifier key for an element.
        :return: The index to which the key maps.
        """

        return self._hash_function(key) % self.get_capacity()

def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    This function takes a DynamicArray and finds the mode among the values
    of the elements in the array. It returns a DynamicArray with the mode
    value(s) and an integer with the integer value of the number of occurrences
    of the mode.
    :param da: A DynamicArray with values.
    :return: A tuple containing a DynamicArray containing the mode value(s) and
    an integer representing the number of occurrences of the value.
    """

    map = HashMap()
    frequency = 0

    for i in range(da.length()):
        val = da.get_at_index(i)
        current = map.get(val)

        # On first pass for a given key, initialize its count to 1.
        if current is None:
            map.put(val, 1)
            count = 1

        # Maps all values to map.
        else:
            count = current + 1
            map.put(val, count)
        if count > frequency:
            frequency = count

    # Find the mode(s) and store the mode(s) in a DynamicArray.
    modes = DynamicArray()
    keyVal = map.get_keys_and_values()
    for i in range(keyVal.length()):
        if keyVal.get_at_index(i)[1] == frequency:
            modes.append(keyVal.get_at_index(i)[0])

    return modes, frequency


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
