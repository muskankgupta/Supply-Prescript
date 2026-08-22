from dataclasses import dataclass
@dataclass
class BusinessConstraints:
    maximum_budget: float
    maximum_delay: float
    available_capacity: int
# Business constraints for the supply chain optimization problem
constraints = BusinessConstraints(
    maximum_budget=20000,
    maximum_delay=5,
    available_capacity=2000
)
def validate_action(action, constraints):
    """
    Validate a business action against all hard business constraints.

    Returns:
        list[str]: Empty list if the action is valid.
                   Otherwise, a list of constraint violations.
    """

    violations = []
 # Invalid input check
    if action is None:
        return ["Invalid input: action cannot be None"]
    required_attributes = [
        "cost",
        "expected_delay",
        "capacity",
        "risk"
    ]

    for attribute in required_attributes:
        if not hasattr(action, attribute):
            violations.append(
                f"Invalid input: missing attribute '{attribute}'"
            )

    if violations:
        return violations
# Budget constraint
    if action.cost > constraints.maximum_budget:
        violations.append(
            f"Cost ${action.cost:,.2f} exceeds "
            f"budget ${constraints.maximum_budget:,.2f}"
        )
#Delay constarints
    if action.expected_delay > constraints.maximum_delay:
        violations.append(
            f"Expected delay {action.expected_delay} days exceeds "
            f"maximum allowed delay {constraints.maximum_delay} days"
        )
#Capacity Constarint
    if action.capacity > constraints.available_capacity:
        violations.append(
            f"Capacity {action.capacity:,} exceeds "
            f"available capacity {constraints.available_capacity:,} units"
        )
    return violations


def is_feasible(action, constraints):
    """
    Return True only when an action satisfies
    every hard business constraint.
    """

    return len(validate_action(action, constraints)) == 0


def print_constraints():
    print("\nBUSINESS CONSTRAINTS")
    print(
        f"Maximum Budget     : "
        f"${constraints.maximum_budget:,.2f}"
    )
    print(
        f"Maximum Delay      : "
        f"{constraints.maximum_delay} days"
    )
    print(
        f"Available Capacity : "
        f"{constraints.available_capacity:,} units"
    )
if __name__ == "__main__":

    from .actions import get_actions
    print_constraints()
    print("\nACTION VALIDATION")
    for action in get_actions():

        violations = validate_action(
            action,
            constraints
        )

        print(f"\n{action.name}")

        if not violations:
            print("Action satisfies all constraints.")

        else:
            print("Constraint violations:")

            for violation in violations:
                print(f" - {violation}")