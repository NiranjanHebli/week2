import csv


def merge_csv_files(file_list):
    all_data = []
    header_saved = False

    for filename in file_list:
        with open(filename, "r", newline="") as f:
            reader = csv.reader(f)

            if not header_saved:
                header = next(reader)
                all_data.append(header)
                header_saved = True
            else:
                next(reader)  # skip header in other files

            for row in reader:
                all_data.append(row)

    with open("merged.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(all_data)

    return len(all_data)


file_list = ["data/data1.csv", "data/data2.csv", "data/data3.csv"]
num_rows = merge_csv_files(file_list)
print(f"Merged {num_rows} rows into 'merged.csv'")
