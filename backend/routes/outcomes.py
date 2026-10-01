from fastapi import APIRouter, HTTPException

from backend.database import get_connection


router = APIRouter(
    prefix="/outcomes",
    tags=["Outcomes"],
)


@router.post("/")
def create_outcome(outcome: dict):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # =========================================================
        # 1. READ DATA FROM FRONTEND
        # =========================================================

        decision_id = outcome.get("decision_id")
        shipment_id = outcome.get("shipment_id")
        actual_cost = outcome.get("actual_cost")
        actual_delay = outcome.get("actual_delay")
        actual_delivery_date = outcome.get("actual_delivery_date")
        outcome_status = outcome.get("outcome_status")

        print("Received outcome:")
        print(outcome)

        # =========================================================
        # 2. VALIDATE DECISION ID
        # =========================================================

        if not decision_id:
            raise HTTPException(
                status_code=400,
                detail="decision_id is required"
            )

        # =========================================================
        # 3. FIND ORIGINAL DECISION
        # =========================================================

        cursor.execute(
            """
            SELECT
                decision_id,
                predicted_cost,
                predicted_delay
            FROM decisions
            WHERE decision_id = %s
            """,
            (decision_id,)
        )

        decision = cursor.fetchone()

        if not decision:
            raise HTTPException(
                status_code=404,
                detail=f"Invalid decision ID: {decision_id}. Please execute the decision again."
            )

        predicted_cost = decision[1]
        predicted_delay = decision[2]

        print("Decision found:")
        print("Decision ID:", decision_id)
        print("Predicted cost:", predicted_cost)
        print("Predicted delay:", predicted_delay)

        # =========================================================
        # 4. VALIDATE ACTUAL VALUES
        # =========================================================

        if actual_cost is None:
            raise HTTPException(
                status_code=400,
                detail="actual_cost is required"
            )

        if actual_delay is None:
            raise HTTPException(
                status_code=400,
                detail="actual_delay is required"
            )

        actual_cost = float(actual_cost)
        actual_delay = float(actual_delay)

        predicted_cost = float(predicted_cost)
        predicted_delay = float(predicted_delay)

        # =========================================================
        # 5. CALCULATE ERRORS
        # =========================================================

        cost_difference = actual_cost - predicted_cost
        delay_difference = actual_delay - predicted_delay

        # Percentage error
        if actual_cost != 0:
            cost_percentage_error = (
                abs(actual_cost - predicted_cost)
                / actual_cost
            ) * 100
        else:
            cost_percentage_error = 0

        if actual_delay != 0:
            delay_percentage_error = (
                abs(actual_delay - predicted_delay)
                / actual_delay
            ) * 100
        else:
            delay_percentage_error = 0

        # =========================================================
        # 6. DETERMINE SUCCESS
        # =========================================================

        SUCCESS_THRESHOLD = 20.0

        successful = (
    outcome_status == "COMPLETED"
    and cost_percentage_error <= SUCCESS_THRESHOLD
    and delay_percentage_error <= SUCCESS_THRESHOLD
)

        print("Evaluation:")
        print("Cost difference:", cost_difference)
        print("Delay difference:", delay_difference)
        print("Cost error:", cost_percentage_error)
        print("Delay error:", delay_percentage_error)
        print("Successful:", successful)

        # =========================================================
        # 7. INSERT ACTUAL OUTCOME
        # =========================================================
        #
        # IMPORTANT:
        # Your current decision_outcomes table does NOT contain
        # actual_delivery_date.
        #
        # Therefore we only insert columns that currently exist.
        #

        cursor.execute(
            """
            INSERT INTO decision_outcomes
            (
                decision_id,
                predicted_cost,
                actual_cost,
                predicted_delay,
                actual_delay
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING outcome_id
            """,
            (
                decision_id,
                predicted_cost,
                actual_cost,
                predicted_delay,
                actual_delay,
            )
        )

        outcome_id = cursor.fetchone()[0]

        # =========================================================
        # 8. INSERT EVALUATION
        # =========================================================

        cursor.execute(
            """
            INSERT INTO decision_evaluations
            (
                decision_id,
                cost_difference,
                delay_difference,
                cost_percentage_error,
                delay_percentage_error,
                successful
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                decision_id,
                cost_difference,
                delay_difference,
                cost_percentage_error,
                delay_percentage_error,
                successful,
            )
        )

        # =========================================================
        # 9. COMMIT EVERYTHING
        # =========================================================

        connection.commit()

        print("Outcome recorded successfully.")
        print("Outcome ID:", outcome_id)

        # =========================================================
        # 10. SEND RESPONSE TO FRONTEND
        # =========================================================

        return {
            "message": "Actual outcome recorded successfully",

            "outcome_id": outcome_id,

            "decision_id": decision_id,

            "shipment_id": shipment_id,

            "predicted_cost": predicted_cost,

            "actual_cost": actual_cost,

            "predicted_delay": predicted_delay,

            "actual_delay": actual_delay,

            "actual_delivery_date": actual_delivery_date,

            "outcome_status": outcome_status,

            "cost_difference": round(cost_difference, 2),

            "delay_difference": round(delay_difference, 2),

            "cost_percentage_error": round(
                cost_percentage_error,
                2
            ),

            "delay_percentage_error": round(
                delay_percentage_error,
                2
            ),

            "successful": successful,
        }

    # =============================================================
    # HANDLE FASTAPI ERRORS
    # =============================================================

    except HTTPException:

        if connection:
            connection.rollback()

        raise

    # =============================================================
    # HANDLE DATABASE / OTHER ERRORS
    # =============================================================

    except Exception as e:

        if connection:
            connection.rollback()

        print(
            "ERROR recording outcome:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=f"Failed to record outcome: {str(e)}"
        )

    # =============================================================
    # CLOSE DATABASE
    # =============================================================

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()