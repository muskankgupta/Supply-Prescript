from fastapi import APIRouter, HTTPException

from backend.database import get_connection
from backend.models import DecisionCreate


router = APIRouter(
    prefix="/decisions",
    tags=["Decisions"],
)


@router.get("/")
def get_decisions():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                decision_id,
                shipment_id,
                recommendation_id,
                selected_action,
                predicted_cost,
                predicted_delay,
                decision_status,
                decision_timestamp
            FROM decisions
            ORDER BY decision_timestamp DESC
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
def get_decision(shipment_id: str):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                decision_id,
                shipment_id,
                recommendation_id,
                selected_action,
                predicted_cost,
                predicted_delay,
                decision_status,
                decision_timestamp
            FROM decisions
            WHERE shipment_id = %s
            ORDER BY decision_timestamp DESC
            LIMIT 1
        """, (shipment_id,))

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Decision not found for this shipment"
            )

        columns = [description[0] for description in cursor.description]

        return dict(zip(columns, row))

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@router.post("/")
def create_decision(decision: DecisionCreate):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Check that the shipment exists
        cursor.execute("""
            SELECT shipment_id
            FROM shipments
            WHERE shipment_id = %s
        """, (decision.shipment_id,))

        shipment = cursor.fetchone()

        if shipment is None:
            raise HTTPException(
                status_code=404,
                detail="Shipment not found"
            )

        # Check recommendation if one was provided
        if decision.recommendation_id:

            cursor.execute("""
                SELECT
                    recommendation_id,
                    action,
                    cost,
                    expected_delay
                FROM recommendations
                WHERE recommendation_id = %s
                  AND shipment_id = %s
            """, (
                decision.recommendation_id,
                decision.shipment_id,
            ))

            recommendation = cursor.fetchone()

            if recommendation is None:
                raise HTTPException(
                    status_code=404,
                    detail="Recommendation not found for this shipment"
                )

        # Generate a new decision ID
        cursor.execute("""
            SELECT COUNT(*)
            FROM decisions
        """)

        count = cursor.fetchone()[0]

        decision_id = f"D{count + 1:03d}"

        # Insert decision
        cursor.execute("""
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
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """, (
            decision_id,
            decision.shipment_id,
            decision.recommendation_id,
            decision.selected_action,
            decision.predicted_cost,
            decision.predicted_delay,
            decision.decision_status,
        ))

        connection.commit()

        return {
            "status": "success",
            "message": "Decision saved successfully",
            "decision_id": decision_id,
        }

    except HTTPException:
        raise

    except Exception as e:
        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save decision: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()