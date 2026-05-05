WITH learner_averages AS (
    SELECT
        l.learner_id,
        l.learner_name,
        l.grade,
        l.class_group,
        ROUND(AVG(m.mark), 1) AS average_mark,
        ROUND(AVG(a.attendance_rate), 3) AS average_attendance_rate
    FROM learners l
    LEFT JOIN marks m
        ON l.learner_id = m.learner_id
    LEFT JOIN attendance a
        ON l.learner_id = a.learner_id
    GROUP BY
        l.learner_id,
        l.learner_name,
        l.grade,
        l.class_group
)

SELECT
    learner_id,
    learner_name,
    grade,
    class_group,
    average_mark,
    average_attendance_rate,
    CASE
        WHEN average_mark < 45 AND average_attendance_rate < 0.85
            THEN 'Critical Support Needed'
        WHEN average_mark < 50
            THEN 'Academic Support Needed'
        WHEN average_attendance_rate < 0.85
            THEN 'Attendance Support Needed'
        ELSE 'On Track'
    END AS learner_status
FROM learner_averages
ORDER BY
    learner_status,
    average_mark ASC,
    average_attendance_rate ASC;