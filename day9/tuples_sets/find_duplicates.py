# A function to find duplicates in a list using sets.
def find_duplicates(lst):
    seen = set()
    duplicates = set()
    
    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
            
    return duplicates

my_list = [1, 2, 3, 4, 2, 5, 1, 6]
print(find_duplicates(my_list))
