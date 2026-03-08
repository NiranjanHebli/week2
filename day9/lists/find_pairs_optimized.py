# Given a list of integers and a target sum, find all unique pairs of integers in the list that add up to the target sum.
def find_pairs(nums, target):
    """Find all unique pairs that sum to target."""
    seen = set()
    pairs = set()
    
    for num in nums:
        complement = target - num
        if complement in seen:
            if (num, complement) not in pairs and (complement, num) not in pairs:
                pairs.add((min(num, complement), max(num, complement)))
        seen.add(num)
    
    return list(pairs)

print(find_pairs([1, 2, 3, 4, 5], 6))  
print(find_pairs([1, 1, 1], 2))



