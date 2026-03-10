# Day 11 - AM - Assignment - File Handling

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](#badges)

## Part A:- Sales Data Pipeline
This project implements a data merger pipeline that processes sales data from multiple CSV files.
The program reads several CSV files, merges their contents, removes duplicate records, and generates structured output files.

In addition to merging the data, the system computes the total revenue for each product across all stores.

The implementation uses Python’s built-in csv, json, and datetime modules.

### Files:- 

[`sales_data_pipeline.py`](./sales_data_pipeline/sales_data_pipeline.py): main program containing data merger logic

### How to use:- 

1. Run the program using :-


```bash
cd sales_data_pipeline
```

```bash
python3 sales_data_pipeline.py
```

## Part B:- Backup Manager
This project implements a backup manager that archives files and folders from a specified directory.


### Features:

- Accepts source directory and backup directory as command-line arguments.

- Copies only files with .csv and .json extensions from the source directory.

- Creates timestamped backup copies of each file to maintain version history.

- Skips files that were already backed up, using entries recorded in the backup log.

- Maintains only the latest 5 backups per file and removes older backups automatically.

- Records all operations (copy, skip, and deletion events) in backup_log.txt using append mode to preserve the backup history.

The implementation uses Python’s built-in os, shutil, and datetime modules.

### Files:- 

[`backup_manager.py`](./backup_manager/backup_manager.py): main program containing backup manager logic

### How to use:- 

1. Run the program using :-

```bash
cd backup_manager
```
```bash
python3 backup_manager.py <source_directory> <destination_directory>
```
eg:-

```bash
python3 backup_manager.py source_data backups
```

## Part C - Interview Answers

### Solutions in the file:- [interview_answers.md](./interview_answers.md)


## Part D - AI Augmented Task

### Solutions in the file:- [ai_augmented.md](./ai_augmented.md)