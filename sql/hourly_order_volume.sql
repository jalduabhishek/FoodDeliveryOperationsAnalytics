SELECT
            Order_Hour,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY Order_Hour
        ORDER BY Order_Hour;
