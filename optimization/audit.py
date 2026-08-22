from dataclasses import replace
from .actions import get_actions
from .constraints import (
    BusinessConstraints,
    constraints,
    validate_action,
    is_feasible
)
from .optimizer import optimize_actions
def print_test_result(test_name, passed):
    """
    Print a formatted test result.
    """

    status = "PASS" if passed else "FAIL"

    print(
        f"{status:<8} | {test_name}"
    )
def test_budget_rejection():
    """
    Test that an action exceeding the budget is rejected.
    Example:
        Budget = $10,000
        Air Freight = $15,000
    Expected:
        REJECT
    """
    test_constraints = BusinessConstraints(
        maximum_budget=10000,
        maximum_delay=5,
        available_capacity=2000
    )
    air_freight = get_actions()[0]
    violations = validate_action(
        air_freight,
        test_constraints
    )
    return len(violations) > 0
def test_budget_acceptance():
    """
    Test that an action within the budget is valid.
    Example:
        Budget = $20,000
        Air Freight = $15,000

    Expected:
        VALID
    """
    test_constraints = BusinessConstraints(
        maximum_budget=20000,
        maximum_delay=5,
        available_capacity=2000
    )
    air_freight = get_actions()[0]
    violations = validate_action(
        air_freight,
        test_constraints
    )
    return len(violations) == 0
def test_capacity_constraint():
    """
    Test that capacity violations are detected.
    """
    action = get_actions()[0]
    test_constraints = BusinessConstraints(
        maximum_budget=20000,
        maximum_delay=5,
        available_capacity=500
    )
    violations = validate_action(
        action,
        test_constraints
    )
    return any(
        "Capacity" in violation
        for violation in violations
    )
def test_delay_constraint():
    """
    Test that delay violations are detected.
    """
    action = get_actions()[0]
    test_constraints = BusinessConstraints(
        maximum_budget=20000,
        maximum_delay=0.5,
        available_capacity=2000
    )
    violations = validate_action(
        action,
        test_constraints
    )
    return any(
        "delay" in violation.lower()
        for violation in violations
    )

def test_invalid_input():
    """
    Test that invalid input is rejected.
    """
    violations = validate_action(
        None,
        constraints
    )
    return any(
        "Invalid input" in violation
        for violation in violations
    )
def test_optimizer_only_returns_feasible_actions():
    """
    Critical Day 10 audit.

    Proves that the optimizer never recommends
    an action violating hard business constraints.
    """
    recommended_actions = optimize_actions()
    for action in recommended_actions:
        if not is_feasible(
            action,
            constraints
        ):
            return False
    return True
def test_optimizer_with_reduced_budget():
    """
    Test the optimizer with a stricter budget.

    This ensures that an expensive action is removed
    automatically by the optimizer.
    """
    strict_constraints = BusinessConstraints(
        maximum_budget=10000,
        maximum_delay=5,
        available_capacity=2000
    )
    recommended_actions = optimize_actions(
        constraints=strict_constraints
    )
    for action in recommended_actions:
        if action.cost > 10000:
            return False
    return True
def run_audit():
    print("\n")
    print("DAY 10 - OPTIMIZATION AUDIT")
    tests = [
        (
            "Budget violation is rejected",
            test_budget_rejection
        ),

        (
            "Valid budget action is accepted",
            test_budget_acceptance
        ),

        (
            "Capacity violation is detected",
            test_capacity_constraint
        ),

        (
            "Delay violation is detected",
            test_delay_constraint
        ),

        (
            "Invalid input is rejected",
            test_invalid_input
        ),

        (
            "Optimizer returns only feasible actions",
            test_optimizer_only_returns_feasible_actions
        ),

        (
            "Optimizer respects reduced budget",
            test_optimizer_with_reduced_budget
        )
    ]

    passed = 0
    failed = 0

    print()

    for test_name, test_function in tests:
        try:
            result = test_function()
            print_test_result(
                test_name,
                result
            )
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as error:
            print_test_result(
                test_name,
                False
            )
            print(
                f" Error: {error}"
            )
            failed += 1
    print()
    print("AUDIT SUMMARY")
    print(
        f"Tests Passed : {passed}"
    )
    print(
        f"Tests Failed : {failed}"
    )
    print(
        f"Total Tests  : {len(tests)}"
    )
    print()
    if failed == 0:
        print(
            "AUDIT RESULT: PASSED"
        )
        print(
            "The optimizer respects all hard business constraints."
        )
    else:
        print(
            "AUDIT RESULT: FAILED"
        )
        print(
            "One or more constraint checks failed."
        )
if __name__ == "__main__":
    run_audit()