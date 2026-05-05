SELECT
    subject,
    ROUND(AVG(mark), 1) AS average_mark,
    MIN(mark) AS lowest_mark,
    MAX(mark) AS highest_mark,
    COUNT(*) AS number_of_marks
FROM marks
GROUP BY subject
ORDER BY average_mark ASC;