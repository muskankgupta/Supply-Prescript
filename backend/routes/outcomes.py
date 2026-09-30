from fastapi import APIRouter, HTTPException

from backend.database import get_connection
from backend.models import OutcomeCreate


router = APIRouter(
    prefix="/outcomes",
    tags=["Outcomes"],
)


@router.post("/")
def create_outcome(outcome: OutcomeCreate):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # --------------------------------------------------
        # Check whether the decision exists
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT decision_id
            FROM decisions
            WHERE decision_id = %s
            """,
            (outcome.decision_id,)
        )

        decision = cursor.fetchone()

        if not decision:
            raise HTTPException(
                status_code=404,
                detail="Decision not found."
            )

        # --------------------------------------------------
        # Insert actual outcome
        # --------------------------------------------------

        cursor.execute(
            """
            INSERT INTO outcomes (
                decision_id,
                shipment_id,
                actual_cost,
                actual_delay,
                actual_delivery_date,
                outcome_status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING outcome_id
            """,
            (
                outcome.decision_id,
                outcome.shipment_id,
                outcome.actual_cost,
                outcome.actual_delay,
                outcome.actual_delivery_date,
                outcome.outcome_status,
            )
        )

        outcome_id = cursor.fetchone()[0]

        connection.commit()

        return {
            "message": "Actual outcome recorded successfully.",
            "outcome_id": outcome_id,
            "decision_id": outcome.decision_id,
            "shipment_id": outcome.shipment_id,
            "actual_cost": outcome.actual_cost,
            "actual_delay": outcome.actual_delay,
            "actual_delivery_date": outcome.actual_delivery_date,
            "outcome_status": outcome.outcome_status,
        }

    except HTTPException:
        if connection:
            connection.rollback()
        raise

    except Exception as error:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to record outcome: {str(error)}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ------------------------------------------------------
# GET ALL OUTCOMES
# ------------------------------------------------------

@router.get("/")
def get_outcomes():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                outcome_id,
                decision_id,
                shipment_id,
                actual_cost,
                actual_delay,
                actual_delivery_date,
                outcome_status,
                recorded_at
            FROM outcomes
            ORDER BY outcome_id DESC
            """
        )

        rows = cursor.fetchall()

        outcomes = []

        for row in rows:

            outcomes.append({
                "outcome_id": row[0],
                "decision_id": row[1],
                "shipment_id": row[2],
                "actual_cost": float(row[3]) if row[3] is not None else None,
                "actual_delay": row[4],
                "actual_delivery_date": row[5],
                "outcome_status": row[6],
                "recorded_at": row[7],
            })

        return outcomes

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch outcomes: {str(error)}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()