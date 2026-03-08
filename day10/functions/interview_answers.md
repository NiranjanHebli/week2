## Q1 Conceptual

### LEGB Rule in Python

### 1. What is the LEGB Rule?

The **LEGB rule** defines how Python resolves variable names. Python searches for variables in the following order:

| Level | Scope | Description |
|------|------|-------------|
| **L** | Local | Variables defined inside the current function |
| **E** | Enclosing | Variables in the outer function (for nested functions) |
| **G** | Global | Variables defined at the module level |
| **B** | Built-in | Python built-in names like `len`, `print`, etc. |

Python searches **Local → Enclosing → Global → Built-in**.

---

### 2. Example

```python
x = 10   # Global scope

def outer():
    x = 20   # Enclosing scope
    
    def inner():
        x = 30   # Local scope
        print(x)
    
    inner()

outer()
```

### 3. Scope Diagram

```
Built-in Scope
   ^
Global Scope
   x = 10
   ^
Enclosing Scope (outer)
   x = 20
   ^
Local Scope (inner)
   x = 30

```

### 4. Variable in Both Local and Global Scope

If the same variable exists in both scopes, the local variable shadows the global variable.

### 5. What the global Keyword Does

The global keyword allows a function to modify a global variable. The global keyword is used to declare a variable as global in the local scope of a function. It is used to indicate that the variable is defined in the global scope, and the function can modify it.

Example:-

```python
x = 5

def modify():
    global x
    x = 20

modify()
print(x)

```

Output :- `20`


### 6. Why global is Considered a Code Smell

Using global is discouraged because:

- Creates hidden dependencies

- Makes code harder to debug

- Reduces function modularity

- Causes unexpected side effects when multiple functions modify the same variable

### 7. Better Alternative

Use function parameters and return values instead of modifying globals.

```python
def modify(x):
    return x + 15

x = 5
x = modify(x)

print(x)
```

## Q2 Coding

### File Link:- 

[`memoize.py`](memoize.py):-
This program contains a decorator that caches the results of a function so that if the function is called again with the same arguments, it returns the cached result instead of calculating the result again.

## Q3 Debug/Analyze

```python 
total = 0

def add_to_cart(item, cart=None):
    global total # Fix for scope issue
    
    if cart is None:          # Fix for mutable default argument
        cart = []
    
    cart.append(item)
    total = total + len(cart) 
    
    return cart


print(add_to_cart('apple'))
print(add_to_cart('banana'))
```