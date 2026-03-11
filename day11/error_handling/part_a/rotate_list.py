def rotate_list(lst, k):
    try:
        if not isinstance(lst, list):
            raise TypeError("Input 'lst' must be a list.")
        if not isinstance(k, int):
            raise TypeError("Input 'k' must be an integer.")
        
        n = len(lst)
        if n == 0:
            return lst
        k = k % n  # Normalize k for large values
        return lst[-k:] + lst[:-k]
    except TypeError as e:
        print(f"Type Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None

# Example usage
lst = [1, 2, 3, 4, 5]
k = 2
print(rotate_list(lst, k))

print(rotate_list([1,2,3,4,5], 7) )
print(rotate_list([1,2,3], 0)    )
print(rotate_list([], 3)         )
print(rotate_list([1], 10)     )
print(rotate_list([1,2,3,4,5], -2) )

print(rotate_list("not a list", 2) )
print(rotate_list([1,2,3], "not an int") )