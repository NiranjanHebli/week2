def jaccard_similarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    if len(union) == 0:
        return 0
    
    return len(intersection) / len(union)


# Example
set_a = {"python", "ai", "machine learning", "data"}
set_b = {"python", "data", "deep learning", "statistics"}

score = jaccard_similarity(set_a, set_b)
print("Jaccard Similarity:", score)


set_d = {}
set_c = {"python", "data"}

score_empty = jaccard_similarity(set_c, set_d)
print("Jaccard Similarity with empty set:", score_empty)


# Error 
# set_c = {}
# set_d = {"python", "data"}

# score_empty = jaccard_similarity(set_c, set_d)
# print("Jaccard Similarity with empty set:", score_empty)

# Error 

# set_c = {}
# set_d = {}

# score_empty = jaccard_similarity(set_c, set_d)
# print("Jaccard Similarity with empty set:", score_empty)

