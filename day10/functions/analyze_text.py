from typing import Dict, Any, List


def count_words(words: List[str]) -> int:
    """Return the number of words."""
    return len(words)


def count_sentences(text: str) -> int:
    """Return the number of sentences."""
    return sum(text.count(p) for p in ".!?")


def find_longest_word(words: List[str]) -> str:
    """Return the longest word."""
    return max(words, key=len) if words else None


def sentiment_simple(words: List[str]) -> str:
    """Return a simple sentiment classification."""
    positive = {"good", "great", "happy", "excellent", "love"}
    negative = {"bad", "sad", "terrible", "hate", "poor"}

    score = sum(1 for w in words if w.lower() in positive) - \
            sum(1 for w in words if w.lower() in negative)

    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"


def analyze_text(text: str, *args: str, **options: bool) -> Dict[str, Any]:
    """
    Perform configurable text analysis.

    Args:
        text: Input text.
        *args: Extra words to include in analysis.
        **options: Analysis flags (count_words, count_sentences,
                   find_longest_word, sentiment_simple).

    Returns:
        Dictionary containing requested analysis results.
    """
    words: List[str] = text.split()
    if args:
        words.extend(args)

    results: Dict[str, Any] = {}

    if options.get("count_words"):
        results["word_count"] = count_words(words)

    if options.get("count_sentences"):
        results["sentence_count"] = count_sentences(text)

    if options.get("find_longest_word"):
        results["longest_word"] = find_longest_word(words)

    if options.get("sentiment_simple"):
        results["sentiment"] = sentiment_simple(words)

    return results

# Example usage:
if __name__ == "__main__":
    sample_text = "I love programming! It's great, but sometimes it can be bad."
    analysis = analyze_text(sample_text, count_words=True, count_sentences=True,
                            find_longest_word=True, sentiment_simple=True)
    print(analysis)
