import pandas as pd
from pathlib import Path

CLEANED_DATA_PATH = Path("data/cleaned")

learners = pd.read_csv(CLEANED_DATA_PATH / "learners_cleaned.csv")
marks = pd.read_csv(CLEANED_DATA_PATH / "marks_cleaned.csv")
attendance = pd.read_csv(CLEANED_DATA_PATH / "attendance_cleaned.csv")

# Average mark per learner
learner_average_marks = (
    marks
    .groupby("learner_id")["mark"]
    .mean()
    .reset_index()
)

learner_average_marks = learner_average_marks.rename(
    columns={"mark": "average_mark"}
)

# Average attendance per learner
learner_average_attendance = (
    attendance
    .groupby("learner_id")["attendance_rate"]
    .mean()
    .reset_index()
)

learner_average_attendance = learner_average_attendance.rename(
    columns={"attendance_rate": "average_attendance_rate"}
)

# Combine learners, marks, and attendance
learner_summary = learners.merge(
    learner_average_marks,
    on="learner_id",
    how="left"
)

learner_summary = learner_summary.merge(
    learner_average_attendance,
    on="learner_id",
    how="left"
)

print("Learner summary created.")
print(learner_summary.head())

# -----------------------------
# Create learner support status
# -----------------------------

def get_learner_status(row):
    if row["average_mark"] < 45 and row["average_attendance_rate"] < 0.85:
        return "Critical Support Needed"
    elif row["average_mark"] < 50:
        return "Academic Support Needed"
    elif row["average_attendance_rate"] < 0.85:
        return "Attendance Support Needed"
    else:
        return "On Track"

learner_summary["learner_status"] = learner_summary.apply(get_learner_status, axis=1)

print()
print("Learner support status counts:")
print(learner_summary["learner_status"].value_counts())

REPORTS_PATH = Path("reports")
REPORTS_PATH.mkdir(parents=True, exist_ok=True)

learner_summary.to_csv(REPORTS_PATH / "learner_summary.csv", index=False)

print()
print("Learner summary report saved to reports/learner_summary.csv")

# -----------------------------
# Subject performance summary
# -----------------------------

subject_summary = (
    marks
    .groupby("subject")
    .agg(
        average_mark=("mark", "mean"),
        lowest_mark=("mark", "min"),
        highest_mark=("mark", "max"),
        number_of_marks=("mark", "count")
    )
    .reset_index()
)

subject_summary["average_mark"] = subject_summary["average_mark"].round(1)

subject_summary = subject_summary.sort_values("average_mark", ascending=True)

subject_summary.to_csv(REPORTS_PATH / "subject_summary.csv", index=False)

print()
print("Subject performance summary:")
print(subject_summary)

print()
print("Subject summary report saved to reports/subject_summary.csv")

# -----------------------------
# Grade performance summary
# -----------------------------

marks_with_learners = marks.merge(
    learners[["learner_id", "grade", "class_group"]],
    on="learner_id",
    how="left"
)

grade_summary = (
    marks_with_learners
    .groupby("grade")
    .agg(
        average_mark=("mark", "mean"),
        lowest_mark=("mark", "min"),
        highest_mark=("mark", "max"),
        number_of_marks=("mark", "count")
    )
    .reset_index()
)

grade_summary["average_mark"] = grade_summary["average_mark"].round(1)

grade_summary = grade_summary.sort_values("grade")

grade_summary.to_csv(REPORTS_PATH / "grade_summary.csv", index=False)

print()
print("Grade performance summary:")
print(grade_summary)

print()
print("Grade summary report saved to reports/grade_summary.csv")

# -----------------------------
# Class performance summary
# -----------------------------

class_summary = (
    marks_with_learners
    .groupby("class_group")
    .agg(
        average_mark=("mark", "mean"),
        lowest_mark=("mark", "min"),
        highest_mark=("mark", "max"),
        number_of_marks=("mark", "count")
    )
    .reset_index()
)

class_summary["average_mark"] = class_summary["average_mark"].round(1)

class_summary = class_summary.sort_values("average_mark", ascending=True)

class_summary.to_csv(REPORTS_PATH / "class_summary.csv", index=False)

print()
print("Class performance summary:")
print(class_summary)

print()
print("Class summary report saved to reports/class_summary.csv")

# -----------------------------
# Class attendance summary
# -----------------------------

attendance_with_learners = attendance.merge(
    learners[["learner_id", "grade", "class_group"]],
    on="learner_id",
    how="left"
)

class_attendance_summary = (
    attendance_with_learners
    .groupby("class_group")
    .agg(
        average_attendance_rate=("attendance_rate", "mean"),
        lowest_attendance_rate=("attendance_rate", "min"),
        highest_attendance_rate=("attendance_rate", "max"),
        number_of_records=("attendance_rate", "count")
    )
    .reset_index()
)

class_attendance_summary["average_attendance_rate"] = (
    class_attendance_summary["average_attendance_rate"] * 100
).round(1)

class_attendance_summary["lowest_attendance_rate"] = (
    class_attendance_summary["lowest_attendance_rate"] * 100
).round(1)

class_attendance_summary["highest_attendance_rate"] = (
    class_attendance_summary["highest_attendance_rate"] * 100
).round(1)

class_attendance_summary = class_attendance_summary.sort_values(
    "average_attendance_rate",
    ascending=True
)

class_attendance_summary.to_csv(
    REPORTS_PATH / "class_attendance_summary.csv",
    index=False
)

print()
print("Class attendance summary:")
print(class_attendance_summary)

print()
print("Class attendance summary saved to reports/class_attendance_summary.csv")

# -----------------------------
# Combined class performance and attendance summary
# -----------------------------

combined_class_summary = class_summary.merge(
    class_attendance_summary,
    on="class_group",
    how="left"
)

combined_class_summary = combined_class_summary[
    [
        "class_group",
        "average_mark",
        "average_attendance_rate",
        "lowest_mark",
        "highest_mark",
        "number_of_marks",
        "lowest_attendance_rate",
        "highest_attendance_rate",
        "number_of_records"
    ]
]

combined_class_summary = combined_class_summary.sort_values(
    ["average_mark", "average_attendance_rate"],
    ascending=[True, True]
)

combined_class_summary.to_csv(
    REPORTS_PATH / "combined_class_summary.csv",
    index=False
)

print()
print("Combined class summary:")
print(combined_class_summary)

print()
print("Combined class summary saved to reports/combined_class_summary.csv")

# -----------------------------
# Subject performance by term
# -----------------------------

subject_term_summary = (
    marks
    .groupby(["subject", "term"])
    .agg(
        average_mark=("mark", "mean"),
        lowest_mark=("mark", "min"),
        highest_mark=("mark", "max"),
        number_of_marks=("mark", "count")
    )
    .reset_index()
)

subject_term_summary["average_mark"] = subject_term_summary["average_mark"].round(1)

subject_term_summary = subject_term_summary.sort_values(["subject", "term"])

subject_term_summary.to_csv(
    REPORTS_PATH / "subject_term_summary.csv",
    index=False
)

print()
print("Subject term summary:")
print(subject_term_summary)

print()
print("Subject term summary saved to reports/subject_term_summary.csv")

# -----------------------------
# Subject trend change summary
# -----------------------------

subject_trend_change = subject_term_summary.pivot(
    index="subject",
    columns="term",
    values="average_mark"
).reset_index()

subject_trend_change = subject_trend_change.rename(
    columns={
        1: "term_1_average",
        2: "term_2_average",
        3: "term_3_average",
        4: "term_4_average"
    }
)

subject_trend_change["change_t1_to_t4"] = (
    subject_trend_change["term_4_average"] - subject_trend_change["term_1_average"]
).round(1)

subject_trend_change = subject_trend_change.sort_values(
    "change_t1_to_t4",
    ascending=True
)

subject_trend_change.to_csv(
    REPORTS_PATH / "subject_trend_change.csv",
    index=False
)

print()
print("Subject trend change summary:")
print(subject_trend_change)

print()
print("Subject trend change report saved to reports/subject_trend_change.csv")

# -----------------------------
# Executive summary text report
# -----------------------------

lowest_subject = subject_summary.iloc[0]
highest_subject = subject_summary.iloc[-1]

lowest_class = combined_class_summary.iloc[0]

biggest_decline = subject_trend_change.iloc[0]
biggest_improvement = subject_trend_change.iloc[-1]

summary_text = f"""
School Performance Analytics - Executive Summary

1. Overall learner support:
{learner_summary["learner_status"].value_counts().to_string()}

2. Lowest-performing subject:
{lowest_subject["subject"]} has the lowest average mark at {lowest_subject["average_mark"]}%.

3. Highest-performing subject:
{highest_subject["subject"]} has the highest average mark at {highest_subject["average_mark"]}%.

4. Lowest-performing class:
{lowest_class["class_group"]} has the lowest average mark at {lowest_class["average_mark"]}%, with an average attendance rate of {lowest_class["average_attendance_rate"]}%.

5. Biggest subject decline from Term 1 to Term 4:
{biggest_decline["subject"]} changed by {biggest_decline["change_t1_to_t4"]} percentage points.

6. Biggest subject improvement from Term 1 to Term 4:
{biggest_improvement["subject"]} improved by {biggest_improvement["change_t1_to_t4"]} percentage points.

Recommended next steps:
- Investigate subjects with low average marks, especially Physical Science and Mathematics.
- Review classes that show both lower marks and lower attendance.
- Prioritise attendance support for learners marked as Attendance Support Needed.
- Use term trend data to monitor subjects that are declining over time.
"""

with open(REPORTS_PATH / "executive_summary.txt", "w", encoding="utf-8") as file:
    file.write(summary_text)

print()
print("Executive summary saved to reports/executive_summary.txt")