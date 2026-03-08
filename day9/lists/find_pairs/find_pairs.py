def find_pairs(nums, target):
    """Find all unique pairs that sum to target using list comprehension only."""
    return [(nums[i], nums[j]) for i in range(len(nums)) 
            for j in range(i+1, len(nums)) 
            if nums[i] + nums[j] == target]


print(find_pairs([1, 2, 3, 4, 5], 6))  
print(find_pairs([1, 1, 1], 2))