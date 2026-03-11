# Q1 Conceptual

# Execution Flow 

In Python, `try`, `except`, `else`, and `finally` are used for **exception handling**.  
They help prevent programs from crashing and allow controlled error handling.

---

## 1. When Each Block Executes

## try
- The `try` block contains code that **might raise an exception**.
- Python always **executes this block first**.
- If an exception occurs, Python immediately stops execution in `try` and looks for a matching `except` block.

**Execution:** Always runs first.

---

## except
- The `except` block runs **only when an exception occurs in the try block**.
- It handles the error so the program can continue safely.

**Execution:** Runs only if an exception happens in `try`.

---

## else
- The `else` block executes **only if no exception occurs in the try block**.
- It is used for code that should run **after successful execution of try**.

**Execution:** Runs after `try` if no exception occurs.

---

## finally
- The `finally` block **always executes**, regardless of whether an exception occurred or not.
- Typically used for **cleanup operations**.

Common uses:
- closing files
- releasing resources
- database connections

**Execution:** Always runs last.

---

##  2. Example Using All Four Blocks


```python
try:
    print("Trying to divide numbers")

    a = int(input("Enter numerator: "))
    b = int(input("Enter denominator: "))

    result = a / b

except ZeroDivisionError:
    print("Error: Cannot divide by zero.")

except ValueError:
    print("Error: Invalid input.")

else:
    print("Division successful!")
    print("Result:", result)

finally:
    print("Execution finished.")
```

## 3. What Happens if an Exception Occurs in the else Block?

If an exception occurs inside the else block:

- The except block will NOT handle it.

- except only catches exceptions that occur in the try block.

- Python will still execute the finally block.

- After that, the program raises the exception normally.



# Q2 - Coding 

### File Link:- [`safe_json_loader.py`](./coding_problem/safe_json_loader.py)

# Q3 - Debug 

## Bug 1: Bare except Block

- The code uses a bare except:, which catches all exceptions.

- This includes critical exceptions like KeyboardInterrupt and SystemExit, which should normally terminate the program.

- Catching everything makes debugging difficult because the real error type is hidden.

- Fix: Replace the bare except with specific exceptions such as ValueError or TypeError.

## Bug 2: return Inside finally

- The finally block contains return results.

- A finally block always executes, regardless of whether an exception occurs or not.

- Because of this, the function returns during the first loop iteration, stopping the loop early.

- Fix: Remove the return from the finally block and place it after the loop finishes

## Bug 3: Non-Informative Error Message

- The code prints a generic message: "Error occurred".

- This message does not indicate:

    - which input item caused the error

    - what type of error happened.

- Lack of information makes debugging and troubleshooting difficult.

- Fix: Print a detailed message including the item and the exception.

## Corrected Code:

```python
def process_data(data_list):
    results = []

    for item in data_list:
        try:
            value = int(item)
            results.append(value * 2)

        except ValueError as e:  # Fix 1: Replace bare except with specific exception (ValueError)
            print(f"ValueError: Cannot convert '{item}' to integer. {e}")  # Fix 3: Provide informative error message

        except TypeError as e:  # Fix 1: Handle specific TypeError instead of catching everything
            print(f"TypeError: Invalid type for '{item}'. {e}")  # Fix 3: Include item and error details

    return results  # Fix 2: Move return outside loop and remove it from finally to avoid premature termination
```