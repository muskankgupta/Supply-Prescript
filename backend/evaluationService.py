def evaluate_outcome(
    predicted_cost,
    actual_cost,
    predicted_delay,
    actual_delay,
):
    """
    Compare predicted decision performance
    with the actual outcome.
    """

    if predicted_cost is None:
        raise ValueError("Predicted cost is missing.")

    if predicted_delay is None:
        raise ValueError("Predicted delay is missing.")

    cost_difference = (
        float(actual_cost) - float(predicted_cost)
    )

    delay_difference = (
        int(actual_delay) - int(predicted_delay)
    )

    return {
        "predicted_cost": float(predicted_cost),
        "actual_cost": float(actual_cost),
        "cost_difference": cost_difference,

        "predicted_delay": int(predicted_delay),
        "actual_delay": int(actual_delay),
        "delay_difference": delay_difference,
    }