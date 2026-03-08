from functools import wraps

def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


n = int(input("Enter a number: "))
if n < 0:
    print("Please enter a non-negative integer.")
else:
    print(f"Fibonacci of {n} is {fibonacci(n)}")