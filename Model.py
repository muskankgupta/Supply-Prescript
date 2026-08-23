# ============================================================
# PROJECT 3 - SUPPLY PRESCRIPT
# PREDICTIVE MODEL USING CSV DATASET
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from lightgbm import (
    LGBMClassifier,
    LGBMRegressor,
    early_stopping
)


# ============================================================
# 1. LOAD CSV DATASET
# ============================================================

FILE_PATH = "supply_chain_dataset.csv"

df = pd.read_csv(FILE_PATH)

print("=" * 70)
print("SUPPLY PRESCRIPT - PREDICTIVE MODEL")
print("=" * 70)

print("\nOriginal Dataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# 2. BASIC DATA INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("DATA INFORMATION")
print("=" * 70)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())


# ============================================================
# 3. DATA CLEANING
# ============================================================

# Remove duplicate records
df = df.drop_duplicates()

# Remove completely empty rows
df = df.dropna(how="all")

# Remove unnecessary index column if present
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])


# ============================================================
# 4. HANDLE MISSING VALUES
# ============================================================

numeric_columns = df.select_dtypes(
    include=["int64", "float64"]
).columns

categorical_columns = df.select_dtypes(
    include=["object"]
).columns


# Numerical columns -> median
for col in numeric_columns:

    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(
            df[col].median()
        )


# Categorical columns -> mode
for col in categorical_columns:

    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(
            df[col].mode()[0]
        )


# ============================================================
# 5. REMOVE INVALID VALUES
# ============================================================

if "historical_lead_time" in df.columns:

    df = df[
        df["historical_lead_time"] >= 0
    ]


if "current_lead_time" in df.columns:

    df = df[
        df["current_lead_time"] >= 0
    ]


if "delay_days" in df.columns:

    df = df[
        df["delay_days"] >= 0
    ]


if "order_quantity" in df.columns:

    df = df[
        df["order_quantity"] > 0
    ]


if "inventory_level" in df.columns:

    df = df[
        df["inventory_level"] >= 0
    ]


if "supplier_reliability" in df.columns:

    df = df[
        (df["supplier_reliability"] >= 0)
        &
        (df["supplier_reliability"] <= 1)
    ]


if "weather_risk" in df.columns:

    df = df[
        (df["weather_risk"] >= 0)
        &
        (df["weather_risk"] <= 1)
    ]


print("\nShape After Cleaning:")
print(df.shape)
