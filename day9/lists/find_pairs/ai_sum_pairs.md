## Sum Pairs

This program takes a list of integers and a target sum, and returns all unique pairs of integers in the list that sum to the target.


Example usage:
```
nums = [1, 2, 3, 4, 5]
target = 6

print(find_pairs(nums, target))
```
```
Output: 
[(1, 5), (2, 4)]
```

### Prompt:-

```
Write a Python function `find_pairs(nums, target)` that returns all unique pairs of numbers from the input list `nums` which sum exactly to `target`, using only list comprehensions.

Requirements:
- Input: `nums = [1, 2, 3, 4, 5, 7]`, `target = 9`
- Output: `[(4, 5), (2, 7)]` (pairs as tuples, order doesn't matter)
- Return empty list `[]` if no pairs found
- Handle duplicates and ensure each pair appears only once
- Use list comprehension only (no loops)
```

### AI - Generated Code:- 
```python
def find_pairs(nums, target):
    """Find all unique pairs that sum to target using list comprehension only."""
    return [(nums[i], nums[j]) for i in range(len(nums)) 
            for j in range(i+1, len(nums)) 
            if nums[i] + nums[j] == target]
```

**file link** :- [find_pairs.py](find_pairs.py)

#### Duplicates Pairs?
Yes, the AI generated code gave output as duplicate pairs

#### Incorrect Logic?
Yes, It had an incorrect logic since it didnt verify for duplicate pairs.

**optimized code link:-** [find_pairs_optimized.py](find_pairs_optimized.py)

### Key changes made:- 
- Two new data structures: Added hash set for tracking seen numbers + second set for unique pairs

- Single pass algorithm: Replaced nested index loops with one linear traversal

- Complement lookup: Calculates target - current and checks if previously seen (O(1))

- Bidirectional duplicate check: Verifies both pair orders exist before adding


### Output Screenshot:- 



### Time Complexity

The time complexity of this program is O(n), where n is the length of the input list. This is because the program iterates over the list once to build the hash set of seen numbers, and then iterates over the list again to find the pairs that sum to the target.



### Analysis:- 

The second version of find_pairs represents significant improvements over the first across multiple dimensions. Most critically, it reduces time complexity from O(n^2) in the list comprehension version which relies on nested loops over all index pairs to O(n) by using a single pass with a hash set to track seen numbers and their complements.This makes it dramatically more efficient for large lists, scaling linearly instead of quadratically.

 Additionally, it properly handles duplicate pairs by maintaining a separate pairs set that checks both (num, complement) and (complement, num) before adding, ensuring value-based uniqueness rather than index-based repetition; for example, with [1, 4, 4, 5] and target 9, the first version might return [(4,5), (4,5)] while the second returns only [(4,5)]. It also introduces canonical pair ordering via min(num, complement) and max(num, complement), guaranteeing consistent sorted tuples regardless of traversal order.