import csv
import json
from pathlib import Path
from datetime import datetime


# This function loads all CSV files from the data directory and returns a list of all rows and a list of filenames.
def load_csv_files():
    """
    Input: None
    Output: A tuple containing a list of all rows from the CSV files and a list of filenames.
    """
    all_rows = []
    files = list(Path(".").glob("data/data*.csv"))

    for file in files:
        with open(file, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_rows.append(row)

    return all_rows, files

# This function removes duplicate rows from a list of rows. A row is considered a duplicate if it has the same date, product, quantity and price as another row.
def remove_duplicates(rows):
    """
   Input: A list of rows, where each row is a dictionary containing the keys "date", "product", "qty", and "price".
   Output: A list of unique rows, where duplicates have been removed based on the combination of

    """
    unique = {}
    for r in rows:
        key = (r["date"], r["product"], r["qty"], r["price"])
        unique[key] = r
    return list(unique.values())

# This function calculates the revenue for each product in a list of rows. It returns a dictionary mapping each product to its revenue and the total revenue.
def calculate_revenue(rows):
    """
    Input: A list of rows, where each row is a dictionary containing the keys "date", "product", "qty", and "price".
    Output: A tuple containing a dictionary mapping each product to its revenue and the total revenue.
    """
    revenue = {}
    total_revenue = 0

    for r in rows:
        product = r["product"]
        qty = float(r["qty"])
        price = float(r["price"])
        rev = qty * price

        revenue[product] = revenue.get(product, 0) + rev
        total_revenue += rev

    return revenue, total_revenue

# This function exports the merged sales data to a CSV file. The function takes a list of rows as input, sorts them by date and writes them to a CSV file named "merged_sales.csv" in the "output" directory.
def export_csv(rows):
    """
    Input: A list of rows, where each row is a dictionary containing the keys "date", "product", "qty", and "price".
    Output: A CSV file named "merged_sales.csv" in the "output" directory, containing the merged sales data sorted by date.

    """
    rows.sort(key=lambda x: x["date"])

    with open("output/merged_sales.csv", "w", newline="") as f:
        fieldnames = ["date", "product", "qty", "price"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# This function exports a summary of the sales data to a JSON file. The function takes four parameters as input: a list of files processed, a list of rows processed, a dictionary mapping product to revenue, and the total revenue. It creates a JSON object containing metadata about the processing and the revenue by product, and writes it to a file named "revenue_summary.json" in the "output" directory.
def export_json(files, rows, revenue, total_revenue):
    """
    Input: - files: A list of files processed.
           - rows: A list of rows processed.
           - revenue: A dictionary mapping product to revenue.
           - total_revenue: The total revenue calculated from the rows.
    Output: A JSON file named "revenue_summary.json" in the "output" directory, containing metadata about the processing and the revenue by product.
    """
    output = {
        "metadata": {
            "files_processed": len(files),
            "total_rows": len(rows),
            "total_revenue": round(total_revenue, 2),
            "generated_at": datetime.now().isoformat()
        },
        "revenue_by_product": {k: round(v, 2) for k, v in revenue.items()}
    }

    with open("output/revenue_summary.json", "w") as f:
        json.dump(output, f, indent=2)


# Main function to run the sales data pipeline. It loads the CSV files, removes duplicates, calculates revenue, and exports the results to CSV and JSON files.
def main():
    
    rows, files = load_csv_files()
    unique_rows = remove_duplicates(rows)
    revenue, total_revenue = calculate_revenue(unique_rows)

    export_csv(unique_rows)
    export_json(files, unique_rows, revenue, total_revenue)

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()