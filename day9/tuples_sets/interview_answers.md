## Q1 Conceptual


### Why it works or fails
The statement t[0][0] = 99 works even though t is a tuple. A tuple in Python is immutable, meaning its elements cannot be reassigned or replaced once the tuple is created. However, in this case the elements stored inside the tuple are lists, and lists are mutable objects. When we execute t[0][0] = 99, we are not attempting to replace the element at index 0 of the tuple. Instead, we are modifying the first element of the list that is stored inside the tuple. Since lists allow modification of their contents, the value changes successfully from [1,2] to [99,2]

### What this reveals about tuple immutability

This behavior reveals an important concept about tuple immutability. The immutability of a tuple applies only to the tuple’s structure, meaning the references to the objects it contains cannot be changed. For example, attempting t[0] = [9,9] would fail because it tries to replace the list stored at that position. However, if the objects inside the tuple are mutable (like lists, dictionaries, or sets), their internal values can still be modified. Therefore, tuples prevent reassignment of their elements, but they do not prevent changes to the mutable objects stored within them

## Q2 Coding - Find Duplicates


### File:-
[find_duplicates.py](./find_duplicates.py)

### Code:- 

```python 
def find_duplicates(lst):
    seen = set()
    duplicates = set()
    
    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
            
    return duplicates
```

### Time Complexity :-  O(n)

## Q3 Debug Problem 

### Why this happens

The function returns [1,2] because it uses the set difference operation set(a) - set(b). This operation only returns elements that exist in a but not in b. In the example unique_to_each([1,2,3], [3,4,5]), the expression set(a) - set(b) becomes {1,2,3} - {3,4,5}, which results in {1,2}. However, the requirement is to return elements unique to each list, meaning elements that appear in either list but not in both. The current code only considers one direction of difference and ignores elements that are in b but not in a.

#### Fixed function:-

To get elements unique to each list, we should use the symmetric difference between the two sets.

```python
def unique_to_each(a, b):
    result = set(a) ^ set(b)
    return list(result)
```

The ^ operator (symmetric difference) returns elements present in either set but not in both, which correctly produces [1,2,4,5] for the given test case.