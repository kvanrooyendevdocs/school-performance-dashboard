SELECT 'teachers' AS table_name, COUNT(*) AS row_count FROM teachers
UNION ALL
SELECT 'learners', COUNT(*) FROM learners
UNION ALL
SELECT 'enrolments', COUNT(*) FROM enrolments
UNION ALL
SELECT 'marks', COUNT(*) FROM marks
UNION ALL
SELECT 'attendance', COUNT(*) FROM attendance;