from fastapi import APIRouter, HTTPException

from backend.database import get_connection


router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"]
)


@router.get("/{decision_id}")
def get_evaluation(decision_id: str):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                evaluation_id,
                decision_id,
                cost_difference,
                delay_difference,
                cost_percentage_error,
                delay_percentage_error,
                evaluated_at
            FROM decision_evaluations
            WHERE decision_id = %s
            ORDER BY evaluation_id DESC
            LIMIT 1
            """,
            (decision_id,)
        )

        result = cursor.fetchone()

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Evaluation not found"
            )

        return {
            "evaluation_id": result[0],
            "decision_id": result[1],
            "cost_difference": float(result[2]),
            "delay_difference": float(result[3]),
            "cost_percentage_error": float(result[4]),
            "delay_percentage_error": float(result[5]),
            "evaluated_at": result[6]
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()
@router.get("/kpis")
def get_evaluation_kpis():

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*) AS evaluated_decisions,

                COUNT(*) FILTER (
                    WHERE successful = TRUE
                ) AS successful_decisions,

                COALESCE(
                    AVG(cost_percentage_error),
                    0
                ) AS average_cost_error,

                COALESCE(
                    AVG(delay_percentage_error),
                    0
                ) AS average_delay_error

            FROM decision_evaluations
            """
        )

        evaluation_result = cursor.fetchone()

        evaluated_decisions = int(evaluation_result[0] or 0)
        successful_decisions = int(evaluation_result[1] or 0)

        average_cost_error = float(
            evaluation_result[2] or 0
        )

        average_delay_error = float(
            evaluation_result[3] or 0
        )

        # -----------------------------------
        # Get total decisions
        # -----------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM decisions
            """
        )

        total_result = cursor.fetchone()

        total_decisions = int(total_result[0] or 0)

        # -----------------------------------
        # Get average predicted cost
        # -----------------------------------

        cursor.execute(
            """
            SELECT
                COALESCE(AVG(predicted_cost), 0)
            FROM decision_outcomes
            """
        )

        cost_result = cursor.fetchone()

        average_predicted_cost = float(
            cost_result[0] or 0
        )

        # -----------------------------------
        # Calculate success rate
        # -----------------------------------

        if evaluated_decisions > 0:
            success_rate = (
                successful_decisions
                / evaluated_decisions
            ) * 100
        else:
            success_rate = 0

        return {
            "total_decisions": total_decisions,

            "evaluated_decisions": evaluated_decisions,

            "successful_decisions": successful_decisions,

            "success_rate": round(success_rate, 2),

            "average_predicted_cost": round(
                average_predicted_cost,
                2
            ),

            "average_cost_error": round(
                average_cost_error,
                2
            ),

            "average_delay_error": round(
                average_delay_error,
                2
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()