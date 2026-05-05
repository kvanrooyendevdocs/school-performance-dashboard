import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("data/raw")
CLEANED_DATA_PATH = Path("data/cleaned")

CLEANED_DATA_PATH.mkdir(parents=True, exist_ok=True)

teachers = pd.read_csv(RAW_DATA_PATH / "teachers.csv")
learners = pd.read_csv(RAW_DATA_PATH / "learners.csv")
enrolments = pd.read_csv(RAW_DATA_PATH / "enrolments.csv")
marks = pd.read_csv(RAW_DATA_PATH / "marks.csv")
attendance = pd.read_csv(RAW_DATA_PATH / "attendance.csv")

print("Raw data loaded successfully.")

print("Teachers:", teachers.shape)
print("Learners:", learners.shape)
print("Enrolments:", enrolments.shape)
print("Marks:", marks.shape)
print("Attendance:", attendance.shape)

# -----------------------------
# Basic cleaning
# -----------------------------

# Remove extra spaces from text columns
teachers["teacher_name"] = teachers["teacher_name"].str.strip()
teachers["subject"] = teachers["subject"].str.strip()

learners["learner_name"] = learners["learner_name"].str.strip()
learners["class_group"] = learners["class_group"].str.strip()

enrolments["subject"] = enrolments["subject"].str.strip()
marks["subject"] = marks["subject"].str.strip()

# Check mark values are between 0 and 100
marks["mark"] = marks["mark"].clip(lower=0, upper=100)

# Recalculate attendance rate to make sure it is correct
attendance["attendance_rate"] = attendance["days_present"] / attendance["days_possible"]
attendance["attendance_rate"] = attendance["attendance_rate"].round(3)
# Create a risk category for each mark
def get_risk_category(mark):
    if mark < 40:
        return "High Risk"
    elif mark < 50:
        return "At Risk"
    elif mark < 70:
        return "Passing"
    else:
        return "Strong"

marks["risk_category"] = marks["mark"].apply(get_risk_category)

# Create an attendance risk category
def get_attendance_category(attendance_rate):
    if attendance_rate < 0.80:
        return "High Attendance Risk"
    elif attendance_rate < 0.90:
        return "Attendance Concern"
    else:
        return "Good Attendance"

attendance["attendance_category"] = attendance["attendance_rate"].apply(get_attendance_category)

teachers.to_csv(CLEANED_DATA_PATH / "teachers_cleaned.csv", index=False)
learners.to_csv(CLEANED_DATA_PATH / "learners_cleaned.csv", index=False)
enrolments.to_csv(CLEANED_DATA_PATH / "enrolments_cleaned.csv", index=False)
marks.to_csv(CLEANED_DATA_PATH / "marks_cleaned.csv", index=False)
attendance.to_csv(CLEANED_DATA_PATH / "attendance_cleaned.csv", index=False)


print("Basic cleaning completed.")