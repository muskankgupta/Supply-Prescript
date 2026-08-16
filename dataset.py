import pandas as pd
import numpy as np
import os
# Reproducibility
np.random.seed(42)
# Number of records
n = 110000
products = [
    "Microchip",
    "Laptop",
    "Smartphone",
    "Tablet",
    "Monitor",
    "Keyboard",
    "Mouse",
    "Headphones",
    "Printer",
    "Router",
    "SSD"
]
suppliers = [
    "SUP001",
    "SUP002",
    "SUP003",
    "SUP004",
    "SUP005",
    "SUP006",
    "SUP007",
    "SUP008",
    "SUP009",
    "SUP010"
]
origins = [
    "China",
    "India",
    "Vietnam",
    "Japan",
    "South Korea",
    "Taiwan",
    "USA",
    "Germany"
]
destinations = [
    "India",
    "USA",
    "UK",
    "Germany",
    "France",
    "Canada",
    "Australia",
    "Singapore"
]
transportation_modes = [
    "Air",
    "Sea",
    "Road",
    "Rail"
]
#generate shipment data
df = pd.DataFrame({
    "shipment_id": [
        f"SHP{str(i).zfill(6)}"
        for i in range(1, n + 1)
    ],
    "supplier_id": np.random.choice(
        suppliers,
        n
    ),
    "product": np.random.choice(
        products,
        n,
        p=[
            0.25,   # Microchip
            0.10,   # Laptop
            0.10,   # Smartphone
            0.08,   # Tablet
            0.08,   # Monitor
            0.07,   # Keyboard
            0.07,   # Mouse
            0.06,   # Headphones
            0.05,   # Printer
            0.07,   # Router
            0.07    # SSD
        ]
    ),
    "origin": np.random.choice(
        origins,
        n
    ),
    "destination": np.random.choice(
        destinations,
        n
    ),
    "order_quantity": np.random.randint(
        50,
        5000,
        n
    ),
    "inventory_level": np.random.randint(
        100,
        10000,
        n
    ),
    "historical_lead_time": np.random.randint(
        3,
        31,
        n
    ),
    "supplier_reliability": np.round(
        np.random.uniform(
            0.70,
            1.00,
            n
        ),
        2
    ),
    "weather_risk": np.round(
        np.random.uniform(
            0.00,
            1.00,
            n
        ),
        2
    ),
    "transportation_mode": np.random.choice(
        transportation_modes,
        n,
        p=[
            0.30,   # Air
            0.35,   # Sea
            0.25,   # Road
            0.10    # Rail
        ]
    ),
    "previous_delays": np.random.randint(
        0,
        5,
        n
    )
})
# TRANSPORTATION EFFECT
# Sea generally takes longer than Air.
transport_lead_time = df["transportation_mode"].map({
    "Air": 1,
    "Sea": 7,
    "Road": 3,
    "Rail": 4
})
# DELAY PROBABILITY
# Base probability that a shipment experiences a delay
base_probability = 0.20
# High weather risk -> higher delay probability
weather_effect = (
    df["weather_risk"] * 0.35
)
# Low supplier reliability -> higher delay probability
reliability_effect = (
    (1 - df["supplier_reliability"]) * 0.60
)
# Previous delays -> higher chance of another delay
previous_delay_effect = (
    df["previous_delays"] * 0.05
)
# Transportation effect
transport_delay_effect = df["transportation_mode"].map({
    "Air": 0.00,
    "Sea": 0.10,
    "Road": 0.04,
    "Rail": 0.03
})
# Final probability
delay_probability = (
    base_probability
    + weather_effect
    + reliability_effect
    + previous_delay_effect
    + transport_delay_effect
)
# Keep probability in a realistic range
delay_probability = delay_probability.clip(
    lower=0.05,
    upper=0.90
)
# GENERATE DELAY DAYS
# Decide which shipments are delayed
is_delayed = (
    np.random.random(n)
    < delay_probability
)
# Start with zero delay
delay_days = np.zeros(
    n,
    dtype=int
)
# Generate delay days only for delayed shipments
delayed_count = is_delayed.sum()
delay_days[is_delayed] = (
    np.random.poisson(
        lam=3,
        size=delayed_count
    ) + 1
)
# Weather can add additional delay days
weather_delay_bonus = np.where(
    is_delayed,
    np.round(
        df["weather_risk"] * 2
    ),
    0
).astype(int)
# Previous delays can also add additional delay
previous_delay_bonus = np.where(
    is_delayed,
    np.floor(
        df["previous_delays"] * 0.5
    ),
    0
).astype(int)
# Final delay days
df["delay_days"] = (
    delay_days
    + weather_delay_bonus
    + previous_delay_bonus
)
# Make sure delay is never negative
df["delay_days"] = (
    df["delay_days"]
    .clip(lower=0)
    .astype(int)
)
# CURRENT LEAD TIME
# Random variation
random_variation = np.random.randint(
    -2,
    3,
    n
)
# Current lead time depends on:
# 1. Historical lead time
# 2. Transportation mode
# 3. Actual delay
# 4. Small random variation
df["current_lead_time"] = (
    df["historical_lead_time"]
    + transport_lead_time
    + df["delay_days"]
    + random_variation
)
# Lead time must be at least 1 day
df["current_lead_time"] = (
    df["current_lead_time"]
    .clip(lower=1)
    .astype(int)
)
df = df[
    [
        "shipment_id",
        "supplier_id",
        "product",
        "origin",
        "destination",
        "order_quantity",
        "inventory_level",
        "historical_lead_time",
        "current_lead_time",
        "supplier_reliability",
        "weather_risk",
        "transportation_mode",
        "previous_delays",
        "delay_days"
    ]
]
os.makedirs(
    "data",
    exist_ok=True
)
output_file = "data/supply_chain_data.csv"
df.to_csv(
    output_file,
    index=False
)
# Shape
print("\nShape:")
print(df.shape)
# Columns
print("\nColumns:")
for column in df.columns:
    print("-", column)
# First rows
print("\nFirst 10 rows:")
print(df.head(10))
# Data types
print("\nData types:")
print(df.dtypes)
# Missing values
print("\nMissing values:")
print(df.isnull().sum())
# Duplicate shipment IDs
print("\nDuplicate shipment IDs:")
print(
    df["shipment_id"].duplicated().sum()
)
# DELAY DISTRIBUTION
print("\nDelay distribution (%):")
delay_distribution = (
    df["delay_days"]
    .value_counts(normalize=True)
    .sort_index()
    .mul(100)
    .round(2)
)
print(delay_distribution.head(20))
# AVERAGE DELAY BY TRANSPORTATION MODE
print("\nAverage delay by transportation mode:")
transport_delay = (
    df.groupby(
        "transportation_mode",
        observed=True
    )["delay_days"]
    .mean()
    .round(2)
)
print(transport_delay)
# AVERAGE DELAY BY SUPPLIER RELIABILITY
print("\nAverage delay by supplier reliability:")
reliability_group = pd.cut(
    df["supplier_reliability"],
    bins=[
        0.69,
        0.80,
        0.90,
        1.00
    ],
    labels=[
        "Low Reliability",
        "Medium Reliability",
        "High Reliability"
    ]
)
reliability_delay = (
    df.groupby(
        reliability_group,
        observed=True
    )["delay_days"]
    .mean()
    .round(2)
)
print(reliability_delay)
# AVERAGE DELAY BY WEATHER RISK
print("\nAverage delay by weather risk:")
weather_group = pd.cut(
    df["weather_risk"],
    bins=[
        -0.01,
        0.33,
        0.66,
        1.00
    ],
    labels=[
        "Low Weather Risk",
        "Medium Weather Risk",
        "High Weather Risk"
    ]
)
weather_delay = (
    df.groupby(
        weather_group,
        observed=True
    )["delay_days"]
    .mean()
    .round(2)
)
print(weather_delay)
# AVERAGE DELAY BY PRODUCT
print("\nAverage delay by product:")
product_delay = (
    df.groupby(
        "product",
        observed=True
    )["delay_days"]
    .mean()
    .sort_values(
        ascending=False
    )
    .round(2)
)
print(product_delay)
# AVERAGE LEAD TIME BY TRANSPORTATION MODE
print("\nAverage current lead time by transportation mode:")
lead_time_by_transport = (
    df.groupby(
        "transportation_mode",
        observed=True
    )["current_lead_time"]
    .mean()
    .sort_values(
        ascending=False
    )
    .round(2)
)
print(lead_time_by_transport)
# CORRELATION WITH DELAY DAYS
print("\nCorrelation with delay_days:")
numeric_columns = [
    "order_quantity",
    "inventory_level",
    "historical_lead_time",
    "current_lead_time",
    "supplier_reliability",
    "weather_risk",
    "previous_delays",
    "delay_days"
]
correlations = (
    df[numeric_columns]
    .corr()["delay_days"]
    .sort_values(
        ascending=False
    )
    .round(3)
)
print(correlations)
print("\nBasic statistics:")
print(df.describe())
print("\nDataset saved to:")
print(output_file)
print("\nFile contains:")
print(f"{len(df):,} rows")
print(f"{len(df.columns)} columns")