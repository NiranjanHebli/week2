import json
import logging

# Create logger
logger = logging.getLogger("json_loader")
logger.setLevel(logging.DEBUG)

# Create file handler
file_handler = logging.FileHandler("json_loader.log")
file_handler.setLevel(logging.DEBUG)

# Log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)

# Attach handler to logger
logger.addHandler(file_handler)


# Function to safely load a JSON file
def safe_json_load(filepath: str):
    """
    Safely load a JSON file with proper exception handling.

    Returns:
        dict | None
    """
    try:
        with open(filepath, "r") as f:
            data = json.load(f)

    except FileNotFoundError as e:
        logger.error(f"File not found: {filepath} | {e}")
        print("Error: File not found")
        return None

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in {filepath} | {e}")
        print("Error: Invalid JSON format")
        return None

    except PermissionError as e:
        logger.error(f"Permission denied: {filepath} | {e}")
        print("Error: Permission denied")
        return None

    except Exception as e:
        logger.error(f"Unexpected error while reading {filepath}: {e}")
        print("Unexpected error occurred")
        return None

    else:
        logger.info(f"Successfully loaded JSON file: {filepath}")
        return data

    finally:
        logger.info(f"Attempted read operation on: {filepath}")


# Example run
if __name__ == "__main__":
    result = safe_json_load("config.json")

    if result:
        print("JSON Loaded Successfully")
        print(result)
    else:
        print("Failed to load JSON")