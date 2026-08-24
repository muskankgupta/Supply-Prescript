from fastapi import APIRouter, HTTPException
from backend.database import get_connection
router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)
@router.get("/")
def get_recommendations():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                recommendation_id,
                shipment_id,
                action,
                cost,
                expected_delay,
                risk,
                rank
            FROM recommendations
            ORDER BY shipment_id, rank
        """)

        rows = cursor.fetchall()

        columns = [description[0] for description in cursor.description]

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    except Exception as e:
        print("RECOMMENDATIONS ERROR:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@router.get("/{shipment_id}")
def get_recommendations_by_shipment(shipment_id: str):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                recommendation_id,
                shipment_id,
                action,
                cost,
                expected_delay,
                risk,
                rank
            FROM recommendations
            WHERE shipment_id = %s
            ORDER BY rank
        """, (shipment_id,))

        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(
                status_code=404,
                detail="Recommendations not found for this shipment"
            )

        columns = [description[0] for description in cursor.description]

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    except HTTPException:
        raise

    except Exception as e:
        print("RECOMMENDATION BY SHIPMENT ERROR:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()