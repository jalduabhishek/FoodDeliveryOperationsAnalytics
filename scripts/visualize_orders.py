
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
root = Path(__file__).resolve().parent.parent
data_path = root / "data" / "food_delivery_orders.csv"
output_dir = root / "reports"
output_dir.mkdir(exist_ok=True)

# Load data
df = pd.read_csv(data_path)
delivered = df[df["Order_Status"] == "Delivered"].copy()

# Chart 1: Orders by city
city_orders = df["City"].value_counts()

plt.figure(figsize=(9, 5))
city_orders.plot(kind="bar", color="steelblue")
plt.title("Total Food Delivery Orders by City")
plt.xlabel("City")
plt.ylabel("Number of Orders")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_dir / "city_orders.png", dpi=200)
plt.close()

# Chart 2: Traffic impact
traffic_avg = delivered.groupby(
    "Traffic_Level"
)["Delivery_Time_Min"].mean()

traffic_avg = traffic_avg.reindex(["Low", "Medium", "High"])

plt.figure(figsize=(9, 5))
traffic_avg.plot(
    kind="bar",
    color=["green", "orange", "red"]
)
plt.title("Impact of Traffic on Delivery Time")
plt.xlabel("Traffic Level")
plt.ylabel("Average Delivery Time (minutes)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_dir / "traffic_impact.png", dpi=200)
plt.close()

# Chart 3: Peak vs non-peak
peak_avg = delivered.groupby(
    "Peak_Hour"
)["Delivery_Time_Min"].mean()

plt.figure(figsize=(8, 5))
plt.bar(
    ["Non-Peak", "Peak"],
    [peak_avg[False], peak_avg[True]],
    color=["skyblue", "coral"]
)
plt.title("Peak vs Non-Peak Delivery Time")
plt.ylabel("Average Delivery Time (minutes)")
plt.tight_layout()
plt.savefig(output_dir / "peak_hour_analysis.png", dpi=200)
plt.close()

# Chart 4: Order status
status_counts = df["Order_Status"].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(
    status_counts,
    labels=status_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Delivered vs Cancelled Orders")
plt.tight_layout()
plt.savefig(output_dir / "order_status.png", dpi=200)
plt.close()

print("All four charts generated successfully!")
print("Charts saved in:", output_dir)
