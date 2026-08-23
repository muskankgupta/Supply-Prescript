CREATE TABLE shipments (
    shipment_id VARCHAR(50) PRIMARY KEY,
    supplier_id VARCHAR(50) NOT NULL,
    product VARCHAR(255) NOT NULL,
    origin VARCHAR(100),
    destination VARCHAR(100),
    quantity INTEGER NOT NULL,
    inventory_level INTEGER,
    expected_delivery_date DATE
);
CREATE TABLE predictions (
    prediction_id VARCHAR(50) PRIMARY KEY,
    shipment_id VARCHAR(50) NOT NULL,
    delay_probability NUMERIC(5,4),
    predicted_delay_days INTEGER,
    prediction_date DATE NOT NULL,
    
    CONSTRAINT fk_prediction_shipment
        FOREIGN KEY (shipment_id)
        REFERENCES shipments(shipment_id)
);
CREATE TABLE recommendations (
    recommendation_id VARCHAR(50) PRIMARY KEY,
    shipment_id VARCHAR(50) NOT NULL,
    action VARCHAR(100) NOT NULL,
    cost NUMERIC(12,2),
    expected_delay INTEGER,
    risk VARCHAR(50),
    rank INTEGER,
    
    CONSTRAINT fk_recommendation_shipment
        FOREIGN KEY (shipment_id)
        REFERENCES shipments(shipment_id)
);
CREATE TABLE decisions (
    decision_id VARCHAR(50) PRIMARY KEY,
    shipment_id VARCHAR(50) NOT NULL,
    recommendation_id VARCHAR(50),
    selected_action VARCHAR(100) NOT NULL,
    predicted_cost NUMERIC(12,2),
    predicted_delay INTEGER,
    decision_status VARCHAR(50) NOT NULL,
    decision_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_decision_shipment
        FOREIGN KEY (shipment_id)
        REFERENCES shipments(shipment_id),
        
    CONSTRAINT fk_decision_recommendation
        FOREIGN KEY (recommendation_id)
        REFERENCES recommendations(recommendation_id)
);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;