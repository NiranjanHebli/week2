

import sys
import traceback
from student_analytics import (
    create_student,
    calculate_gpa,
    get_top_performers,
    generate_report,
    classify_students,
)


PASS  = 0
FAIL  = 0


def check(label: str, expr: bool) -> None:
    global PASS, FAIL
    if expr:
        PASS += 1
        print(f"  PASS  {label}")
    else:
        FAIL += 1
        print(f"  FAIL  {label}")


def expect_error(label: str, fn, *args, **kwargs) -> None:
    """Assert that calling fn(*args, **kwargs) raises an exception."""
    global PASS, FAIL
    try:
        fn(*args, **kwargs)
        FAIL += 1
        print(f"  FAIL  {label}  (no exception raised)")
    except Exception:
        PASS += 1
        print(f"  PASS  {label}")


def section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")



section("create_student")

s1 = create_student("Amit", "R001", math=85, python=92, ml=78)
s2 = create_student("Priya", "R002", math=95, python=88, ml=91)
s3 = create_student("Rahul", "R003", math=60, python=65, ml=70)

# Basic structure
check("returns a dict",                    isinstance(s1, dict))
check("name stored correctly",             s1["name"] == "Amit")
check("roll stored correctly",             s1["roll"] == "R001")
check("marks stored as nested dict",       isinstance(s1["marks"], dict))
check("math mark stored",                  s1["marks"]["math"] == 85)
check("python mark stored",                s1["marks"]["python"] == 92)
check("ml mark stored",                    s1["marks"]["ml"] == 78)
check("attendance defaults to 100.0",      s1["attendance"] == 100.0)

# Whitespace stripping
s_ws = create_student("  Bob  ", "  R099  ", math=70)
check("name is stripped",                  s_ws["name"] == "Bob")
check("roll is stripped",                  s_ws["roll"] == "R099")

# Boundary marks
s_boundary = create_student("Edge", "E001", math=0, python=100)
check("mark 0 is valid",                   s_boundary["marks"]["math"] == 0)
check("mark 100 is valid",                 s_boundary["marks"]["python"] == 100)

# No subjects provided -- valid empty marks dict
s_empty = create_student("NoSubj", "N001")
check("no subjects gives empty marks dict", s_empty["marks"] == {})

# Error cases
expect_error("empty name raises ValueError",    create_student, "", "R001", math=50)
expect_error("empty roll raises ValueError",    create_student, "X", "", math=50)
expect_error("mark > 100 raises ValueError",    create_student, "X", "R1", math=101)
expect_error("mark < 0 raises ValueError",      create_student, "X", "R1", math=-1)
expect_error("non-numeric mark raises ValueError", create_student, "X", "R1", math="high")


section("calculate_gpa")

check("three marks on scale 10",           calculate_gpa(85, 92, 78) == 8.5)
check("perfect marks give 10.0",           calculate_gpa(100, 100, 100) == 10.0)
check("zero marks give 0.0",               calculate_gpa(0, 0, 0) == 0.0)
check("single mark",                       calculate_gpa(80) == 8.0)
check("scale=4.0 conversion",              calculate_gpa(85, 92, 78, scale=4.0) == 3.4)
check("scale=100 returns raw average",     calculate_gpa(85, 92, 78, scale=100) == 85.0)
check("result is float",                   isinstance(calculate_gpa(70, 80), float))
check("rounds to two decimal places",      calculate_gpa(33, 33, 34) == round((100/3) / 100 * 10, 2))
check("float marks accepted",              calculate_gpa(85.5, 90.5) == round((176.0 / 200) * 10, 2))

# Edge / error cases
expect_error("no marks raises ValueError",          calculate_gpa)
expect_error("mark > 100 raises ValueError",        calculate_gpa, 105)
expect_error("mark < 0 raises ValueError",          calculate_gpa, -5)
expect_error("non-numeric mark raises ValueError",  calculate_gpa, "A")
expect_error("negative scale raises ValueError",    calculate_gpa, 80, scale=-1)
expect_error("zero scale raises ValueError",        calculate_gpa, 80, scale=0)



section("get_top_performers")

cohort = [s1, s2, s3]

# Overall ranking
top1 = get_top_performers(cohort, n=1)
check("returns a list",                    isinstance(top1, list))
check("n=1 returns exactly 1 student",     len(top1) == 1)
check("top overall is Priya (avg 91.3)",   top1[0]["name"] == "Priya")

top2 = get_top_performers(cohort, n=2)
check("n=2 returns exactly 2 students",    len(top2) == 2)
check("second overall is Amit (avg 85)",   top2[1]["name"] == "Amit")

# Subject-specific ranking
top_py = get_top_performers(cohort, n=1, subject="python")
check("top Python scorer is Amit (92)",    top_py[0]["name"] == "Amit")

top_math = get_top_performers(cohort, n=1, subject="math")
check("top math scorer is Priya (95)",     top_math[0]["name"] == "Priya")

# n larger than cohort returns all
all_students = get_top_performers(cohort, n=100)
check("n > len returns all students",      len(all_students) == len(cohort))

# Default n
default_n = get_top_performers(cohort)
check("default n=5 returns at most 5",     len(default_n) <= 5)

# Empty list
check("empty list returns empty list",     get_top_performers([], n=3) == [])

# Missing subject excludes student
s_no_ml = create_student("Temp", "T001", math=99)
result = get_top_performers([s_no_ml, s1], n=5, subject="ml")
check("student missing subject is excluded", s_no_ml not in result)

# Error case
expect_error("n=0 raises ValueError",      get_top_performers, cohort, 0)



section("generate_report")

report_default = generate_report(s2)
check("report is a string",                isinstance(report_default, str))
check("report contains student name",      "Priya" in report_default)
check("report contains roll number",       "R002" in report_default)
check("report contains grade by default",  "Grade" in report_default)
check("Priya's grade is A",                "Grade      : A" in report_default)

# verbose=True shows subject breakdown
report_verbose = generate_report(s1, verbose=True)
check("verbose report contains 'Subjects'", "Subjects" in report_verbose)
check("verbose report contains math mark",  "math" in report_verbose)

# include_grade=False hides grade
report_no_grade = generate_report(s1, include_grade=False)
check("include_grade=False hides Grade",   "Grade" not in report_no_grade)

# include_rank with rank key present
s1_ranked = {**s1, "rank": 2}
report_ranked = generate_report(s1_ranked, include_rank=True)
check("rank shown when include_rank=True", "Rank" in report_ranked)

# include_rank=False suppresses rank even if present
report_no_rank = generate_report(s1_ranked, include_rank=False)
check("include_rank=False hides rank",     "Rank" not in report_no_rank)

# GPA line always present
check("report contains GPA line",          "GPA" in report_default)

# Error case -- missing required key
expect_error("missing 'marks' raises ValueError",
             generate_report, {"name": "X", "roll": "Y"})
expect_error("missing 'name' raises ValueError",
             generate_report, {"roll": "Y", "marks": {}})


section("classify_students")

# Build a diverse cohort
a_student = create_student("Alice", "A001", math=95, python=92, ml=91)   # avg 92.7 -> A
b_student = create_student("Bob",   "B001", math=80, python=78, ml=75)   # avg 77.7 -> B
c_student = create_student("Carol", "C001", math=65, python=62, ml=63)   # avg 63.3 -> C
d_student = create_student("Dave",  "D001", math=40, python=55, ml=50)   # avg 48.3 -> D

buckets = classify_students([a_student, b_student, c_student, d_student])

check("returns a dict",                    isinstance(buckets, dict))
check("all four grade keys present",       set(buckets.keys()) == {"A", "B", "C", "D"})
check("A bucket contains Alice",           any(s["name"] == "Alice" for s in buckets["A"]))
check("B bucket contains Bob",             any(s["name"] == "Bob"   for s in buckets["B"]))
check("C bucket contains Carol",           any(s["name"] == "Carol" for s in buckets["C"]))
check("D bucket contains Dave",            any(s["name"] == "Dave"  for s in buckets["D"]))
check("total students preserved",
      sum(len(v) for v in buckets.values()) == 4)

# Boundary: avg exactly 90 goes to A
s90 = create_student("Ninety", "N090", math=90, python=90, ml=90)
b90 = classify_students([s90])
check("avg == 90 classified as A",         any(s["name"] == "Ninety" for s in b90["A"]))

# Boundary: avg exactly 75 goes to B
s75 = create_student("Seventy5", "N075", math=75, python=75, ml=75)
b75 = classify_students([s75])
check("avg == 75 classified as B",         any(s["name"] == "Seventy5" for s in b75["B"]))

# Empty input
empty_buckets = classify_students([])
check("empty list returns four empty grade keys",
      all(empty_buckets[g] == [] for g in ("A", "B", "C", "D")))

# Student with no marks is skipped
s_nomarks = create_student("Ghost", "G001")
ghost_buckets = classify_students([s_nomarks])
check("student with no marks is skipped",
      sum(len(v) for v in ghost_buckets.values()) == 0)


print(f"\n{'=' * 60}")
total = PASS + FAIL
print(f"  Results: {PASS} passed, {FAIL} failed  ({total} total)")
print(f"{'=' * 60}\n")

if FAIL > 0:
    sys.exit(1)