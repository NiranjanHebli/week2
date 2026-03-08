# ============================================================
#   Student Management System
# ============================================================

# This program manages student records for a class, allowing you to:
# - Add new student records (name, subject, marks)
# - View top-3 students in a subject
# - Calculate class average for a subject
# - List students scoring above overall average
# - Remove student records by name
# - Save records to a file on exit and load on startup

records = [
    ["Aman", "Math", 88],
    ["Priya", "Physics", 91],
    ["Rahul", "Math", 76],
    ["Sneha", "Chemistry", 84],
    ["Arjun", "Physics", 67],
    ["Meera", "Math", 95],
    ["Karan", "Chemistry", 78],
    ["Divya", "Physics", 82],
    ["Rohan", "Chemistry", 90],
    ["Tanvi", "Math", 73],
]


VALID_SUBJECTS = {"math", "physics", "chemistry"}


# Add a new student record; reject duplicate name+subject pairs.
def add_student(name, subject, marks):
    """Append a new student record; reject duplicate name+subject pairs."""
    if subject.lower() not in VALID_SUBJECTS:
        print("  Error: Invalid subject '" + subject + "'. Allowed subjects are: Math, Physics, Chemistry.")
        return

    duplicates = [
        r
        for r in records
        if r[0].lower() == name.lower() and r[1].lower() == subject.lower()
    ]
    if duplicates:
        print("Error: '" + name + "' is already enrolled in " + subject + ".")
        return

    records.append([name, subject, marks])
    print("  Added: " + name + " | " + subject + " | " + str(marks))


# Return the top-3 students in a subject, sorted by marks descending.
# If fewer than 3 students are enrolled in the subject, return all of them.
# If no students are enrolled in the subject, return an empty list.
def get_toppers(subject):
    """Return the top-3 students in a subject, sorted by marks descending."""
    if subject.lower() not in VALID_SUBJECTS:
        print("  Error: Invalid subject '" + subject + "'. Allowed subjects are: Math, Physics, Chemistry.")
        return []

    subject_records = [r for r in records if r[1].lower() == subject.lower()]

    if not subject_records:
        print("  No records found for subject '" + subject + "'.")
        return []

    ranked = sorted(subject_records, key=lambda x: x[2], reverse=True)
    top3 = ranked[:3]  # slicing

    print("\n  Top 3 Toppers - " + subject)
    print("  " + "-" * 30)
    print("  {:<6} {:<15} {}".format("Rank", "Name", "Marks"))
    print("  " + "-" * 30)
    for i, student in enumerate(top3, start=1):
        print("  {:<6} {:<15} {}".format(i, student[0], student[2]))
    return top3


# Calculate and return the average marks for a given subject.
def class_average(subject):
    """Return the average marks for a given subject."""
    if subject.lower() not in VALID_SUBJECTS:
        print("  Error: Invalid subject '" + subject + "'. Allowed subjects are: Math, Physics, Chemistry.")
        return 0.0

    marks_list = [m[2] for m in records if m[1].lower() == subject.lower()]

    if not marks_list:
        print("  No records found for subject '" + subject + "'.")
        return 0.0

    avg = sum(marks_list) / len(marks_list)
    print("\n  Class Average - " + subject + ": " + str(round(avg, 2)))
    return avg


# Return all students who score above the overall average across all subjects.
def above_average_students():
    """Return all students who score above the overall average."""
    if not records:
        print("  No student records available.")
        return []

    overall_avg = sum(r[2] for r in records) / len(records)

    above = [r for r in records if r[2] > overall_avg]

    print("\n  Overall Average: " + str(round(overall_avg, 2)))
    print("  Students scoring above average:")
    print("  " + "-" * 35)
    print("  {:<15} {:<12} {}".format("Name", "Subject", "Marks"))
    print("  " + "-" * 35)
    for s in above:
        print("  {:<15} {:<12} {}".format(s[0], s[1], s[2]))
    return above


# Remove every record belonging to 'name' without using remove() in a loop.
def remove_student(name):
    """Remove every record belonging to 'name' without using remove() in a loop."""
    global records

    original_len = len(records)
    records = [r for r in records if r[0].lower() != name.lower()]

    removed = original_len - len(records)
    if removed:
        print("  Removed " + str(removed) + " record(s) for '" + name + "'.")
    else:
        print("  No records found for '" + name + "'.")


# Non-destructive peek at the most recently added record.
def peek_latest():
    """Non-destructive peek at the most recently added record."""
    if records:
        latest = records[-1]  # pop-equivalent peek
        print(
            "  Latest record: " + latest[0] + " | " + latest[1] + " | " + str(latest[2])
        )

# Save all records to a text file on exit, and load them on startup.
def save_to_file(filename="students.txt"):
    """Persist all records to a text file on exit."""
    with open(filename, "w") as f:  # file write
        f.write("{}|{}|{}\n".format("Name", "Subject", "Marks"))
        f.write("-" * 35 + "\n")
        for r in sorted(records, key=lambda x: (x[1], -x[2])):
            f.write("{}|{}|{}\n".format(r[0], r[1], r[2]))
    print("\n  Records saved to '" + filename + "'.")


# Load previously saved records from file, if it exists. If the file is missing (first run), start with the default records.
def load_from_file(filename="students.txt"):
    """Load previously saved records from file."""
    global records
    try:
        with open(filename, "r") as f:  # file read
            lines = f.readlines()[2:]  # skip header rows
        loaded = []
        for line in lines:
            parts = line.strip().split("|")
            if len(parts) >= 3:
                name = parts[0]
                subject = parts[1]
                marks = int(parts[2])
                loaded.append([name, subject, marks])
        if loaded:
            records = loaded
            print("  Loaded " + str(len(loaded)) + " records from '" + filename + "'.")
    except FileNotFoundError:
        pass  # first run - no file yet


# Display all records in a tabular format, sorted by subject and marks descending.
def show_all():
    print("\n  {:<4} {:<15} {:<12} {}".format("#", "Name", "Subject", "Marks"))
    print("  " + "-" * 40)
    for i, r in enumerate(records, 1):
        print("  {:<4} {:<15} {:<12} {}".format(i, r[0], r[1], r[2]))
    peek_latest()


# Display a menu of options and prompt the user to select an action until they choose to exit.
def print_menu():
    print("\n+----------------------------------------------+")
    print("|         STUDENT MANAGEMENT SYSTEM            |")
    print("+----------------------------------------------+\n")
    print("  1  Add Student")
    print("  2  Show Toppers (by Subject)")
    print("  3  Show Class Average (by Subject)")
    print("  4  Show Above-Average Students")
    print("  5  Remove Student")
    print("  6  Show All Records")
    print("  7  Exit and Save")

# Main program loop
def main():
    load_from_file()

    while True:
        print_menu()
        choice = input("  Enter choice (1-7): ").strip()

        if choice == "1":
            name = input("  Name    : ").strip().title()
            while True:
                subject = input("  Subject (Math / Physics / Chemistry): ").strip().title()
                if subject.lower() in VALID_SUBJECTS:
                    break
                print("  Invalid subject. Please enter one of: Math, Physics, Chemistry.")
            try:
                marks = int(input("  Marks   : ").strip())
                if not (0 <= marks <= 100):
                    raise ValueError
            except ValueError:
                print("  Marks must be an integer between 0 and 100.")
                continue
            add_student(name, subject, marks)

        elif choice == "2":
            while True:
                subject = input("  Enter subject (Math / Physics / Chemistry): ").strip().title()
                if subject.lower() in VALID_SUBJECTS:
                    break
                print("  Invalid subject. Please enter one of: Math, Physics, Chemistry.")
            get_toppers(subject)

        elif choice == "3":
            while True:
                subject = input("  Enter subject (Math / Physics / Chemistry): ").strip().title()
                if subject.lower() in VALID_SUBJECTS:
                    break
                print("  Invalid subject. Please enter one of: Math, Physics, Chemistry.")
            class_average(subject)

        elif choice == "4":
            above_average_students()

        elif choice == "5":
            name = input("  Enter student name to remove: ").strip().title()
            remove_student(name)

        elif choice == "6":
            show_all()

        elif choice == "7":
            save_to_file()
            break

        else:
            print("  Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()