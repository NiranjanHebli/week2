"""
decorators.py
Three decorators built from scratch: @timer, @logger, @retry
"""

import time
import functools


def timer(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start  = time.time()
        result = fn(*args, **kwargs)
        print(f"[timer] {fn.__name__}() took {time.time() - start:.4f}s")
        return result
    return wrapper


def logger(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        all_args = ", ".join(
            [repr(a) for a in args] +
            [f"{k}={v!r}" for k, v in kwargs.items()]
        )
        print(f"[logger] calling {fn.__name__}({all_args})")
        result = fn(*args, **kwargs)
        print(f"[logger] {fn.__name__} returned {result!r}")
        return result
    return wrapper



def retry(max_attempts=3):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    print(f"[retry] {fn.__name__}() attempt {attempt}/{max_attempts} failed -- {exc}")
                    if attempt == max_attempts:
                        raise
        return wrapper
    return decorator




@timer
def slow_sum(n):
    time.sleep(0.05)
    return sum(range(n))


@logger
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


_attempts = {"count": 0}

@retry(max_attempts=3)
def flaky_call():
    _attempts["count"] += 1
    if _attempts["count"] < 3:
        raise ConnectionError(f"Server not ready (attempt {_attempts['count']})")
    return "success"


if __name__ == "__main__":
    print("--- @timer ---")
    print(slow_sum(1000))

    print("\n--- @logger ---")
    greet("Amit")
    greet("Priya", greeting="Namaste")

    print("\n--- @retry ---")
    print(flaky_call())