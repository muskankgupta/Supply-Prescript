import pytest

from optimization.actions import get_actions
from optimization.constraints import (
    BusinessConstraints,
    constraints,
    validate_action,
    is_feasible,
)
from optimization.optimizer import optimize_actions


# =========================================================
# 1. BUDGET VIOLATION TEST
# =========================================================

def test_budget_violation_is_rejected():
    """
    An action costing more than the maximum budget
    must be rejected.
    """

    test_constraints = BusinessConstraints(
        maximum_budget=10000,
        maximum_delay=5,
        available_capacity=2000,
    )

    air_freight = get_actions()[0]

    violations = validate_action(
        air_freight,
        test_constraints,
    )

    assert len(violations) > 0


# =========================================================
# 2. VALID BUDGET TEST
# =========================================================

def test_valid_budget_action_is_accepted():
    """
    An action within the allowed budget
    should be considered valid.
    """

    test_constraints = BusinessConstraints(
        maximum_budget=20000,
        maximum_delay=5,
        available_capacity=2000,
    )

    air_freight = get_actions()[0]

    violations = validate_action(
        air_freight,
        test_constraints,
    )

    assert len(violations) == 0


# =========================================================
# 3. CAPACITY CONSTRAINT TEST
# =========================================================

def test_capacity_violation_is_detected():
    """
    An action requiring more capacity than available
    must be rejected.
    """

    action = get_actions()[0]

    test_constraints = BusinessConstraints(
        maximum_budget=20000,
        maximum_delay=5,
        available_capacity=500,
    )

    violations = validate_action(
        action,
        test_constraints,
    )

    assert any(
        "Capacity" in violation
        for violation in violations
    )


# =========================================================
# 4. DELAY CONSTRAINT TEST
# =========================================================

def test_delay_violation_is_detected():
    """
    An action exceeding the maximum allowed delay
    must be rejected.
    """

    action = get_actions()[0]

    test_constraints = BusinessConstraints(
        maximum_budget=20000,
        maximum_delay=0.5,
        available_capacity=2000,
    )

    violations = validate_action(
        action,
        test_constraints,
    )

    assert any(
        "delay" in violation.lower()
        for violation in violations
    )


# =========================================================
# 5. INVALID INPUT TEST
# =========================================================

def test_invalid_input_is_rejected():
    """
    None or invalid action input must be rejected.
    """

    violations = validate_action(
        None,
        constraints,
    )

    assert any(
        "Invalid input" in violation
        for violation in violations
    )


# =========================================================
# 6. OPTIMIZER FEASIBILITY TEST
# =========================================================

def test_optimizer_returns_only_feasible_actions():
    """
    Critical optimization audit.

    The optimizer must NEVER return an action
    that violates hard business constraints.
    """

    recommended_actions = optimize_actions()

    for action in recommended_actions:

        assert is_feasible(
            action,
            constraints,
        ), (
            f"Optimizer returned an infeasible action: "
            f"{action}"
        )


# =========================================================
# 7. REDUCED BUDGET TEST
# =========================================================

def test_optimizer_respects_reduced_budget():
    """
    When the budget is reduced to $10,000,
    the optimizer must not recommend an action
    costing more than $10,000.
    """

    strict_constraints = BusinessConstraints(
        maximum_budget=10000,
        maximum_delay=5,
        available_capacity=2000,
    )

    recommended_actions = optimize_actions(
        constraints=strict_constraints
    )

    for action in recommended_actions:

        assert action.cost <= 10000, (
            f"Optimizer recommended an action "
            f"above the strict budget: {action.cost}"
        )