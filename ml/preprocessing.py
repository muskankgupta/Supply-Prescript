import pandas as pd
FEATURE_COLUMNS = [
    "supplier_id",
    "product",
    "origin",
    "destination",
    "order_quantity",
    "inventory_level",
    "historical_lead_time",
    "supplier_reliability",
    "weather_risk",
    "transportation_mode",
    "previous_delays"
]
def prepare_shipment(shipment):
    """
    Convert shipment information into a DataFrame
    suitable for the trained ML model.
    """

    if not isinstance(shipment, dict):
        raise TypeError(
            "Shipment information must be provided as a dictionary."
        )
    required_fields = FEATURE_COLUMNS
    missing_fields = [
        field
        for field in required_fields
        if field not in shipment
    ]
    if missing_fields:
        raise ValueError(
            f"Missing required fields: {missing_fields}"
        )
    data = {
        field: shipment[field]
        for field in FEATURE_COLUMNS
    }
    return pd.DataFrame(
        [data],
        columns=FEATURE_COLUMNS
    )