CREATE TABLE IF NOT EXISTS outcome_evaluations (
    evaluation_id SERIAL PRIMARY KEY,

    decision_id VARCHAR(50) NOT NULL,

    predicted_cost NUMERIC(12,2),
    actual_cost NUMERIC(12,2),
    cost_difference NUMERIC(12,2),

    predicted_delay INTEGER,
    actual_delay INTEGER,
    delay_difference INTEGER,

    success BOOLEAN,
    evaluation_note TEXT,

    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SELECT *
FROM outcome_evaluations;
SELECT *
FROM outcome_evaluations
ORDER BY evaluated_at DESC;