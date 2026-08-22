from .actions import BusinessAction, get_actions
from .constraints import BusinessConstraints, constraints, is_feasible


def calculate_score(action: BusinessAction) -> float:
    """
    Lower score = better action.

    Objective considers:
        - total cost
        - delay penalty
        - risk penalty
    """

    delay_penalty = action.expected_delay * 1000
    risk_penalty = action.risk * 2000

    return (
        action.cost
        + delay_penalty
        + risk_penalty
    )


def optimize_actions(
    actions=None,
    constraints: BusinessConstraints = constraints
):
    """
    Find feasible actions and rank them.

    IMPORTANT:
    Infeasible actions are removed BEFORE ranking.
    """

    if actions is None:
        actions = get_actions()

    # ---------------------------------------------------------
    # Step 1: Keep only feasible actions
    # ---------------------------------------------------------

    feasible_actions = [
        action
        for action in actions
        if is_feasible(action, constraints)
    ]

    # ---------------------------------------------------------
    # Step 2: Rank feasible actions
    # ---------------------------------------------------------

    ranked_actions = sorted(
        feasible_actions,
        key=calculate_score
    )

    return ranked_actions


def print_optimization_results():

    print("\nOPTIMIZATION RESULTS")
    print("=" * 60)

    ranked_actions = optimize_actions()

    if not ranked_actions:
        print("No feasible actions available.")
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
            f"Description    : "
            f"{action.description}"
        )

        print(
            f"Cost           : "
            f"${action.cost:,.2f}"
        )

        print(
            f"Expected Delay : "
            f"{action.expected_delay} days"
        )

        print(
            f"Capacity       : "
            f"{action.capacity:,} units"
        )

        print(
            f"Risk           : "
            f"{action.risk:.2f}"
        )

        print(
            f"Score          : "
            f"{score:,.2f}"
        )


if __name__ == "__main__":
    print_optimization_results()