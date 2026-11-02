
import pandas as pd
import numpy as np
from pathlib import Path

# Make results reproducible
rng = np.random.default_rng(42)

# Number of food delivery orders
n = 5000

# Generate order dates and hours
dates = pd.date_range("2026-01-01", periods=90, freq="D")
order_dates = rng.choice(dates, size=n)
order_hours = rng.integers(8, 24, size=n)

# Generate delivery characteristics
distance = rng.uniform(1, 15, size=n).round(2)
peak_hour = np.isin(order_hours, [12, 13, 19, 20, 21])
traffic = rng.choice(
    ["Low", "Medium", "High"],
    size=n,
    p=[0.3, 0.45, 0.25]
)

traffic_delay = np.select(
    [traffic == "Low", traffic == "Medium", traffic == "High"],
    [0, 7, 15]
)

delivery_time = (
    12 + distance * 3
    + peak_hour * 8
    + traffic_delay
    + rng.normal(0, 5, n)
).clip(min=10).round(1)

# Generate order status
status = rng.choice(
    ["Delivered", "Cancelled"],
    size=n,
    p=[0.93, 0.07]
)

# Build dataset
df = pd.DataFrame({
    "Order_ID": range(10001, 10001 + n),
    "Order_Date": order_dates,
    "Order_Hour": order_hours,
    "City": rng.choice(
        ["Delhi", "Mumbai", "Bangalore", "Hyderabad"],
        size=n
    ),
    "Distance_km": distance,
    "Traffic_Level": traffic,
    "Peak_Hour": peak_hour,
    "Order_Value_INR": rng.integers(150, 1200, size=n),
    "Order_Status": status,
    "Delivery_Time_Min": np.where(
        status == "Delivered", delivery_time, np.nan
    )
})

# Define a late delivery as taking over 45 minutes
df["Is_Delayed"] = (
    (df["Delivery_Time_Min"] > 45)
    & (df["Order_Status"] == "Delivered")
)

# Save CSV
project_root = Path(__file__).resolve().parent.parent
output_path = project_root / "data" / "food_delivery_orders.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print("Dataset generated successfully!")
print("Total orders:", len(df))
print("Saved to:", output_path)
print(df.head())
