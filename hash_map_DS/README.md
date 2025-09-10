# Hash Map Implementations in Python

This repository contains two complete hash map implementations built on top of
a minimal data structures module:

- **`hash_map_sc.py`** — Separate Chaining hash map (linked lists for collisions)
- **`hash_map_oa.py`** — Open Addressing hash map (quadratic probing with tombstones)
- **`a6_include.py`** — Provided scaffolding (`DynamicArray`, `LinkedList`, `HashEntry`,
  and sample hash functions)

---

## Features

- Prime number capacities with automatic resizing
- Consistent public API across both versions:
  - `put(key, value)`
  - `get(key)`
  - `remove(key)`
  - `contains_key(key)`
  - `get_keys_and_values() -> DynamicArray[(key, value)]`
  - `table_load()`
  - `empty_buckets()`
  - `clear()`
  - `get_size()`, `get_capacity()`
- **SC version** includes `find_mode()` — computes the statistical mode(s) of a `DynamicArray`
- **OA version** supports iteration over live entries (`for entry in HashMap: ...`)

---

## Quickstart

Clone and run:

```bash
git clone <your-repo-url> hashmap
cd hashmap

# Run built-in demonstrations
python3 hash_map_sc.py
python3 hash_map_oa.py

