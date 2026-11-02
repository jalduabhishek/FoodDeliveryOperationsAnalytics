SELECT
            Order_Status,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY Order_Status;
