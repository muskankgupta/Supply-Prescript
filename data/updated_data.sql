
UPDATE shipments
SET product = 'Microchip'
WHERE shipment_id = 'SH1023';

DELETE FROM decisions
WHERE shipment_id = 'SH1023';

DELETE FROM recommendations
WHERE shipment_id = 'SH1023';

INSERT INTO recommendations (
    recommendation_id,
    shipment_id,
    action,
    cost,
    expected_delay,
    risk,
    rank
)
VALUES
('R001', 'SH1023', 'Air Freight', 15000, 2, 'Low', 1),
('R002', 'SH1023', 'Secondary Supplier', 12000, 4, 'Medium', 2),
('R003', 'SH1023', 'Delay Launch', 2000, 14, 'High', 3);

INSERT INTO decisions (
    decision_id,
    shipment_id,
    recommendation_id,
    selected_action,
    predicted_cost,
    predicted_delay,
    decision_status
)
VALUES (
    'D001',
    'SH1023',
    'R001',
    'Air Freight',
    15000,
    2,
    'SELECTED'
);
SELECT
    s.shipment_id,
    s.product,
    p.delay_probability,
    p.predicted_delay_days,
    r.action,
    r.cost,
    r.expected_delay,
    r.risk,
    r.rank,
    d.selected_action,
    d.decision_status
FROM shipments s
LEFT JOIN predictions p
    ON s.shipment_id = p.shipment_id
LEFT JOIN recommendations r
    ON s.shipment_id = r.shipment_id
LEFT JOIN decisions d
    ON r.recommendation_id = d.recommendation_id
WHERE s.shipment_id = 'SH1023'
ORDER BY r.rank;