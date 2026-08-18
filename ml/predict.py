from pathlib import Path
import joblib

from preprocessing import prepare_shipment
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "delay_model.pkl"
)
def load_model():
    """
    Load the trained XGBoost model and preprocessor.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at: {MODEL_PATH}\n"
            "Run the Day 4 training script first."
        )

    model_bundle = joblib.load(MODEL_PATH)
    return model_bundle
def predict_delay(shipment):
    """
    Predict the probability that a shipment will be delayed.

    Returns:
        {
            "shipment_id": "...",
            "delay_probability": 0.87
        }
    """
    if "shipment_id" not in shipment:
        raise ValueError(
            "shipment_id is required."
        )
    bundle = load_model()
    model = bundle["model"]
    preprocessor = bundle["preprocessor"]
    shipment_id = shipment["shipment_id"]
    # Prepare input
    input_data = prepare_shipment(shipment)
    # Apply the SAME preprocessing used during training
    processed_data = preprocessor.transform(
        input_data
    )
    # Predict probability of delay
    delay_probability = model.predict_proba(
        processed_data
    )[0][1]
    return {
        "shipment_id": shipment_id,
        "delay_probability": round(
            float(delay_probability),
            2
        )
    }


if __name__ == "__main__":

    example_shipment = {
        "shipment_id": "SHP1023",

        "supplier_id": "SUP003",

        "product": "Microchip",

        "origin": "China",

        "destination": "India",

        "order_quantity": 2500,

        "inventory_level": 1200,

        "historical_lead_time": 20,

        "supplier_reliability": 0.78,

        "weather_risk": 0.85,

        "transportation_mode": "Sea",

        "previous_delays": 3
    }

    result = predict_delay(
        example_shipment
    )

    print("\nPrediction Result:")
    print(result)