# Q1 Conceptual


### Json.load()

- json.load() is a function from Python’s json module used to read JSON data directly from a file object and convert it into a Python data structure such as a dictionary or list. It expects a file that has already been opened using functions like open().

- When should it be used:-
This function should be used when the JSON data is stored in a file, such as configuration files, API response files saved locally, or data exchange files.

- Example:
In a real-world scenario, an application may store settings in a config.json file. The program can read that file and convert it into a Python dictionary using json.load().

### Python Code:-

```python
import json

with open("config.json", "r") as file:
    config = json.load(file)

print(config["database"])
```

### Json.loads()

- json.loads() is used to convert a JSON formatted string into a Python object such as a dictionary or list. The “s” in loads stands for string, meaning it works with JSON data that already exists as a string in memory rather than in a file.

- When should it be used:-
This function should be used when JSON data is received as a string, such as from a web API response, message queue, or user input.

- Example:
In a real-world case, when a program receives data from a web API, the response is often returned as a JSON string. json.loads() can convert that string into a Python dictionary so it can be processed easily.

### Python Code:-

```python
import json

json_string = '{"product": "Laptop", "price": 75000}'

data = json.loads(json_string)

print(data["product"])
```


# Q2 Coding 


### File link :- [Large File Finder](./large_file_finder/find_large_files.py)


# Q3 Debug 

### Bug 1: Missing Import for csv

The code uses the csv module but does not import it. This will cause a NameError when the program runs.

- Fix: Add import csv at the beginning of the script.

### Bug 2: Header Rows Will Be Duplicated

Each CSV file usually contains a header row. The current code reads every row from every file, so the header from each file will be appended, leading to multiple headers in the merged file.

- Fix: Read the header only from the first file and skip it for the remaining files.

### Bug 3: Missing newline="" When Writing CSV

When writing CSV files in Python, the file should be opened with newline="". Without this, extra blank lines may appear in the output file on some systems.

- Fix: Use open("merged.csv", "w", newline="")

Corrected Code:- [Debugged Code](./debugged_solution/debug_code.py)