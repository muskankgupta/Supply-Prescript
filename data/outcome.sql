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

CREATE TABLE IF NOT EXISTS decision_roi (
    roi_id SERIAL PRIMARY KEY,

    decision_id INTEGER NOT NULL,

    baseline_cost NUMERIC(12,2),
    recommended_cost NUMERIC(12,2),
    actual_cost NUMERIC(12,2),

    savings NUMERIC(12,2),
    roi_percent NUMERIC(10,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SELECT *
FROM outcome_evaluations;
SELECT *
FROM outcome_evaluations
ORDER BY evaluated_at DESC;
CREATE TABLE IF NOT EXISTS outcomes (
    outcome_id SERIAL PRIMARY KEY,

    decision_id VARCHAR(100) NOT NULL,

    shipment_id VARCHAR(100) NOT NULL,

    actual_cost NUMERIC(12, 2),

    actual_delay INTEGER,

    actual_delivery_date DATE,

    outcome_status VARCHAR(50) NOT NULL,

    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from outcomes;
CREATE TABLE IF NOT EXISTS decision_outcomes (
    outcome_id SERIAL PRIMARY KEY,

    decision_id VARCHAR(50) NOT NULL,

    predicted_cost NUMERIC(12,2),
    actual_cost NUMERIC(12,2),

    predicted_delay NUMERIC(10,2),
    actual_delay NUMERIC(10,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS decision_evaluations (
    evaluation_id SERIAL PRIMARY KEY,

    decision_id VARCHAR(50) NOT NULL,

    cost_difference NUMERIC(12,2),
    delay_difference NUMERIC(10,2),

    cost_percentage_error NUMERIC(10,2),
    delay_percentage_error NUMERIC(10,2),

    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO decision_outcomes
(
    decision_id,
    predicted_cost,
    actual_cost,
    predicted_delay,
    actual_delay
)
VALUES
(
    'D017',
    15000,
    18000,
    2,
    4
);
select * from decision_outcomes;