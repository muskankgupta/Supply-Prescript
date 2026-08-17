import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "supply_chain_data.csv"
RESULTS_DIR = PROJECT_ROOT / "eda" / "eda_results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"\nDataset not found at:\n{DATA_PATH}\n\n"
        "Make sure supply_chain_data.csv exists inside the data folder."
    )

df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully.")
print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")
outlier_columns = [
    "order_quantity",
    "inventory_level",
    "historical_lead_time",
    "current_lead_time",
    "delay_days"
]

outlier_results = []

for column in outlier_columns:

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ]

    outlier_results.append({
        "column": column,
        "Q1": Q1,
        "Q3": Q3,
        "IQR": IQR,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "outlier_count": len(outliers),
        "outlier_percentage": round(
            len(outliers) / len(df) * 100,
            2
        )
    })

outlier_analysis = pd.DataFrame(outlier_results)

print(
    outlier_analysis.to_string(index=False)
)

outlier_analysis.to_csv(
    "eda_results/outlier_analysis.csv",
    index=False
)