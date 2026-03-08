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


### Output Screenshot:- 



### Time Complexity

The time complexity of this program is O(n), where n is the length of the input list. This is because the program iterates over the list once to build the hash set of seen numbers, and then iterates over the list again to find the pairs that sum to the target.

