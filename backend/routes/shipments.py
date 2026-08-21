from fastapi import APIRouter, HTTPException

from backend.database import get_connection


router = APIRouter(
    prefix="/shipments",
    tags=["Shipments"],
)


@router.get("/")
def get_shipments():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                shipment_id,
                supplier_id,
                product,
                origin,
                destination,
                quantity,
                inventory_level,
                expected_delivery_date
            FROM shipments
            ORDER BY shipment_id
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
def get_shipment(shipment_id: str):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                shipment_id,
                supplier_id,
                product,
                origin,
                destination,
                quantity,
                inventory_level,
                expected_delivery_date
            FROM shipments
            WHERE shipment_id = %s
        """, (shipment_id,))

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Shipment not found"
            )

        columns = [description[0] for description in cursor.description]

        return dict(zip(columns, row))

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()