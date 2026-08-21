from fastapi import APIRouter, HTTPException

from backend.database import get_connection


router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


@router.get("/")
def get_predictions():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                prediction_id,
                shipment_id,
                delay_probability,
                predicted_delay_days,
                prediction_date
            FROM predictions
            ORDER BY prediction_date DESC, prediction_id
        """)

        rows = cursor.fetchall()

        columns = [description[0] for description in cursor.description]

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@router.get("/{shipment_id}")
def get_prediction(shipment_id: str):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                prediction_id,
                shipment_id,
                delay_probability,
                predicted_delay_days,
                prediction_date
            FROM predictions
            WHERE shipment_id = %s
            ORDER BY prediction_date DESC
            LIMIT 1
        """, (shipment_id,))

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Prediction not found for this shipment"
            )

        columns = [description[0] for description in cursor.description]

        return dict(zip(columns, row))

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()