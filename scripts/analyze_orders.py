
import pandas as pd
from pathlib import Path

# Locate project folder
project_root = Path(__file__).resolve().parent.parent

# Load dataset
file_path = project_root / "data" / "food_delivery_orders.csv"
df = pd.read_csv(file_path)

print("\n========== FOOD DELIVERY OPERATIONS ANALYSIS ==========")

# 1. Total orders
total_orders = len(df)

# 2. Delivered orders
delivered = df[df["Order_Status"] == "Delivered"]
delivered_orders = len(delivered)

# 3. Cancelled orders
cancelled_orders = len(df[df["Order_Status"] == "Cancelled"])

# 4. Cancellation rate
cancellation_rate = (cancelled_orders / total_orders) * 100

# 5. Average delivery time
avg_delivery_time = delivered["Delivery_Time_Min"].mean()

# 6. Delayed deliveries
delayed_orders = delivered["Is_Delayed"].sum()
delay_rate = (delayed_orders / delivered_orders) * 100

# Print KPIs
print(f"Total Orders: {total_orders}")
print(f"Delivered Orders: {delivered_orders}")
print(f"Cancelled Orders: {cancelled_orders}")
print(f"Cancellation Rate: {cancellation_rate:.2f}%")
print(f"Average Delivery Time: {avg_delivery_time:.2f} minutes")
print(f"Delayed Deliveries: {delayed_orders}")
print(f"Delivery Delay Rate: {delay_rate:.2f}%")

# 7. Orders by city
print("\n========== CITY-WISE ORDERS ==========")
print(df.groupby("City").size().sort_values(ascending=False))

# 8. Orders by hour
print("\n========== ORDERS BY HOUR ==========")
print(df.groupby("Order_Hour").size())

# 9. Delivery time by traffic level
print("\n========== TRAFFIC IMPACT ==========")
print(delivered.groupby("Traffic_Level")["Delivery_Time_Min"].mean())

# 10. Peak vs non-peak delivery time
print("\n========== PEAK HOUR ANALYSIS ==========")
print(delivered.groupby("Peak_Hour")["Delivery_Time_Min"].mean())

print("\nAnalysis completed successfully!")
