import pandas as pd
from faker import Faker
from pathlib import Path
import random

fake = Faker()

# This makes the fake data repeatable.
# Every time we run the script, we get the same fake names.
random.seed(42)
Faker.seed(42)

RAW_DATA_PATH = Path("data/raw")
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

subjects = [
    "Mathematics",
    "English",
    "Afrikaans",
    "Physical Science",
    "Life Science",
    "History",
    "Geography",
    "Information Technology",
    "Accounting"
]

# -----------------------------
# Create teachers
# -----------------------------

teacher_records = []
teacher_id = 1

for subject in subjects:
    for _ in range(3):
        teacher_records.append({
            "teacher_id": teacher_id,
            "teacher_name": fake.name(),
            "subject": subject
        })
        teacher_id += 1

teachers_df = pd.DataFrame(teacher_records)

teachers_df.to_csv(RAW_DATA_PATH / "teachers.csv", index=False)

# -----------------------------
# Create learners
# -----------------------------

NUM_LEARNERS = 300

grades = [8, 9, 10, 11, 12]
classes = ["A", "B", "C", "D", "E"]

learner_records = []

for learner_id in range(1, NUM_LEARNERS + 1):
    grade = random.choice(grades)
    class_letter = random.choice(classes)

    learner_records.append({
        "learner_id": learner_id,
        "learner_name": fake.name(),
        "grade": grade,
        "class_group": f"{grade}{class_letter}"
    })

learners_df = pd.DataFrame(learner_records)

learners_df.to_csv(RAW_DATA_PATH / "learners.csv", index=False)

# -----------------------------
# Create enrolments
# -----------------------------

enrolment_records = []
enrolment_id = 1

for _, learner in learners_df.iterrows():
    compulsory_subjects = ["English", "Afrikaans", "Mathematics"]

    elective_subjects = random.sample(
        [subject for subject in subjects if subject not in compulsory_subjects],
        3
    )

    learner_subjects = compulsory_subjects + elective_subjects

    for subject in learner_subjects:
        possible_teachers = teachers_df[teachers_df["subject"] == subject]
        teacher = possible_teachers.sample(1).iloc[0]

        enrolment_records.append({
            "enrolment_id": enrolment_id,
            "learner_id": learner["learner_id"],
            "subject": subject,
            "teacher_id": teacher["teacher_id"]
        })

        enrolment_id += 1

enrolments_df = pd.DataFrame(enrolment_records)

enrolments_df.to_csv(RAW_DATA_PATH / "enrolments.csv", index=False)

# -----------------------------
# Create marks
# -----------------------------

terms = [1, 2, 3, 4]

mark_records = []
mark_id = 1

for _, enrolment in enrolments_df.iterrows():
    # Each learner/subject combination gets a base ability score
    base_ability = random.randint(45, 85)

    for term in terms:
        # Small random change per term to simulate improvement or decline
        term_change = random.randint(-8, 8)

        subject_difficulty = {
            "Mathematics": -5,
            "Physical Science": -7,
            "Information Technology": -2,
            "Accounting": -3,
            "English": 2,
            "Afrikaans": 0,
            "Life Science": 1,
            "History": 3,
            "Geography": 2
        }.get(enrolment["subject"], 0)

        mark = base_ability + term_change + subject_difficulty

        # Keep marks between 0 and 100
        mark = max(0, min(100, mark))

        mark_records.append({
            "mark_id": mark_id,
            "learner_id": enrolment["learner_id"],
            "subject": enrolment["subject"],
            "teacher_id": enrolment["teacher_id"],
            "term": term,
            "mark": mark
        })

        mark_id += 1

marks_df = pd.DataFrame(mark_records)

marks_df.to_csv(RAW_DATA_PATH / "marks.csv", index=False)

# -----------------------------
# Create attendance
# -----------------------------

attendance_records = []
attendance_id = 1

for _, learner in learners_df.iterrows():
    for term in terms:
        days_possible = random.randint(45, 55)

        # Most learners attend well, but some have weaker attendance
        attendance_rate = random.uniform(0.78, 0.98)

        days_present = round(days_possible * attendance_rate)
        days_absent = days_possible - days_present

        attendance_records.append({
            "attendance_id": attendance_id,
            "learner_id": learner["learner_id"],
            "term": term,
            "days_possible": days_possible,
            "days_present": days_present,
            "days_absent": days_absent,
            "attendance_rate": round(days_present / days_possible, 3)
        })

        attendance_id += 1

attendance_df = pd.DataFrame(attendance_records)

attendance_df.to_csv(RAW_DATA_PATH / "attendance.csv", index=False)

print("Teachers data generated.")
print("Learners data generated.")
print("Enrolments data generated.")
print("Marks data generated.")
print("Attendance data generated.")
print(attendance_df.head())