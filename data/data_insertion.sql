INSERT INTO shipments (
    shipment_id,
    supplier_id,
    product,
    origin,
    destination,
    quantity,
    inventory_level,
    expected_delivery_date
)
VALUES
(
    'SH1023',
    'SUP001',
    'Laptop',
    'Delhi',
    'Mumbai',
    100,
    25,
    '2026-08-25'
),
(
    'SH1024',
    'SUP002',
    'Monitor',
    'Bangalore',
    'Delhi',
    50,
    80,
    '2026-08-24'
),
(
    'SH1025',
    'SUP003',
    'Keyboard',
    'Chennai',
    'Hyderabad',
    200,
    40,
    '2026-08-26'
);
INSERT INTO predictions (
    prediction_id,
    shipment_id,
    delay_probability,
    predicted_delay_days,
    prediction_date
)
VALUES (
    'P001',
    'SH1023',
    0.8700,
    14,
    '2026-08-17'
);
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
(
    'R001',
    'SH1023',
    'Air Freight',
    15000,
    2,
    'Low',
    1
),
(
    'R002',
    'SH1023',
    'Expedited Road',
    9000,
    5,
    'Medium',
    2
),
(
    'R003',
    'SH1023',
    'Standard Freight',
    5000,
    12,
    'High',
    3
);
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
    s.origin,
    s.destination,
    s.quantity,
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