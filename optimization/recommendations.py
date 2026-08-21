from .optimizer import optimize_actions
def generate_recommendations(
    shipment,
    actions=None,
    constraints=None
):
    """
    Generate the three best actions for a shipment.
    """

    if constraints is None:
        ranked_actions = optimize_actions(
            actions=actions
        )
    else:
        ranked_actions = optimize_actions(
            actions=actions,
            constraints=constraints
        )

    recommendations = []

    for action in ranked_actions[:3]:

        recommendations.append({
            "action": action.name,
            "cost": action.cost,
            "expected_delay": action.expected_delay,
            "risk": action.risk
        })

    return recommendations
shipment = {
    "shipment_id": "SH1023",
    "delay_probability": 0.87
}

recommendations = generate_recommendations(shipment)

print(recommendations)