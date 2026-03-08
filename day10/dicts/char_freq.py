def char_freq(text):
    freq = {}
    
    for char in text:
        if char not in freq:      # Fix for Bug 1
            freq[char] = 0
        freq[char] += 1
    
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)  # Fix for Bug 2
    
    return sorted_freq


# Example usage
input_text = "banana"
print(char_freq(input_text))