import pandas as pd
import numpy as np
import os
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "supply_chain_data.csv"
TRAIN_PATH = PROJECT_ROOT / "data" / "train.csv"
TEST_PATH = PROJECT_ROOT / "data" / "test.csv"
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        f"Dataset not found at: {DATA_PATH}\n"
        "Run dataset.py first."
    )

df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully.")
print(f"File: {DATA_PATH}")
print("1. DATASET OVERVIEW")
print(f"\nOriginal dataset:")
print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")

if "delay_days" not in df.columns:
    raise ValueError(
        "Target column 'delay_days' was not found."
    )
#randomize
df = df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)
#splitting
split_index = int(len(df) * 0.80)

train_df = df.iloc[:split_index].copy()
test_df = df.iloc[split_index:].copy()
train_df.to_csv(
    TRAIN_PATH,
    index=False
)

test_df.to_csv(
    TEST_PATH,
    index=False
)
print("\nDataset split completed.")

print("\nTraining dataset:")
print(f"Rows    : {len(train_df):,}")
print(f"Columns : {len(train_df.columns)}")

print("\nTesting dataset:")
print(f"Rows    : {len(test_df):,}")
print(f"Columns : {len(test_df.columns)}")
print("\nTarget distribution:")

print("\nTraining delay statistics:")
print(
    train_df["delay_days"]
    .describe()
    .round(2)
    .to_string()
)

print("\nTesting delay statistics:")
print(
    test_df["delay_days"]
    .describe()
    .round(2)
    .to_string()
)
#data lekeage checking

train_ids = set(train_df["shipment_id"])
test_ids = set(test_df["shipment_id"])

overlap = train_ids.intersection(test_ids)

print("\nShipment ID overlap:")
print(len(overlap))

if len(overlap) == 0:
    print("✓ No shipment IDs overlap.")
else:
    print("⚠ WARNING: Shipment IDs overlap.")
    print("\nFiles created:")

print(f"Training: {TRAIN_PATH}")
print(f"Testing : {TEST_PATH}")

print("\n" + "=" * 70)
print("DAY 3 SPLIT COMPLETED")
print("=" * 70)
print("\nColumns:")
for column in df.columns:
    print(f" - {column}")

print("2. FIRST 10 RECORDS")
print(df.head(10).to_string(index=False))
print("3. DATA TYPES")
print(df.dtypes)

print("4. MISSING VALUES")
missing_values = df.isnull().sum()

missing_table = pd.DataFrame({
    "column": missing_values.index,
    "missing_count": missing_values.values,
    "missing_percentage": (
        missing_values.values / len(df) * 100
    ).round(2)
})

print(missing_table.to_string(index=False))

if missing_values.sum() == 0:
    print("\n✓ No missing values found.")
else:
    print("\n⚠ Missing values detected.")

print("5. DUPLICATE SHIPMENT IDs")
duplicate_shipments = df["shipment_id"].duplicated().sum()

print(f"Duplicate shipment IDs: {duplicate_shipments}")

if duplicate_shipments == 0:
    print("✓ Shipment IDs are unique.")
else:
    print("⚠ Duplicate shipment IDs found.")

print("6. NUMERICAL SUMMARY")
numeric_columns = df.select_dtypes(
    include=np.number
).columns

print(
    df[numeric_columns]
    .describe()
    .round(2)
    .to_string()
)
print("7. CATEGORICAL VARIABLES")
categorical_columns = [
    "supplier_id",
    "product",
    "origin",
    "destination",
    "transportation_mode"
]

for column in categorical_columns:

    print(f"\n{column}:")
    print(f"Unique values: {df[column].nunique()}")

    print(
        df[column]
        .value_counts()
        .head(10)
        .to_string()
    )

print("8. TARGET VARIABLE - DELAY DAYS")
print("\nTarget statistics:")

print(
    df["delay_days"]
    .describe()
    .round(2)
    .to_string()
)

print("\nDelay distribution:")

delay_distribution = (
    df["delay_days"]
    .value_counts()
    .sort_index()
)

print(delay_distribution.to_string())

print("9. DELAYED VS ON-TIME SHIPMENTS")
df["is_delayed"] = (
    df["delay_days"] > 0
).astype(int)

shipment_status = (
    df["is_delayed"]
    .value_counts()
    .rename(index={
        0: "On Time",
        1: "Delayed"
    })
)

shipment_percentage = (
    df["is_delayed"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
    .rename(index={
        0: "On Time",
        1: "Delayed"
    })
)

print("\nShipment count:")
print(shipment_status.to_string())

print("\nShipment percentage:")
print(shipment_percentage.to_string())

print("10. AVERAGE DELAY BY TRANSPORTATION MODE")
transport_delay = (
    df.groupby("transportation_mode")["delay_days"]
    .agg(
        shipment_count="count",
        delayed_shipments=lambda x: (x > 0).sum(),
        average_delay="mean",
        maximum_delay="max"
    )
    .sort_values(
        "average_delay",
        ascending=False
    )
)

transport_delay["delay_rate_%"] = (
    transport_delay["delayed_shipments"]
    / transport_delay["shipment_count"]
    * 100
).round(2)

transport_delay["average_delay"] = (
    transport_delay["average_delay"]
    .round(2)
)

print(
    transport_delay.to_string()
)

print("11. SUPPLIER PERFORMANCE")
supplier_performance = (
    df.groupby("supplier_id")
    .agg(
        shipments=("shipment_id", "count"),
        average_delay=("delay_days", "mean"),
        average_reliability=(
            "supplier_reliability",
            "mean"
        ),
        delayed_shipments=(
            "is_delayed",
            "sum"
        )
    )
)

supplier_performance["delay_rate_%"] = (
    supplier_performance["delayed_shipments"]
    / supplier_performance["shipments"]
    * 100
).round(2)

supplier_performance["average_delay"] = (
    supplier_performance["average_delay"]
    .round(2)
)

supplier_performance["average_reliability"] = (
    supplier_performance["average_reliability"]
    .round(3)
)

print(
    supplier_performance
    .sort_values(
        "average_delay",
        ascending=False
    )
    .to_string()
)

print("12. SUPPLIER RELIABILITY VS DELAY")
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
    ],
    include_lowest=True
)

reliability_analysis = (
    df.groupby(
        reliability_group,
        observed=True
    )["delay_days"]
    .agg(
        shipment_count="count",
        average_delay="mean"
    )
)

reliability_analysis["average_delay"] = (
    reliability_analysis["average_delay"]
    .round(2)
)

print(
    reliability_analysis.to_string()
)

print("13. WEATHER RISK VS DELAY")
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
    ],
    include_lowest=True
)

weather_analysis = (
    df.groupby(
        weather_group,
        observed=True
    )["delay_days"]
    .agg(
        shipment_count="count",
        average_delay="mean"
    )
)

weather_analysis["average_delay"] = (
    weather_analysis["average_delay"]
    .round(2)
)

print(
    weather_analysis.to_string()
)

print("14. PREVIOUS DELAYS VS CURRENT DELAY")
previous_delay_analysis = (
    df.groupby("previous_delays")["delay_days"]
    .agg(
        shipment_count="count",
        average_current_delay="mean"
    )
)

previous_delay_analysis[
    "average_current_delay"
] = (
    previous_delay_analysis[
        "average_current_delay"
    ].round(2)
)

print(
    previous_delay_analysis.to_string()
)

print("15. PRODUCT DELAY ANALYSIS")
product_analysis = (
    df.groupby("product")
    .agg(
        shipments=("shipment_id", "count"),
        average_delay=("delay_days", "mean"),
        average_lead_time=(
            "current_lead_time",
            "mean"
        )
    )
    .sort_values(
        "average_delay",
        ascending=False
    )
)

product_analysis["average_delay"] = (
    product_analysis["average_delay"]
    .round(2)
)

product_analysis["average_lead_time"] = (
    product_analysis["average_lead_time"]
    .round(2)
)

print(
    product_analysis.to_string()
)

print("16. LEAD TIME ANALYSIS")
df["lead_time_increase"] = (
    df["current_lead_time"]
    - df["historical_lead_time"]
)

lead_time_summary = df[
    [
        "historical_lead_time",
        "current_lead_time",
        "lead_time_increase"
    ]
].describe().round(2)

print(
    lead_time_summary.to_string()
)

print("17. CORRELATION WITH DELAY DAYS")
correlation_columns = [
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
    df[correlation_columns]
    .corr()["delay_days"]
    .drop("delay_days")
    .sort_values(
        ascending=False
    )
    .round(3)
)

print(
    correlations.to_string()
)

print("18. HIGH-RISK SHIPMENTS")
high_risk = df[
    (
        (df["weather_risk"] >= 0.70)
        |
        (df["supplier_reliability"] <= 0.80)
        |
        (df["previous_delays"] >= 3)
    )
]

print(
    f"High-risk shipments: {len(high_risk):,}"
)

print("\nPercentage of dataset:")
print(
    round(
        len(high_risk) / len(df) * 100,
        2
    ),
    "%"
)
os.makedirs(
    "eda_results",
    exist_ok=True
)

transport_delay.to_csv(
    "eda_results/transportation_analysis.csv"
)

supplier_performance.to_csv(
    "eda_results/supplier_analysis.csv"
)

reliability_analysis.to_csv(
    "eda_results/reliability_analysis.csv"
)

weather_analysis.to_csv(
    "eda_results/weather_analysis.csv"
)

product_analysis.to_csv(
    "eda_results/product_analysis.csv"
)

correlations.to_csv(
    "eda_results/correlation_analysis.csv"
)
print("19. FINAL DATA QUALITY CHECK")
print(
    f"Rows: {len(df):,}"
)

print(
    f"Columns: {len(df.columns)}"
)

print(
    f"Missing values: {df.isnull().sum().sum()}"
)

print(
    f"Duplicate shipment IDs: "
    f"{df['shipment_id'].duplicated().sum()}"
)

print(
    f"Minimum delay: "
    f"{df['delay_days'].min()}"
)

print(
    f"Maximum delay: "
    f"{df['delay_days'].max()}"
)

print(
    f"Average delay: "
    f"{df['delay_days'].mean():.2f}"
)

print(
    f"Delayed shipment rate: "
    f"{df['is_delayed'].mean() * 100:.2f}%"
)
