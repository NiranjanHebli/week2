
from collections import defaultdict
from typing import Optional


GRADE_SCALE = [
    (90, "A"),
    (75, "B"),
    (60, "C"),
    (0,  "D"),
]


def _letter_grade(average: float) -> str:
    """Return the letter grade for a given average score."""
    for threshold, grade in GRADE_SCALE:
        if average >= threshold:
            return grade
    return "D"


# Used to create student records, calculate GPA, get top performers, generate reports, and classify students.
def create_student(name: str, roll: str, **marks: int) -> dict:
    """Create and return a student record dict.

    Args:
        name: Student's full name.
        roll: Unique roll number (e.g. 'R001').
        **marks: Subject marks as keyword args (e.g. math=85, python=92).

    Returns:
        Dict with keys 'name', 'roll', 'marks', and 'attendance' (default 100.0).

    Raises:
        ValueError: If name/roll is empty or any mark is outside 0-100.
    """
    if not name or not name.strip():
        raise ValueError("Student name cannot be empty.")
    if not roll or not roll.strip():
        raise ValueError("Roll number cannot be empty.")
    for subject, score in marks.items():
        if not isinstance(score, (int, float)):
            raise ValueError(f"Mark for '{subject}' must be numeric, got {type(score).__name__}.")
        if not (0 <= score <= 100):
            raise ValueError(f"Mark for '{subject}' must be between 0 and 100, got {score}.")

    return {
        "name":       name.strip(),
        "roll":       roll.strip(),
        "marks":      {subject: int(score) for subject, score in marks.items()},
        "attendance": 100.0,
    }


# Used to calculate GPA, get top performers, generate reports, and classify students.
def calculate_gpa(*marks: float, scale: float = 10.0) -> float:
    """Calculate GPA by averaging marks and scaling to the given scale.

    Args:
        *marks: One or more numeric marks (0-100).
        scale: Target GPA scale. Defaults to 10.0.

    Returns:
        GPA rounded to two decimal places.

    Raises:
        ValueError: If no marks given, any mark is outside 0-100, or scale <= 0.
    """
    if not marks:
        raise ValueError("At least one mark is required to calculate GPA.")
    if scale <= 0:
        raise ValueError(f"Scale must be a positive number, got {scale}.")
    for m in marks:
        if not isinstance(m, (int, float)):
            raise ValueError(f"All marks must be numeric, got {type(m).__name__}.")
        if not (0 <= m <= 100):
            raise ValueError(f"Each mark must be between 0 and 100, got {m}.")

    average = sum(marks) / len(marks)
    return round((average / 100.0) * scale, 2)


# Used to get top performers, generate reports, and classify students.

def get_top_performers(
    students: list[dict],
    n: int = 5,
    subject: Optional[str] = None,
) -> list[dict]:
    """Return the top n students ranked by subject mark or overall average.

    Args:
        students: List of student dicts from create_student().
        n: Number of results to return. Defaults to 5.
        subject: Rank by this subject mark; ranks by overall average if None.

    Returns:
        Up to n student dicts in descending score order. Students missing
        the requested subject are excluded when subject is specified.

    Raises:
        ValueError: If n < 1.
    """
    if not students:
        return []
    if n < 1:
        raise ValueError(f"n must be at least 1, got {n}.")

    def score_key(student: dict) -> float:
        marks = student.get("marks", {})
        if subject:
            return marks.get(subject, -1)          # -1 so missing subjects sort last
        values = list(marks.values())
        return sum(values) / len(values) if values else 0.0

    if subject:
        eligible = [s for s in students if subject in s.get("marks", {})]
    else:
        eligible = [s for s in students if s.get("marks")]

    ranked = sorted(eligible, key=score_key, reverse=True)
    return ranked[:n]



# Used to generate reports and classify students.
def generate_report(student: dict, **options) -> str:
    """Generate a formatted performance report string for a student.

    Args:
        student: Student dict from create_student().
        **options: Formatting flags -- include_rank (bool, default True),
            include_grade (bool, default True), verbose (bool, default False).

    Returns:
        Multi-line formatted report string.

    Raises:
        ValueError: If student dict is missing 'name', 'roll', or 'marks'.
    """
    required_keys = {"name", "roll", "marks"}
    missing = required_keys - student.keys()
    if missing:
        raise ValueError(f"Student record is missing required keys: {missing}.")

    include_rank  = options.get("include_rank",  True)
    include_grade = options.get("include_grade", True)
    verbose       = options.get("verbose",       False)

    marks  = student["marks"]
    values = list(marks.values())
    average = sum(values) / len(values) if values else 0.0
    gpa    = calculate_gpa(*values) if values else 0.0

    lines = [
        "--- Student Report ---",
        f"Name       : {student['name']}",
        f"Roll       : {student['roll']}",
        f"Attendance : {student.get('attendance', 'N/A')}%",
    ]

    if include_rank and "rank" in student:
        lines.append(f"Rank       : {student['rank']}")

    lines.append(f"Average    : {average:.2f} / 100")
    lines.append(f"GPA        : {gpa:.2f} / 10.0")

    if include_grade:
        lines.append(f"Grade      : {_letter_grade(average)}")

    if verbose and marks:
        lines.append("Subjects   :")
        for subject, mark in sorted(marks.items()):
            lines.append(f"  {subject:<12}: {mark}")

    lines.append("----------------------")
    return "\n".join(lines)



# Used to classify students by grade.
def classify_students(students: list[dict]) -> dict:
    """Classify students into grade buckets A/B/C/D by overall average.

    Args:
        students: List of student dicts from create_student().

    Returns:
        Dict with keys 'A', 'B', 'C', 'D' mapping to lists of student dicts.
        All four keys are always present, even if a bucket is empty.
    """
    buckets: dict = defaultdict(list)

    # Ensure all four grade keys always exist even if empty.
    for grade in ("A", "B", "C", "D"):
        buckets[grade]          # touch the key to initialise

    for student in students:
        marks = student.get("marks", {})
        values = list(marks.values())
        if not values:
            continue                   # skip students with no marks recorded
        average = sum(values) / len(values)
        grade   = _letter_grade(average)
        buckets[grade].append(student)

    return dict(buckets)


# start of demo code to show how the functions work together
def start() -> None:
    separator = "=" * 60

    print(
        "\n+------------------------------------------------------------------------------+"
    )
    print(
        "|                        STUDENT PERFORMANCE ANALYTICS                         |"
    )
    print(
        "+------------------------------------------------------------------------------+\n"
    )
    print(separator)

    # Build a small cohort
    cohort = [
        create_student("Amit",    "R001", math=85, python=92, ml=78),
        create_student("Priya",   "R002", math=95, python=88, ml=91),
        create_student("Rahul",   "R003", math=72, python=65, ml=70),
        create_student("Sneha",   "R004", math=60, python=55, ml=58),
        create_student("Karan",   "R005", math=91, python=94, ml=89),
        create_student("Divya",   "R006", math=45, python=50, ml=48),
        create_student("Arjun",   "R007", math=78, python=82, ml=75),
        create_student("Meera",   "R008", math=88, python=91, ml=93),
    ]

    # --- GPA examples ---
    print("\ncalculate_gpa examples")
    print("-" * 40)
    print(f"  calculate_gpa(85, 92, 78)            -> {calculate_gpa(85, 92, 78)}")
    print(f"  calculate_gpa(85, 92, 78, scale=4.0) -> {calculate_gpa(85, 92, 78, scale=4.0)}")

    # --- Top performers overall ---
    print("\nTop 3 overall performers")
    print("-" * 40)
    for rank, s in enumerate(get_top_performers(cohort, n=3), start=1):
        avg = sum(s["marks"].values()) / len(s["marks"])
        print(f"  {rank}. {s['name']:<10}  avg={avg:.1f}")

    # --- Top performers by subject ---
    print("\nTop 3 by Python marks")
    print("-" * 40)
    for rank, s in enumerate(get_top_performers(cohort, n=3, subject="python"), start=1):
        print(f"  {rank}. {s['name']:<10}  python={s['marks']['python']}")

    # --- Full report ---
    print("\nVerbose report for Priya")
    print("-" * 40)
    priya = cohort[1]
    priya["rank"] = 1
    print(generate_report(priya, verbose=True))

    # --- Classification ---
    print("\nStudent classification")
    print("-" * 40)
    buckets = classify_students(cohort)
    for grade in ("A", "B", "C", "D"):
        names = [s["name"] for s in buckets[grade]]
        print(f"  Grade {grade}: {names if names else '(none)'}")

    print(f"\n{separator}\n")


if __name__ == "__main__":
    start()