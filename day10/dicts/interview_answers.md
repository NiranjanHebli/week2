## Q1 Conceptual


### Time Complexity

| Operation                 | Average Case | Worst Case |
| ------------------------- | ------------ | ---------- |
| Lookup (`d[key]`)         | O(1)         | O(n)       |
| Insert (`d[key] = value`) | O(1)         | O(n)       |
| Delete (`del d[key]`)     | O(1)         | O(n)       |


In the average case, these operations take constant time O(1) because Python uses a hash function to directly map a key to a specific index in an internal array. Instead of scanning through all elements like a list, Python computes the hash of the key and jumps directly to the memory location where the value should be stored.

The worst-case complexity becomes O(n) when many keys produce the same hash index, which is called a hash collision. When collisions occur, Python must probe other positions in the hash table to find the correct slot. If many collisions happen, Python may end up checking many entries, making the operation closer to linear time.

Python handles collisions using a technique called open addressing with probing, where it searches for the next available slot in the table. Although this situation is rare with good hash functions and resizing strategies, it is theoretically possible and leads to the worst-case complexity.

### How Python’s Hash Function Works

Python uses different hashing strategies depending on the data type of the key.

For integers, the hash function is very simple. In most cases, the integer value itself is used as the hash value (with small internal adjustments). This makes hashing integers extremely fast.

For strings, Python calculates the hash using a more complex algorithm that processes each character of the string. It combines the character codes using a polynomial-style computation to produce a single hash value. Additionally, Python adds random hash seeding to string hashing so that the hash values change between different program runs. This protects against deliberate collision attacks.

### When to Choose a dict Over a list

A dictionary should be chosen when fast key-based lookup is required. Dictionaries are ideal when you want to map one value to another, such as storing user IDs with user data, counting frequencies of words, or building lookup tables.

Lists are better suited for ordered collections where elements are accessed by their index position. Searching for an element in a list requires scanning through the list, which takes O(n) time, while dictionary lookups typically take O(1) time.


## Q2 Coding

### File link:- [group_anagrams.py](./group_anagrams.py)

Run using :-
```bash
python3 group_anagrams.py
```

## Q3 Debug 
The first issue occurs at freq[char] += 1. When a character appears for the first time, it is not yet present in the dictionary, so trying to increment it raises a KeyError. The dictionary must initialize the key with a value (such as 0) before incrementing.

The second issue is that sorted(freq, key=freq.get, reverse=True) returns only the dictionary keys, not the (character, frequency) pairs. To include the counts in the result, the code should sort freq.items() instead.

#### Corrected Code:-

```python

def char_freq(text):
    freq = {}
    
    for char in text:
        if char not in freq:      # Fix for Bug 1
            freq[char] = 0
        freq[char] += 1
    
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)  # Fix for Bug 2
    
    return sorted_freq
```
