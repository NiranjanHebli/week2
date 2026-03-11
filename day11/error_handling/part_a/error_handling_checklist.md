## [Finance Calculator](./finance_calculator.py)

### 1. Which Exceptions Are Caught

- ValueError is raised when invalid inputs are provided (e.g., empty name, negative salary, invalid tax rate, or savings rate outside 0–100%).

- Generic Exception is caught to handle unexpected runtime errors during input collection or calculations.

- KeyboardInterrupt is caught in the main function when the user manually stops the program using Ctrl + C.

- Validation errors inside get_employee_data() trigger exceptions that prevent incorrect financial calculations.

### 2. What Recovery Action Is Taken

- If a ValueError occurs, the function returns None, preventing invalid employee data from being used.

- The main program checks for None values and exits safely if employee data collection fails.

- For unexpected exceptions, the program prints an error message and stops execution to avoid incorrect outputs.

- When KeyboardInterrupt occurs, the program exits gracefully instead of crashing.

### 3. What the User Sees

- For invalid inputs, the user sees clear messages such as “Input Error: Salary cannot be negative.”

- If an unexpected issue occurs, the user sees “Unexpected Error: <error message>.”

- If data collection fails, the user sees “Failed to collect employee data. Exiting.”

- If the user interrupts execution, the message “Program interrupted by user.” is displayed.

### 4. What Gets Logged Internally

- The program does not currently implement a logging system.

- Errors are only printed to the console for visibility.


## [Rotate List](./rotate_list.py)

### 1. Which Exceptions Are Caught

- TypeError is raised when the input lst is not a list or when k is not an integer.

- Generic Exception is used as a fallback to catch any unexpected runtime errors during execution.

- The function explicitly validates input types before performing the rotation logic.

- Edge cases such as empty lists or very large rotation values are handled through logical checks rather than exceptions.

### 2. What Recovery Action Is Taken

- When a TypeError occurs, the function catches it and returns None to prevent further incorrect operations.

- For any unexpected exceptions, the function also returns None after displaying an error message.

- If the list is empty, the function safely returns the empty list without performing rotation.

- For large rotation values, the function normalizes k using modulo (k % n) to keep rotation within valid bounds.

### 3. What the User Sees

- If incorrect types are provided, the user sees messages like “Type Error: Input 'lst' must be a list.”

- If k is not an integer, the user sees “Type Error: Input 'k' must be an integer.”

- For unexpected errors, the user sees “Unexpected Error: [Error Message]”

- For valid inputs, the rotated list is printed as the function output.

### 4. What Gets Logged Internally

- The program does not currently implement internal logging.

- Error messages are printed directly to the console.


## [Password Analyzer](./password_analyzer/password_analyzer.py)

### 1. Which Exceptions Are Caught

- TypeError is caught in analyze_password() when the password input is not a string.

- ValueError is caught in generate_password() when the password length is not a positive integer.

- ValueError is also caught when converting user input to an integer for password length in the menu.

- KeyboardInterrupt is caught in the main program to handle user interruption using Ctrl + C.

- A generic Exception handler is included in multiple functions and the main loop to catch unexpected runtime errors.

### 2. What Recovery Action Is Taken

- When a TypeError occurs in password analysis, the function returns a score of 0 and a list containing "invalid input".

- When a ValueError occurs during password generation, the function returns None to indicate failure.

- If invalid numeric input is provided for password length, the program asks the user to enter a valid number.

- When KeyboardInterrupt occurs, the program exits gracefully instead of crashing.

- For unexpected exceptions, the program stops the current operation while logging the error.

### 3. What the User Sees

- If the password input type is incorrect, the user sees “Error: Password must be a string.”

- If an invalid password length is entered, the user sees “Invalid input. Please enter a valid number for password length.”

- If password generation fails, the message “Failed to generate password. Please try again.” is displayed.

- If the user interrupts execution, the program shows “Program interrupted by user.”

- The user also sees password strength scores and suggestions for missing criteria.

### 4. What Gets Logged Internally

- All password analyses are logged with score and missing criteria in password_analyzer.log.

- Errors such as TypeError, ValueError, and unexpected exceptions are logged with error severity.

- User menu selections and password generation events are logged as informational entries.

- Invalid inputs are recorded as warning logs to help with debugging and monitoring user behavior.

- Program exits and interruptions are also recorded in the log file.