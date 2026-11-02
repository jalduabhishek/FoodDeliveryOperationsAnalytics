
import sqlite3
import pandas as pd
from pathlib import Path

# Project paths
root = Path(__file__).resolve().parent.parent
csv_path = root / "data" / "food_delivery_orders.csv"
db_path = root / "data" / "food_delivery.db"
sql_dir = root / "sql"
sql_dir.mkdir(exist_ok=True)

# Load CSV
df = pd.read_csv(csv_path)

# Create SQLite database
conn = sqlite3.connect(db_path)

# Save orders into database
df.to_sql(
    "orders",
    conn,
    if_exists="replace",
    index=False
)

print("SQLite database created successfully!")

# SQL queries
queries = {
    "Total Orders": """
        SELECT COUNT(*) AS total_orders
        FROM orders;
    """,

    "Order Status": """
        SELECT
            Order_Status,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY Order_Status;
    """,

    "City Performance": """
        SELECT
            City,
            COUNT(*) AS total_orders,
            ROUND(AVG(
                CASE WHEN Order_Status = 'Delivered'
                THEN Delivery_Time_Min END
            ), 2) AS avg_delivery_minutes,
            ROUND(
                100.0 * SUM(
                    CASE WHEN Order_Status = 'Cancelled'
                    THEN 1 ELSE 0 END
                ) / COUNT(*), 2
            ) AS cancellation_rate_pct
        FROM orders
        GROUP BY City
        ORDER BY total_orders DESC;
    """,

    "Traffic Impact": """
        SELECT
            Traffic_Level,
            COUNT(*) AS delivered_orders,
            ROUND(AVG(Delivery_Time_Min), 2)
                AS avg_delivery_minutes,
            ROUND(
                100.0 * SUM(
                    CASE WHEN Is_Delayed = 1
                    THEN 1 ELSE 0 END
                ) / COUNT(*), 2
            ) AS delay_rate_pct
        FROM orders
        WHERE Order_Status = 'Delivered'
        GROUP BY Traffic_Level
        ORDER BY avg_delivery_minutes DESC;
    """,

    "Peak Hour Performance": """
        SELECT
            CASE
                WHEN Peak_Hour = 1 THEN 'Peak'
                ELSE 'Non-Peak'
            END AS period,
            COUNT(*) AS delivered_orders,
            ROUND(AVG(Delivery_Time_Min), 2)
                AS avg_delivery_minutes
        FROM orders
        WHERE Order_Status = 'Delivered'
        GROUP BY Peak_Hour
        ORDER BY Peak_Hour;
    """,

    "Hourly Order Volume": """
        SELECT
            Order_Hour,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY Order_Hour
        ORDER BY Order_Hour;
    """
}

# Run queries and save SQL files
for name, query in queries.items():
    print(f"\n========== {name.upper()} ==========")

    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))

    filename = name.lower().replace(" ", "_") + ".sql"
    (sql_dir / filename).write_text(
        query.strip() + "\n",
        encoding="utf-8"
    )

conn.close()

print("\nSQL analysis completed successfully!")
print("Database saved to:", db_path)
print("SQL queries saved to:", sql_dir)
