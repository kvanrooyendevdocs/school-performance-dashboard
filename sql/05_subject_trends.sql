WITH subject_term_averages AS (
    SELECT
        subject,
        term,
        ROUND(AVG(mark), 1) AS average_mark
    FROM marks
    GROUP BY subject, term
),

subject_trends AS (
    SELECT
        subject,
        MAX(CASE WHEN term = 1 THEN average_mark END) AS term_1_average,
        MAX(CASE WHEN term = 2 THEN average_mark END) AS term_2_average,
        MAX(CASE WHEN term = 3 THEN average_mark END) AS term_3_average,
        MAX(CASE WHEN term = 4 THEN average_mark END) AS term_4_average
    FROM subject_term_averages
    GROUP BY subject
)

SELECT
    subject,
    term_1_average,
    term_2_average,
    term_3_average,
    term_4_average,
    ROUND(term_4_average - term_1_average, 1) AS change_t1_to_t4
FROM subject_trends
ORDER BY change_t1_to_t4 ASC;