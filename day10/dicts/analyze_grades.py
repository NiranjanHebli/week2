from collections import defaultdict
from typing import Dict, List, Any


def analyze_grades(sem1: Dict[str, float], sem2: Dict[str, float]) -> Dict[str, Any]:
    """
    Analyze grades from two semesters to compute combined GPA,
    grade trend, and common subjects.
    """

    merged: defaultdict[str, List[float]] = defaultdict(list)

    for subject, grade in sem1.items():
        merged[subject].append(grade)

    for subject, grade in sem2.items():
        merged[subject].append(grade)

    subject_avg: Dict[str, float] = {
        subject: sum(grades) / len(grades) for subject, grades in merged.items()
    } if merged else {}

    all_grades: List[float] = [g for grades in merged.values() for g in grades]
    combined_gpa: float | None = sum(all_grades) / len(all_grades) if all_grades else None

    avg_sem1: float | None = sum(sem1.values()) / len(sem1) if sem1 else None
    avg_sem2: float | None = sum(sem2.values()) / len(sem2) if sem2 else None

    if avg_sem1 is None or avg_sem2 is None:
        trend = "Insufficient Data"
    elif avg_sem2 > avg_sem1:
        trend = "Improving"
    elif avg_sem2 < avg_sem1:
        trend = "Declining"
    else:
        trend = "Stable"

    common_subjects: List[str] = list(sem1.keys() & sem2.keys())

    return {
        "combined_gpa": combined_gpa,
        "trend": trend,
        "common_subjects": common_subjects,
    }

# Example usage
sem1 = {}
sem2 = {"Math": 90, "Physics": 80, "Biology": 88}
print(analyze_grades(sem1, sem2))