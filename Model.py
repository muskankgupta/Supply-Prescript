import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    precision_score,
    recall_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from lightgbm import LGBMClassifier, LGBMRegressor, early_stopping


# ==========================================================
# 1. LOAD DATA
# ==========================================================

df = pd.read_csv("supply_chain_dataset.csv")

print("Original shape:", df.shape)
print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())


# ==========================================================
# 2. DATA CLEANING
# ==========================================================

# Remove duplicate records
df = df.drop_duplicates()

# Remove completely empty rows
df = df.dropna(how="all")

# Remove unnecessary index column if present
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])


# ----------------------------------------------------------
# Handle missing values
# ----------------------------------------------------------

numeric_columns = df.select_dtypes(
    include=["int64", "float64"]
).columns

categorical_columns = df.select_dtypes(
    include=["object"]
).columns

# Numerical columns -> median
for col in numeric_columns:
    df[col] = df[col].fillna(df[col].median())

# Categorical columns -> mode
for col in categorical_columns:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].mode()[0])


# ----------------------------------------------------------
# Remove invalid numerical values
# ----------------------------------------------------------

# Lead times should not be negative
if "historical_lead_time" in df.columns:
    df = df[df["historical_lead_time"] >= 0]

if "current_lead_time" in df.columns:
    df = df[df["current_lead_time"] >= 0]

# Delay cannot be negative
if "delay_days" in df.columns:
    df = df[df["delay_days"] >= 0]

# Order quantity should be positive
if "order_quantity" in df.columns:
    df = df[df["order_quantity"] > 0]

# Inventory cannot be negative
if "inventory_level" in df.columns:
    df = df[df["inventory_level"] >= 0]


# ----------------------------------------------------------
# Remove impossible reliability/risk values
# ----------------------------------------------------------

if "supplier_reliability" in df.columns:
    df = df[
        (df["supplier_reliability"] >= 0) &
        (df["supplier_reliability"] <= 1)
    ]

if "weather_risk" in df.columns:
    df = df[
        (df["weather_risk"] >= 0) &
        (df["weather_risk"] <= 1)
    ]


# ----------------------------------------------------------
# Outlier treatment using IQR
# ----------------------------------------------------------

def cap_outliers(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    data[column] = data[column].clip(
        lower=lower,
        upper=upper
    )

    return data


outlier_columns = [
    "order_quantity",
    "inventory_level",
    "historical_lead_time",
    "current_lead_time",
    "previous_delays",
    "delay_days"
]

for col in outlier_columns:
    if col in df.columns:
        df = cap_outliers(df, col)


print("\nShape after cleaning:", df.shape)

print("\nMissing values after cleaning:")
print(df.isnull().sum())
