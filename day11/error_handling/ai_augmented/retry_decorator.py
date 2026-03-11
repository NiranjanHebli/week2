import time
from functools import wraps
from typing import Callable, TypeVar, Any, cast

F = TypeVar("F", bound=Callable[..., Any])

# This module defines a retry decorator that can be applied to any function to automatically retry it upon failure.
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
@retry(max_attempts=5, delay=1)
def unstable_function() -> str:
    """Function that randomly fails to demonstrate retry behavior."""
    import random
    random_value = random.random()
    print(f"Generated random value: {random_value}")
    if random_value < 0.7:
        raise ValueError("Random failure occurred!")
    return "Success!"

if __name__ == "__main__":
    print(unstable_function())
