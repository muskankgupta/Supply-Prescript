from fastapi import APIRouter, HTTPException

from backend.database import get_connection
from backend.models import FeedbackCreate


router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)


@router.post("/")
def create_feedback(feedback: FeedbackCreate):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
#Actual decision
        cursor.execute(
            """
            SELECT
                predicted_cost,
                predicted_delay
            FROM decisions
            WHERE decision_id = %s
            """,
            (feedback.decision_id,)
        )

        decision = cursor.fetchone()
        if not decision:
            raise HTTPException(
                status_code=404,
                detail=f"Decision {feedback.decision_id} not found"
            )
        predicted_cost = decision[0]
        predicted_delay = decision[1]

        if predicted_cost is None:
            raise HTTPException(
                status_code=400,
                detail="Predicted cost is missing for this decision."
            )
        if predicted_delay is None:
            raise HTTPException(
                status_code=400,
                detail="Predicted delay is missing for this decision."
            )
        #calculate difference
        cost_difference = (
            float(feedback.actual_cost)
            - float(predicted_cost)
        )

        delay_difference = (
            int(feedback.actual_delay)
            - int(predicted_delay)
        )
        #Store feedback
        cursor.execute(
            """
            INSERT INTO decision_feedback
            (
                decision_id,
                outcome,
                actual_cost,
                actual_delay,
                success,
                feedback_note
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING feedback_id
            """,
            (
                feedback.decision_id,
                feedback.outcome,
                feedback.actual_cost,
                feedback.actual_delay,
                feedback.success,
                feedback.feedback_note,
            ),
        )
#Store outcome evaluation
        cursor.execute(
            """
            INSERT INTO outcome_evaluations (
                decision_id,
                predicted_cost,
                actual_cost,
                cost_difference,
                predicted_delay,
                actual_delay,
                delay_difference,
                success,
                evaluation_note
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                feedback.decision_id,
                predicted_cost,
                feedback.actual_cost,
                cost_difference,
                predicted_delay,
                feedback.actual_delay,
                delay_difference,
                feedback.success,
                feedback.feedback_note,
            )
        )

        connection.commit()

        return {
            "message": "Feedback and outcome evaluation recorded successfully",
            "decision_id": feedback.decision_id,

            "predicted_cost": float(predicted_cost),
            "actual_cost": float(feedback.actual_cost),
            "cost_difference": cost_difference,

            "predicted_delay": int(predicted_delay),
            "actual_delay": int(feedback.actual_delay),
            "delay_difference": delay_difference,

            "success": feedback.success,
        }
        feedback_id = cursor.fetchone()[0]

        connection.commit()

        return {
            "message": "Feedback recorded successfully",
            "feedback_id": feedback_id,
            "decision_id": feedback.decision_id,
        }

    except HTTPException:
        if connection:
            connection.rollback()
        raise

    except Exception as error:
        if connection:
            connection.rollback()

        print("Feedback error:", error)

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


@router.get("/")
def get_feedback():

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                feedback_id,
                decision_id,
                outcome,
                actual_cost,
                actual_delay,
                success,
                feedback_note
            FROM decision_feedback
            ORDER BY feedback_id DESC
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "feedback_id": row[0],
                "decision_id": row[1],
                "outcome": row[2],
                "actual_cost": row[3],
                "actual_delay": row[4],
                "success": row[5],
                "feedback_note": row[6],
            }
            for row in rows
        ]

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()