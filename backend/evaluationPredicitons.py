from backend.database import get_connection


def calculate_percentage_error(actual, predicted):
    if actual == 0:
        return 0

    return abs(actual - predicted) / actual * 100


def evaluate_decision(decision_id):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                predicted_cost,
                actual_cost,
                predicted_delay,
                actual_delay
            FROM decision_outcomes
            WHERE decision_id = %s
            """,
            (decision_id,)
        )

        result = cursor.fetchone()

        if not result:
            print(f"No outcome found for decision {decision_id}")
            return

        predicted_cost = float(result[0])
        actual_cost = float(result[1])

        predicted_delay = float(result[2])
        actual_delay = float(result[3])


        cost_difference = actual_cost - predicted_cost

        delay_difference = actual_delay - predicted_delay

        cost_percentage_error = calculate_percentage_error(
            actual_cost,
            predicted_cost
        )

        delay_percentage_error = calculate_percentage_error(
            actual_delay,
            predicted_delay
        )

        cursor.execute(
            """
            INSERT INTO decision_evaluations
            (
                decision_id,
                cost_difference,
                delay_difference,
                cost_percentage_error,
                delay_percentage_error
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                decision_id,
                cost_difference,
                delay_difference,
                cost_percentage_error,
                delay_percentage_error
            )
        )

        connection.commit()

        print("\n===================================")
        print("      DECISION EVALUATION")
        print("===================================")

        print(f"Decision ID       : {decision_id}")

        print("\nCOST")
        print(f"Predicted Cost    : ₹{predicted_cost:,.2f}")
        print(f"Actual Cost       : ₹{actual_cost:,.2f}")
        print(f"Difference        : ₹{cost_difference:,.2f}")
        print(f"Percentage Error  : {cost_percentage_error:.2f}%")

        print("\nDELAY")
        print(f"Predicted Delay   : {predicted_delay:.2f} days")
        print(f"Actual Delay      : {actual_delay:.2f} days")
        print(f"Difference        : {delay_difference:.2f} days")
        print(f"Percentage Error  : {delay_percentage_error:.2f}%")

        print("\n===================================")

    except Exception as e:

        if connection:
            connection.rollback()

        print("Evaluation error:", e)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

if __name__ == "__main__":

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT decision_id
        FROM decision_outcomes
        """
    )

    decisions = cursor.fetchall()

    cursor.close()
    connection.close()

    for decision in decisions:
        evaluate_decision(decision[0])