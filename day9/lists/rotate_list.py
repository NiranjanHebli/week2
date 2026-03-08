def rotate_list(lst, k):
    n = len(lst)
    if n == 0:
        return lst
    k = k % n  # Normalize k for large values
    return lst[-k:] + lst[:-k]

# Example usage
lst = [1, 2, 3, 4, 5]
k = 2
print(rotate_list(lst, k))

print(rotate_list([1,2,3,4,5], 7) )
print(rotate_list([1,2,3], 0)    )
print(rotate_list([], 3)         )
print(rotate_list([1], 10)     )
print(rotate_list([1,2,3,4,5], -2) )
