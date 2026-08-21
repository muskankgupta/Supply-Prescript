from .actions import BusinessAction, get_actions
from .constraints import BusinessConstraints, constraints, validate_action


def calculate_score(action: BusinessAction) -> float:
   # Calculate the optimization score. Lower score = better action.
   
    #Objective considers:Total cost, Delay penalty, Risk penalty
    # Penalty for expected delay
    delay_penalty = action.expected_delay * 1000

    # Penalty for risk
    risk_penalty = action.risk * 2000

    return (
        action.cost
        + delay_penalty
        + risk_penalty
    )


def optimize_actions(
    actions=None,
    business_constraints: BusinessConstraints = constraints
):
    """
    Find feasible business actions and rank them
    using the optimization objective.

    Steps:
    1. Get available business actions.
    2. Validate each action against constraints.
    3. Remove actions that violate constraints.
    4. Calculate optimization score.
    5. Rank feasible actions.
    """

    # Get default actions
    if actions is None:
        actions = get_actions()

    feasible_actions = []

    # Validate every action
    for action in actions:

        violations = validate_action(
            action,
            business_constraints
        )

        # Action is feasible if there are no violations
        if not violations:
            feasible_actions.append(action)

    # Rank feasible actions
    ranked_actions = sorted(
        feasible_actions,
        key=calculate_score
    )

    return ranked_actions


def print_optimization_results(
    ranked_actions
):
    """
    Display the ranked optimization results.
    """

    print("\nOPTIMIZATION RESULTS")


    if not ranked_actions:
        print("No feasible actions found.")
        return

    for index, action in enumerate(
        ranked_actions,
        start=1
    ):

        score = calculate_score(action)

        print(
            f"\nRank {index}: {action.name}"
        )

        print(
            f"Description     : "
            f"{action.description}"
        )

        print(
            f"Cost            : "
            f"${action.cost:,.2f}"
        )

        print(
            f"Expected Delay  : "
            f"{action.expected_delay} days"
        )

        print(
            f"Capacity        : "
            f"{action.capacity:,} units"
        )

        print(
            f"Risk            : "
            f"{action.risk:.2f}"
        )

        print(
            f"Optimization Score : "
            f"{score:,.2f}"
        )


if __name__ == "__main__":

    ranked_actions = optimize_actions()

    print_optimization_results(
        ranked_actions
    )