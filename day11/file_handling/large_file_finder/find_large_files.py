from pathlib import Path


# This function searches recursively for files larger than a specified size in megabytes within a given directory. It returns a list of tuples containing the filenames and their sizes in megabytes, sorted by size in descending order.
def find_large_files(directory, size_mb):
    """
    Search recursively for files larger than the given size (in MB).

    Args:
        directory (str or Path): Directory to search.
        size_mb (float): Minimum file size in megabytes.

    Returns:
        list of tuples: [("filename", size_in_mb)] sorted by size descending.
    """

    path = Path(directory)
    threshold = size_mb * 1024 * 1024
    results = []

    for file in path.rglob("*"):
        if file.is_file():
            size_bytes = file.stat().st_size
            if size_bytes > threshold:
                size_in_mb = round(size_bytes / (1024 * 1024), 2)
                results.append((file.name, size_in_mb))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


# files = find_large_files("data", 5)
files = find_large_files("data", 1)
# print(files)
for name, size in files:
    print(f"{name} - {size} MB")
