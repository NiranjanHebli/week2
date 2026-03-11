## Prompt:- 

Write a Python decorator called @retry that retries a function if it raises an exception.

Requirements:
1. The decorator should accept two parameters:
   - max_attempts (default = 3): maximum number of retry attempts.
   - delay (default = 1): initial delay in seconds before retrying.

2. Implement exponential backoff:
   - After each failed attempt, the delay should double.
   - Example: 1s → 2s → 4s → ...

3. The decorator should:
   - Catch exceptions raised by the wrapped function.
   - Retry the function until max_attempts is reached.
   - Wait using time.sleep() between retries.
   - Raise the last exception if all attempts fail.

4. Use functools.wraps to preserve the original function metadata.

5. Include:
   - Proper type hints
   - A clear docstring
   - A short example demonstrating usage of the decorator.


AI - Generated Code :- 

```python 
import time
from functools import wraps
from typing import Callable, TypeVar, Any, cast

F = TypeVar("F", bound=Callable[..., Any])

def retry(max_attempts: int = 3, delay: float = 1) -> Callable[[F], F]:
    """
    Decorator that retries a function if it raises an exception.

    Args:
        max_attempts (int): Maximum number of attempts before giving up.
        delay (float): Initial delay (in seconds) before retrying.

    Behavior:
        - Retries the wrapped function when an exception occurs.
        - Uses exponential backoff: delay doubles after each failed attempt.
        - Waits using time.sleep() between retries.
        - Raises the last exception if all attempts fail.

    Returns:
        Callable: The wrapped function with retry logic applied.
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            last_exception: Exception | None = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == max_attempts:
                        break
                    time.sleep(current_delay)
                    current_delay *= 2  # Exponential backoff

            if last_exception:
                raise last_exception

        return cast(F, wrapper)

    return decorator


# Example usage
@retry(max_attempts=3, delay=1)
def unstable_function() -> str:
    """Function that randomly fails to demonstrate retry behavior."""
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure occurred!")
    return "Success!"


if __name__ == "__main__":
    print(unstable_function())

```

### File Link:-  [retry_decorator.py](./ai_augmented/retry_decorator.py)


### 1. Does the decorator handle edge cases?
The decorator handles some basic edge cases, such as retrying a function multiple times and raising the last exception if all attempts fail. It also correctly implements exponential backoff by doubling the delay after each failed attempt. However, it does not validate input parameters such as max_attempts or delay. If max_attempts is set to 0 or a negative value, the retry loop may behave incorrectly. Similarly, negative delay values could cause unexpected behavior. It also does not explicitly handle cases such as keyboard interruption or extremely large delays.

###  2. Does it preserve function metadata using functools.wraps?
Yes, the decorator correctly uses functools.wraps on the wrapper function. This ensures that the wrapped function preserves important metadata such as the original function name, docstring, annotations, and module information. Preserving metadata is important for debugging, documentation generation, and introspection tools.

### 3. Does it distinguish between retryable vs non-retryable exceptions?
No, the decorator currently catches all exceptions using a broad except Exception clause. This means it retries even for errors that are unlikely to succeed on retry, such as invalid arguments or programming mistakes. Ideally, the decorator should allow specifying a tuple of retryable exceptions.

### 4. What improvements would you make?
I would add parameter validation, support for specifying retryable exception types, optional logging of retry attempts, and possibly a maximum backoff limit to prevent excessively long delays.