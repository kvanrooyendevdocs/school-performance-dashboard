DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS marks;
DROP TABLE IF EXISTS enrolments;
DROP TABLE IF EXISTS learners;
DROP TABLE IF EXISTS teachers;

CREATE TABLE teachers (
    teacher_id INTEGER PRIMARY KEY,
    teacher_name TEXT,
    subject TEXT
);

CREATE TABLE learners (
    learner_id INTEGER PRIMARY KEY,
    learner_name TEXT,
    grade INTEGER,
    class_group TEXT
);

CREATE TABLE enrolments (
    enrolment_id INTEGER PRIMARY KEY,
    learner_id INTEGER,
    subject TEXT,
    teacher_id INTEGER,
    FOREIGN KEY (learner_id) REFERENCES learners(learner_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

CREATE TABLE marks (
    mark_id INTEGER PRIMARY KEY,
    learner_id INTEGER,
    subject TEXT,
    teacher_id INTEGER,
    term INTEGER,
    mark NUMERIC,
    risk_category TEXT,
    FOREIGN KEY (learner_id) REFERENCES learners(learner_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

CREATE TABLE attendance (
    attendance_id INTEGER PRIMARY KEY,
    learner_id INTEGER,
    term INTEGER,
    days_possible INTEGER,
    days_present INTEGER,
    days_absent INTEGER,
    attendance_rate NUMERIC,
    attendance_category TEXT,
    FOREIGN KEY (learner_id) REFERENCES learners(learner_id)
);