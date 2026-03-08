## Prompt:- 

Write a Python module containing a function analyze_text(text: str, *args, **options) that analyzes input text based on optional keyword arguments: count_words, count_sentences, find_longest_word, and sentiment_simple. Each option should trigger the corresponding analysis. Use *args and **kwargs, include proper type hints and Google-style docstrings, and return a dictionary containing all requested analysis results.

## AI - Generated Code:-


```python
from typing import Any, Dict


def analyze_text(text: str, *args: str, **options: bool) -> Dict[str, Any]:
    """
    Perform configurable text analysis.

    Args:
        text (str): Input text to analyze.
        *args (str): Additional words to include in the analysis.
        **options (bool): Flags enabling analyses:
            count_words, count_sentences, find_longest_word, sentiment_simple.

    Returns:
        Dict[str, Any]: Results of the requested analyses.
    """
    words = text.split()
    if args:
        words.extend(args)

    results: Dict[str, Any] = {}

    if options.get("count_words", False):
        results["word_count"] = len(words)

    if options.get("count_sentences", False):
        results["sentence_count"] = sum(text.count(p) for p in ".!?")

    if options.get("find_longest_word", False):
        results["longest_word"] = max(words, key=len) if words else None

    if options.get("sentiment_simple", False):
        positive = {"good", "great", "happy", "excellent", "love"}
        negative = {"bad", "sad", "terrible", "hate", "poor"}

        score = sum(1 for w in words if w.lower() in positive) - \
                sum(1 for w in words if w.lower() in negative)

        if score > 0:
            results["sentiment"] = "positive"
        elif score < 0:
            results["sentiment"] = "negative"
        else:
            results["sentiment"] = "neutral"

    return results
```


### Does it properly use **kwargs?
Yes, it correctly accesses options using options.get() which is the standard way to safely read keyword arguments.

### Are type hints correct?
 Yes, the type hints (str, *args: str, **options: bool, Dict[str, Any]) are appropriate for the function’s inputs and output.

### Does it handle edge cases (empty text, no options)? 
Yes, it handles empty text and missing options without errors by using safe checks like if words and default False in options.get().

### Is the docstring actually useful or just boilerplate?
 The docstring is useful because it clearly explains parameters, options, and the returned result.

### Does the function follow Single Responsibility Principle or is it doing too much?
 It slightly violates the Single Responsibility Principle because it performs multiple analyses instead of delegating them to smaller helper functions.


 ### Improvised Version

 File Link :- [analyze_text.py](./analyze_text.py)