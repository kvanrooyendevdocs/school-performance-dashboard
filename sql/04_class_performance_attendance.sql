WITH class_marks AS (
    SELECT
        l.class_group,
        ROUND(AVG(m.mark), 1) AS average_mark,
        MIN(m.mark) AS lowest_mark,
        MAX(m.mark) AS highest_mark,
        COUNT(*) AS number_of_marks
    FROM marks m
    JOIN learners l
        ON m.learner_id = l.learner_id
    GROUP BY l.class_group
),

class_attendance AS (
    SELECT
        l.class_group,
        ROUND(AVG(a.attendance_rate) * 100, 1) AS average_attendance_rate,
        ROUND(MIN(a.attendance_rate) * 100, 1) AS lowest_attendance_rate,
        ROUND(MAX(a.attendance_rate) * 100, 1) AS highest_attendance_rate
    FROM attendance a
    JOIN learners l
        ON a.learner_id = l.learner_id
    GROUP BY l.class_group
)

SELECT
    cm.class_group,
    cm.average_mark,
    ca.average_attendance_rate,
    cm.lowest_mark,
    cm.highest_mark,
    cm.number_of_marks,
    ca.lowest_attendance_rate,
    ca.highest_attendance_rate
FROM class_marks cm
JOIN class_attendance ca
    ON cm.class_group = ca.class_group
ORDER BY
    cm.average_mark ASC,
    ca.average_attendance_rate ASC;