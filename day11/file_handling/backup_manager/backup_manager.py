import sys
import shutil
from pathlib import Path
from datetime import datetime

LOG_FILE = "logs/backup_log.txt"
VALID_EXTENSIONS = [".csv", ".json"]
MAX_BACKUPS = 5


# log function to write messages to the log file with timestamps. It appends messages to the log file, creating it if it doesn't exist.
def log(message):
    """Write log messages to backup_log.txt."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


# This function reads the log file and extracts the names of files that have already been backed up.
def get_backed_up_files():
    """Read log file and return a set of files already backed up."""
    backed_up = set()

    if Path(LOG_FILE).exists():
        with open(LOG_FILE, "r") as f:
            for line in f:
                if "Copied:" in line:
                    name = line.split("Copied:")[1].split("->")[0].strip()
                    backed_up.add(name)

    return backed_up


# This function copies .csv and .json files from the source directory to the backup directory, appending a timestamp to the filename.
def copy_files(source_dir, backup_dir):
    """Copy .csv and .json files with timestamp suffix, skip already backed files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backed_up_files = get_backed_up_files()

    for file in source_dir.iterdir():
        if file.suffix.lower() in VALID_EXTENSIONS and file.is_file():

            if file.name in backed_up_files:
                log(f"Skipped (already backed up): {file.name}")
                continue

            new_name = f"{file.stem}_{timestamp}{file.suffix}"
            destination = backup_dir / new_name

            shutil.copy2(file, destination)
            log(f"Copied: {file.name} -> {new_name}")


# This function manages the backup rotation by keeping only the last 5 backups for each original file.
def rotate_backups(backup_dir):
    """Keep only the last 5 backups per original file."""
    backups = {}

    for file in backup_dir.iterdir():
        if file.suffix in VALID_EXTENSIONS:
            base_name = file.stem.rsplit("_", 2)[0]
            backups.setdefault(base_name, []).append(file)

    for base, files in backups.items():
        files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        for old_file in files[MAX_BACKUPS:]:
            old_file.unlink()
            log(f"Deleted old backup: {old_file.name}")


# The main function orchestrates the backup process.
def main():
    if len(sys.argv) != 3:
        print("Usage: python backup_manager.py <source_directory> <backup_directory>")
        sys.exit(1)

    source_directory = Path(sys.argv[1])
    backup_directory = Path(sys.argv[2])

    if not source_directory.exists():
        print("Source directory does not exist.")
        sys.exit(1)

    backup_directory.mkdir(parents=True, exist_ok=True)

    log("Backup process started")

    copy_files(source_directory, backup_directory)
    rotate_backups(backup_directory)

    log("Backup process completed\n")


if __name__ == "__main__":
    main()
