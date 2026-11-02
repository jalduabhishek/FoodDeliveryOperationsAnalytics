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
