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
