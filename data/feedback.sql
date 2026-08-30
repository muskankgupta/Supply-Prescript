CREATE TABLE IF NOT EXISTS decision_feedback (
    feedback_id SERIAL PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    outcome VARCHAR(50) NOT NULL,
    actual_cost NUMERIC(12,2),
    actual_delay NUMERIC(10,2),
    success BOOLEAN NOT NULL,
    feedback_note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);