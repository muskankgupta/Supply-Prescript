from fastapi import APIRouter, HTTPException

from backend.database import get_connection
from backend.models import FeedbackCreate
from backend.evaluationService import evaluate_outcome


router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)


# CREATE FEEDBACK + EVALUATE OUTCOME
@router.post("/")
def create_feedback(feedback: FeedbackCreate):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # 1. GET ORIGINAL DECISION
      
        cursor.execute(
            """
            SELECT
                predicted_cost,
                predicted_delay
            FROM decisions
            WHERE decision_id = %s
            """,
            (feedback.decision_id,),
        )

        decision = cursor.fetchone()

        if not decision:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Decision "
                    f"{feedback.decision_id} not found"
                ),
            )

        predicted_cost = decision[0]
        predicted_delay = decision[1]
        # 2. EVALUATE ACTUAL VS PREDICTED OUTCOME
    
        try:

            evaluation = evaluate_outcome(
                predicted_cost=predicted_cost,
                actual_cost=feedback.actual_cost,
                predicted_delay=predicted_delay,
                actual_delay=feedback.actual_delay,
            )

        except ValueError as error:

            raise HTTPException(
                status_code=400,
                detail=str(error),
            )
        # 3. STORE FEEDBACK
    
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
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
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

        feedback_id = cursor.fetchone()[0]
        # 4. STORE OUTCOME EVALUATION
        cursor.execute(
            """
            INSERT INTO outcome_evaluations
            (
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
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                feedback.decision_id,

                evaluation["predicted_cost"],
                evaluation["actual_cost"],
                evaluation["cost_difference"],

                evaluation["predicted_delay"],
                evaluation["actual_delay"],
                evaluation["delay_difference"],

                feedback.success,
                feedback.feedback_note,
            ),
        )
        # 5. COMMIT
      
        connection.commit()
        # 6. RETURN EVALUATION
       
        return {
            "message": (
                "Feedback and outcome "
                "evaluation recorded successfully"
            ),

            "feedback_id": feedback_id,

            "decision_id": feedback.decision_id,

            "predicted_cost": (
                evaluation["predicted_cost"]
            ),

            "actual_cost": (
                evaluation["actual_cost"]
            ),

            "cost_difference": (
                evaluation["cost_difference"]
            ),

            "predicted_delay": (
                evaluation["predicted_delay"]
            ),

            "actual_delay": (
                evaluation["actual_delay"]
            ),

            "delay_difference": (
                evaluation["delay_difference"]
            ),

            "success": feedback.success,
        }

    except HTTPException:

        if connection:
            connection.rollback()

        raise

    except Exception as error:

        if connection:
            connection.rollback()

        print(
            "Feedback error:",
            error,
        )

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# GET ALL FEEDBACK

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

    except Exception as error:

        print(
            "Get feedback error:",
            error,
        )

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()