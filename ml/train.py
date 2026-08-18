import json
import os
from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)
from xgboost import XGBClassifier

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TRAIN_PATH = PROJECT_ROOT / "data" / "train.csv"
TEST_PATH = PROJECT_ROOT / "data" / "test.csv"

MODEL_DIR = PROJECT_ROOT / "models"

MODEL_PATH = MODEL_DIR / "delay_model.pkl"
METRICS_PATH = MODEL_DIR / "model_metrics.json"


if not TRAIN_PATH.exists():
    raise FileNotFoundError(
        f"Training dataset not found:\n{TRAIN_PATH}\n"
        "Run your Day 3 splitting script first."
    )

if not TEST_PATH.exists():
    raise FileNotFoundError(
        f"Testing dataset not found:\n{TEST_PATH}\n"
        "Run your Day 3 splitting script first."
    )
train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

print(f"Training data: {train_df.shape}")
print(f"Testing data : {test_df.shape}")


# Target:
# 0 = shipment is on time
# 1 = shipment is delayed

train_df["is_delayed"] = (
    train_df["delay_days"] > 0
).astype(int)

test_df["is_delayed"] = (
    test_df["delay_days"] > 0
).astype(int)
feature_columns = [
    "supplier_id",
    "product",
    "origin",
    "destination",
    "order_quantity",
    "inventory_level",
    "historical_lead_time",
    "supplier_reliability",
    "weather_risk",
    "transportation_mode",
    "previous_delays"
]

target_column = "is_delayed"


X_train = train_df[feature_columns]
y_train = train_df[target_column]

X_test = test_df[feature_columns]
y_test = test_df[target_column]


print("\nFeatures used for prediction:")

for feature in feature_columns:
    print(f" - {feature}")

categorical_features = [
    "supplier_id",
    "product",
    "origin",
    "destination",
    "transportation_mode"
]

numerical_features = [
    "order_quantity",
    "inventory_level",
    "historical_lead_time",
    "supplier_reliability",
    "weather_risk",
    "previous_delays"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)


print(
    f"Processed training shape: "
    f"{X_train_processed.shape}"
)

print(
    f"Processed testing shape: "
    f"{X_test_processed.shape}"
)

negative_count = (y_train == 0).sum()
positive_count = (y_train == 1).sum()

print("\nTraining target distribution:")
print(f"On-time shipments : {negative_count:,}")
print(f"Delayed shipments : {positive_count:,}")

if positive_count > 0:
    scale_pos_weight = negative_count / positive_count
else:
    scale_pos_weight = 1.0

print("\nBuilding XGBoost classifier...")

model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1,
    scale_pos_weight=scale_pos_weight
)


model.fit(
    X_train_processed,
    y_train
)

print("\nGenerating predictions...")

# Probability that shipment will be delayed
delay_probability = model.predict_proba(
    X_test_processed
)[:, 1]

# Classification
y_pred = (
    delay_probability >= 0.50
).astype(int)

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    delay_probability
)

print(f"\nAccuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "On Time",
            "Delayed"
        ],
        zero_division=0
    )
)


MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

model_bundle = {
    "model": model,
    "preprocessor": preprocessor,
    "features": feature_columns,
    "categorical_features": categorical_features,
    "numerical_features": numerical_features
}

joblib.dump(
    model_bundle,
    MODEL_PATH
)


metrics = {
    "model": "XGBoost Classifier",
    "target": "is_delayed",
    "target_definition": "1 if delay_days > 0 else 0",

    "training_rows": int(len(train_df)),
    "testing_rows": int(len(test_df)),

    "features": feature_columns,

    "accuracy": round(float(accuracy), 4),
    "precision": round(float(precision), 4),
    "recall": round(float(recall), 4),
    "f1_score": round(float(f1), 4),
    "roc_auc": round(float(roc_auc), 4),

    "confusion_matrix": cm.tolist()
}

with open(
    METRICS_PATH,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        metrics,
        file,
        indent=4
    )


prediction_output = test_df[
    [
        "shipment_id",
        "supplier_id",
        "product",
        "supplier_reliability",
        "weather_risk",
        "transportation_mode",
        "previous_delays",
        "delay_days"
    ]
].copy()

prediction_output["actual_delayed"] = y_test.values

prediction_output["delay_probability"] = (
    delay_probability
)

prediction_output["predicted_delayed"] = (
    y_pred
)

prediction_output["delay_probability"] = (
    prediction_output["delay_probability"]
    .round(4)
)

print("\nExample predictions:")

print(
    prediction_output.head(10).to_string(
        index=False
    )
)
