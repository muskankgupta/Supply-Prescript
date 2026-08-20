from dataclasses import dataclass
from typing import List


@dataclass
class BusinessAction:
    name: str
    description: str
    cost: float
    expected_delay: float
    capacity: int
    risk: float

air_freight = BusinessAction(
    name="Air Freight",
    description="Move the shipment using air transportation.",
    cost=15000,
    expected_delay=1.0,
    capacity=1000,
    risk=0.10
)

secondary_supplier = BusinessAction(
    name="Secondary Supplier",
    description="Use an alternative supplier to reduce supply risk.",
    cost=10000,
    expected_delay=2.0,
    capacity=2000,
    risk=0.20
)

delay_product_launch = BusinessAction(
    name="Delay Product Launch",
    description="Delay the product launch to avoid immediate shipment pressure.",
    cost=5000,
    expected_delay=5.0,
    capacity=2000,
    risk=0.30
)


actions: List[BusinessAction] = [
    air_freight,
    secondary_supplier,
    delay_product_launch
]


def get_actions() -> List[BusinessAction]:
    return actions


def print_actions():
    print("\nAVAILABLE BUSINESS ACTIONS")
    for index, action in enumerate(actions, start=1):

        print(f"\nAction {index}: {action.name}")
        print(f"Description     : {action.description}")
        print(f"Cost            : ${action.cost:,.2f}")
        print(f"Expected Delay  : {action.expected_delay} days")
        print(f"Capacity        : {action.capacity:,} units")
        print(f"Risk            : {action.risk:.2f}")


if __name__ == "__main__":
    print_actions()