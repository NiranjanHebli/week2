import csv
import json
from pathlib import Path


def csv_to_json(input_file, output_file):
    """
    Convert a CSV file to JSON while automatically detecting the delimiter.
    Supported delimiters: comma, tab, semicolon, pipe.
    """

    try:
        input_path = Path(input_file)

        # Check if file exists
        if not input_path.exists():
            print("Error: CSV file not found.")
            return

        # Check if file is empty
        if input_path.stat().st_size == 0:
            print("Error: CSV file is empty.")
            return

        # Read a sample of the file to detect delimiter
        with open(input_file, "r", newline="") as f:
            sample = f.read(2048)

            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample, delimiters=[",", "\t", ";", "|"])
            f.seek(0)

            # Use DictReader so headers become JSON keys
            reader = csv.DictReader(f, dialect=dialect)

            data = []

            # Convert each row into a dictionary
            for row in reader:
                data.append(row)

        # Write JSON output
        with open(output_file, "w") as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Conversion successful: {output_file}")

    except csv.Error:
        print("Error: Could not detect CSV delimiter.")
    except Exception as e:
        print(f"Unexpected error: {e}")


# Example usage
if __name__ == "__main__":
    csv_to_json("data/input.csv", "output/output.json")
