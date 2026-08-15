import pandas as pd
import numpy as np

#Reproduce random data
np.random.seed(42)
#number of records
n = 110000

products = [
    "Laptop",
    "Smartphone",
    "Microchip",
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
#Generating dataset
df= pd.DataFrame({
    "shipment_id": [
        f"SHP{str(i).zfill(6)}"
        for i in range(1, n+1)
    ],
    "supplier_id": np.random.choice(
        suppliers,
        n
    ),
    "product": np.random.choice(
        products,
        n
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
    "current_lead_time": np.random.randint(
        3,
        45,
        n
    ),
    "supplier_reliability": np.round(
        np.random.uniform(0.70, 1.00, n),
        2
    ),

    "weather_risk": np.round(
        np.random.uniform(0, 1, n),
        2
    ),

    "transportation_mode": np.random.choice(
        transportation_modes,
        n,
        p=[0.30, 0.35, 0.25, 0.10]
    ),

    "previous_delays": np.random.randint(
        0,
        8,
        n
    ),
})
#predicting dealys
base_delay = np.random.normal(2, 2, n)

weather_effect = df["weather_risk"] * 8

reliability_effect = (1 - df["supplier_reliability"]) * 15

previous_delay_effect = df["previous_delays"] * 1.2

transport_effect = df["transportation_mode"].map({
    "Air": 0.5,
    "Sea": 2.0,
    "Road": 1.0,
    "Rail": 1.5
})

df["delay_days"] = np.maximum(
    0,
    np.round(
        base_delay
        + weather_effect
        + reliability_effect
        + previous_delay_effect
        + transport_effect
    )
).astype(int)

#current lead times depends on delays
df["current_lead_time"] = (
    df["historical_lead_time"]
    + df["delay_days"]
    + np.random.randint(-2, 4, n)
)

# Ensure lead time is at least 1
df["current_lead_time"] = df["current_lead_time"].clip(lower=1)
df.to_csv(
    "supply_chain_dataset.csv",
    index=False
)

print("Shape:")
print(df.shape)

print("\nFirst 10 rows:")
print(df.head(10))

print("\nColumn information:")
print(df.info())

print("\nBasic statistics:")
print(df.describe())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate shipment IDs:")
print(df["shipment_id"].duplicated().sum())
