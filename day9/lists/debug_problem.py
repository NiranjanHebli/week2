nums = [2,4,6,8]

## Old solution - This will skip some even numbers due to the way the list is modified during iteration.
for num in nums:
    if num % 2 == 0:
        nums.remove(num)

print(nums)

## New solution - This creates a new list with only odd numbers, preserving the original list.
nums = [2,4,6,8]
nums = [num for num in nums if num % 2 != 0]
print(nums)