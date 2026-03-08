
## Prompt:-


Write a Python program that analyzes student grades across two semesters.

Create a function analyze_grades(sem1, sem2) where sem1 and sem2 are dictionaries representing subjects and their grades for two different semesters.

The function should:

- Merge the grade data and compute a combined GPA (average of all grades from both semesters).

Determine the grade trend:

- "Improving" if the average grade in semester 2 is higher than semester 1.

- "Declining" if the average grade in semester 2 is lower than semester 1.

- "Stable" if both averages are equal.

Identify the subjects common to both semesters.

Requirements:

- Use defaultdict from the collections module to help combine subject grades.

- Use dictionary comprehension where appropriate.

Return the result as a dictionary report containing:

- combined_gpa

- trend

- common_subjects

## AI Generated Code:-

```python

from collections import defaultdict

def analyze_grades(sem1, sem2):
    merged = defaultdict(list)

    # Merge grades from both semesters
    for subject, grade in sem1.items():
        merged[subject].append(grade)

    for subject, grade in sem2.items():
        merged[subject].append(grade)

    # Dictionary comprehension (example: subject -> average grade)
    subject_avg = {sub: sum(grades) / len(grades) for sub, grades in merged.items()}

    # Combined GPA
    all_grades = [grade for grades in merged.values() for grade in grades]
    combined_gpa = sum(all_grades) / len(all_grades)

    # Semester averages
    avg_sem1 = sum(sem1.values()) / len(sem1)
    avg_sem2 = sum(sem2.values()) / len(sem2)

    # Determine trend
    if avg_sem2 > avg_sem1:
        trend = "Improving"
    elif avg_sem2 < avg_sem1:
        trend = "Declining"
    else:
        trend = "Stable"

    # Common subjects
    common_subjects = list(set(sem1.keys()) & set(sem2.keys()))

    report = {
        "combined_gpa": combined_gpa,
        "trend": trend,
        "common_subjects": common_subjects
    }

    return report


# Example
sem1 = {"Math": 85, "Physics": 78, "Chemistry": 82}
sem2 = {"Math": 90, "Physics": 80, "Biology": 88}

print(analyze_grades(sem1, sem2))

```