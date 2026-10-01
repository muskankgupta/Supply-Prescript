from fastapi import APIRouter, HTTPException

from backend.database import get_connection


router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"],
)


@router.get("/kpis")
def get_kpis():

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # ---------------------------------------------------------
        # TOTAL DECISIONS
        # ---------------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM decisions
            """
        )

        total_decisions = cursor.fetchone()[0] or 0

        # ---------------------------------------------------------
        # EVALUATED DECISIONS
        # ---------------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM decision_evaluations
            """
        )

        evaluated_decisions = cursor.fetchone()[0] or 0

        # ---------------------------------------------------------
        # SUCCESSFUL DECISIONS
        # ---------------------------------------------------------

        cursor.execute(
    """
    SELECT COUNT(*)
    FROM decision_evaluations
    WHERE cost_percentage_error <= 20
      AND delay_percentage_error <= 20
    """
)

        successful_decisions = cursor.fetchone()[0] or 0

        # ---------------------------------------------------------
        # SUCCESS RATE
        # ---------------------------------------------------------

        if evaluated_decisions > 0:
            success_rate = (
                successful_decisions / evaluated_decisions
            ) * 100
        else:
            success_rate = 0

        # ---------------------------------------------------------
        # AVERAGE PREDICTED COST
        # ---------------------------------------------------------

        cursor.execute(
            """
            SELECT COALESCE(AVG(predicted_cost), 0)
            FROM decision_outcomes
            """
        )

        average_predicted_cost = cursor.fetchone()[0] or 0

        # ---------------------------------------------------------
        # AVERAGE COST ERROR
        # ---------------------------------------------------------

        cursor.execute(
            """
            SELECT COALESCE(AVG(cost_percentage_error), 0)
            FROM decision_evaluations
            """
        )

        average_cost_error = cursor.fetchone()[0] or 0

        # ---------------------------------------------------------
        # AVERAGE DELAY ERROR
        # ---------------------------------------------------------

        cursor.execute(
            """
            SELECT COALESCE(AVG(delay_percentage_error), 0)
            FROM decision_evaluations
            """
        )

        average_delay_error = cursor.fetchone()[0] or 0

        # ---------------------------------------------------------
        # RETURN KPI DATA
        # ---------------------------------------------------------

        return {
            "total_decisions": int(total_decisions),
            "evaluated_decisions": int(evaluated_decisions),
            "successful_decisions": int(successful_decisions),
            "success_rate": round(float(success_rate), 2),
            "average_predicted_cost": round(
                float(average_predicted_cost), 2
            ),
            "average_cost_error": round(
                float(average_cost_error), 2
            ),
            "average_delay_error": round(
                float(average_delay_error), 2
            ),
        }

    except Exception as e:

        print("ERROR loading KPIs:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Failed to load KPI data: {str(e)}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()