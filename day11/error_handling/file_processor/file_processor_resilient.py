import os
import csv
import json
import time
import logging
import traceback


logging.basicConfig(
    filename="file_processor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

INPUT_DIR = "data"
REPORT_FILE = "processing_report.json"
MAX_RETRIES = 3
RETRY_DELAY = 1

# Function to process a CSV file
def process_csv(file_path):
    """
    Parses a CSV file and calculates basic structure metrics:
    - Number of rows
    - Number of columns
    - Detects corrupted files
    """

    total_rows = 0
    num_columns = 0
    corrupted = False
    corruption_reason = None

    try:
        with open(file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            first_row = True
            expected_columns = 0

            for row_num, row in enumerate(reader, start=1):
                if not row:
                    # Empty row - could be corruption or just empty
                    continue

                total_rows += 1

                # Determine column count from the first non-empty row
                if first_row:
                    expected_columns = len(row)
                    num_columns = expected_columns
                    first_row = False

                # Check for inconsistent column count (potential corruption)
                if len(row) != expected_columns:
                    corrupted = True
                    corruption_reason = f"Inconsistent columns at row {row_num}: expected {expected_columns}, got {len(row)}"
                    logging.warning(
                        f"Corruption detected in {file_path}: {corruption_reason}"
                    )
                    break

                # Check for obviously corrupted data (e.g., binary data in text field)
                for col_num, cell in enumerate(row):
                    try:
                        # Try to decode as UTF-8 to catch binary corruption
                        cell.encode("utf-8").decode("utf-8")
                    except (UnicodeDecodeError, UnicodeEncodeError):
                        corrupted = True
                        corruption_reason = f"Invalid character encoding at row {row_num}, column {col_num + 1}"
                        logging.warning(
                            f"Corruption detected in {file_path}: {corruption_reason}"
                        )
                        break

                if corrupted:
                    break

    except UnicodeDecodeError as e:
        corrupted = True
        corruption_reason = f"File encoding error: {str(e)}"
        logging.error(f"Encoding corruption in {file_path}: {corruption_reason}")
    except csv.Error as e:
        corrupted = True
        corruption_reason = f"CSV parsing error: {str(e)}"
        logging.error(f"CSV corruption in {file_path}: {corruption_reason}")
    except Exception as e:
        corrupted = True
        corruption_reason = f"Unexpected error: {str(e)}"
        logging.error(f"Unexpected corruption in {file_path}: {corruption_reason}")

    result = {"rows": total_rows, "columns": num_columns}

    if corrupted:
        result["corruption_reason"] = corruption_reason

    return result

# Function to process a file with retry logic for PermissionError
def process_with_retry(file_path):
    """
    Processes a file with retry logic for PermissionError.
    """
    attempts = 0

    while attempts < MAX_RETRIES:
        try:
            return process_csv(file_path)

        except PermissionError as e:
            attempts += 1
            logging.warning(f"PermissionError on {file_path}. Retry {attempts}")

            if attempts >= MAX_RETRIES:
                raise

            time.sleep(RETRY_DELAY)

        except Exception:
            raise


#  Main execution to process all files in the input directory and generate a report
def main():

    report = {
        "files_processed": [],
        "files_failed": [],
        "error_details": {},
    }

    if not os.path.isdir(INPUT_DIR):
        print(f"Directory '{INPUT_DIR}' does not exist.")
        return

    for filename in os.listdir(INPUT_DIR):

        if not filename.lower().endswith(".csv"):
            continue

        file_path = os.path.join(INPUT_DIR, filename)

        try:
            logging.info(f"Processing file: {filename}")

            result = process_with_retry(file_path)

            if "corruption_reason" in result:
                logging.warning(f"Corrupted file detected: {filename}")
                report["files_failed"].append({"file": filename, "result": result})
                report["error_details"][filename] = {
                    "error_type": "corruption",
                    "reason": result.get("corruption_reason", "Unknown corruption"),
                    "rows_processed": result.get("rows", 0),
                    "columns_detected": result.get("columns", 0),
                }
            else:
                report["files_processed"].append({"file": filename, "result": result})

        except Exception as e:
            logging.error(f"Failed processing {filename}")
            logging.error(traceback.format_exc())

            report["files_failed"].append({"file": filename, "error": str(e)})
            report["error_details"][filename] = {
                "error_type": "processing_error",
                "reason": str(e),
                "traceback": traceback.format_exc(),
            }

    # Export report
    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=4)

    print("Processing completed.")
    print(f"Report saved to {REPORT_FILE}")


if __name__ == "__main__":
    main()
