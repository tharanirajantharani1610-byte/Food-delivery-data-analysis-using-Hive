-- ==============================================================================
-- STEP 9: 30 HiveQL Analytical Queries
-- Database: food_delivery_db
-- Table:    food_delivery_cleaned
-- ==============================================================================

USE food_delivery_db;

-- ------------------------------------------------------------------------------
-- QUERY 1: Total Orders
-- ------------------------------------------------------------------------------
SELECT COUNT(order_id) AS total_orders 
FROM food_delivery_cleaned;

-- ------------------------------------------------------------------------------
-- QUERY 2: Total Revenue (From Delivered Orders)
-- ------------------------------------------------------------------------------
SELECT ROUND(SUM(total_amount), 2) AS total_revenue 
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered';

-- ------------------------------------------------------------------------------
-- QUERY 3: Average Order Value (AOV)
-- ------------------------------------------------------------------------------
SELECT ROUND(AVG(total_amount), 2) AS average_order_value 
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered';

-- ------------------------------------------------------------------------------
-- QUERY 4: Total Unique Customers
-- ------------------------------------------------------------------------------
SELECT COUNT(DISTINCT customer_id) AS total_unique_customers 
FROM food_delivery_cleaned;

-- ------------------------------------------------------------------------------
-- QUERY 5: Total Unique Restaurants
-- ------------------------------------------------------------------------------
SELECT COUNT(DISTINCT restaurant_id) AS total_unique_restaurants 
FROM food_delivery_cleaned;

-- ------------------------------------------------------------------------------
-- QUERY 6: Most Popular Food Category (By Order Volume)
-- ------------------------------------------------------------------------------
SELECT food_category, COUNT(order_id) AS order_count 
FROM food_delivery_cleaned 
GROUP BY food_category 
ORDER BY order_count DESC 
LIMIT 1;

-- ------------------------------------------------------------------------------
-- QUERY 7: Most Ordered Food Item
-- ------------------------------------------------------------------------------
SELECT item_name, food_category, SUM(quantity) AS total_quantity_ordered 
FROM food_delivery_cleaned 
GROUP BY item_name, food_category 
ORDER BY total_quantity_ordered DESC 
LIMIT 1;

-- ------------------------------------------------------------------------------
-- QUERY 8: Top 10 Restaurants by Revenue
-- ------------------------------------------------------------------------------
SELECT 
    restaurant_name, 
    COUNT(order_id) AS orders_handled, 
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(customer_rating), 2) AS avg_rating
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered' 
GROUP BY restaurant_name 
ORDER BY total_revenue DESC 
LIMIT 10;

-- ------------------------------------------------------------------------------
-- QUERY 9: Top 10 Customers by Total Spend
-- ------------------------------------------------------------------------------
SELECT 
    customer_id, 
    customer_city,
    COUNT(order_id) AS total_orders, 
    ROUND(SUM(total_amount), 2) AS total_spent 
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered' 
GROUP BY customer_id, customer_city 
ORDER BY total_spent DESC 
LIMIT 10;

-- ------------------------------------------------------------------------------
-- QUERY 10: Revenue by City
-- ------------------------------------------------------------------------------
SELECT 
    customer_city, 
    COUNT(order_id) AS total_orders, 
    ROUND(SUM(total_amount), 2) AS city_revenue,
    ROUND(AVG(delivery_time_minutes), 1) AS avg_delivery_time
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered' 
GROUP BY customer_city 
ORDER BY city_revenue DESC;

-- ------------------------------------------------------------------------------
-- QUERY 11: Revenue by Food Category
-- ------------------------------------------------------------------------------
SELECT 
    food_category, 
    COUNT(order_id) AS total_orders, 
    ROUND(SUM(total_amount), 2) AS category_revenue,
    ROUND(AVG(price), 2) AS avg_item_price
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered' 
GROUP BY food_category 
ORDER BY category_revenue DESC;

-- ------------------------------------------------------------------------------
-- QUERY 12: Monthly Revenue Trend
-- ------------------------------------------------------------------------------
SELECT 
    SUBSTR(order_date, 1, 7) AS order_month, 
    COUNT(order_id) AS total_orders, 
    ROUND(SUM(total_amount), 2) AS monthly_revenue 
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered' 
GROUP BY SUBSTR(order_date, 1, 7) 
ORDER BY order_month ASC;

-- ------------------------------------------------------------------------------
-- QUERY 13: Daily Order Count (Sample Recent 15 Days)
-- ------------------------------------------------------------------------------
SELECT 
    order_date, 
    COUNT(order_id) AS daily_orders,
    ROUND(SUM(total_amount), 2) AS daily_revenue
FROM food_delivery_cleaned 
GROUP BY order_date 
ORDER BY order_date DESC 
LIMIT 15;

-- ------------------------------------------------------------------------------
-- QUERY 14: Orders by Payment Method
-- ------------------------------------------------------------------------------
SELECT 
    payment_method, 
    COUNT(order_id) AS transaction_count, 
    ROUND(SUM(total_amount), 2) AS total_transaction_value,
    ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM food_delivery_cleaned), 2) AS percentage_share
FROM food_delivery_cleaned 
GROUP BY payment_method 
ORDER BY transaction_count DESC;

-- ------------------------------------------------------------------------------
-- QUERY 15: Delivered Orders Count
-- ------------------------------------------------------------------------------
SELECT COUNT(*) AS total_delivered_orders 
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered';

-- ------------------------------------------------------------------------------
-- QUERY 16: Cancelled Orders Count
-- ------------------------------------------------------------------------------
SELECT COUNT(*) AS total_cancelled_orders 
FROM food_delivery_cleaned 
WHERE order_status = 'Cancelled';

-- ------------------------------------------------------------------------------
-- QUERY 17: Order Cancellation Rate (%)
-- ------------------------------------------------------------------------------
SELECT 
    ROUND(
        (SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 
        2
    ) AS cancellation_rate_percentage 
FROM food_delivery_cleaned;

-- ------------------------------------------------------------------------------
-- QUERY 18: Average Delivery Time (Minutes)
-- ------------------------------------------------------------------------------
SELECT ROUND(AVG(delivery_time_minutes), 2) AS avg_delivery_time_mins 
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered' AND delivery_time_minutes > 0;

-- ------------------------------------------------------------------------------
-- QUERY 19: Average Customer Rating
-- ------------------------------------------------------------------------------
SELECT ROUND(AVG(customer_rating), 2) AS overall_avg_rating 
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered' AND customer_rating > 0;

-- ------------------------------------------------------------------------------
-- QUERY 20: Peak Ordering Hour Analysis
-- ------------------------------------------------------------------------------
SELECT 
    CAST(SUBSTR(order_time, 1, 2) AS INT) AS order_hour, 
    COUNT(order_id) AS total_orders,
    ROUND(SUM(total_amount), 2) AS hourly_revenue
FROM food_delivery_cleaned 
GROUP BY CAST(SUBSTR(order_time, 1, 2) AS INT) 
ORDER BY total_orders DESC;

-- ------------------------------------------------------------------------------
-- QUERY 21: Best-Rated Restaurants (Min 30 Orders)
-- ------------------------------------------------------------------------------
SELECT 
    restaurant_name, 
    COUNT(order_id) AS total_orders,
    ROUND(AVG(customer_rating), 2) AS average_rating 
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered' AND customer_rating > 0 
GROUP BY restaurant_name 
HAVING COUNT(order_id) >= 30 
ORDER BY average_rating DESC, total_orders DESC 
LIMIT 10;

-- ------------------------------------------------------------------------------
-- QUERY 22: Highest Revenue City
-- ------------------------------------------------------------------------------
SELECT 
    customer_city, 
    ROUND(SUM(total_amount), 2) AS total_revenue 
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered' 
GROUP BY customer_city 
ORDER BY total_revenue DESC 
LIMIT 1;

-- ------------------------------------------------------------------------------
-- QUERY 23: Discount and Promotion Analysis
-- ------------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount > 0 AND discount <= 50 THEN 'Low Discount (<= 50)'
        WHEN discount > 50 AND discount <= 100 THEN 'Medium Discount (51-100)'
        ELSE 'High Discount (> 100)'
    END AS discount_tier,
    COUNT(order_id) AS order_count,
    ROUND(SUM(discount), 2) AS total_discount_given,
    ROUND(SUM(total_amount), 2) AS net_revenue
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered' 
GROUP BY 
    CASE 
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount > 0 AND discount <= 50 THEN 'Low Discount (<= 50)'
        WHEN discount > 50 AND discount <= 100 THEN 'Medium Discount (51-100)'
        ELSE 'High Discount (> 100)'
    END 
ORDER BY order_count DESC;

-- ------------------------------------------------------------------------------
-- QUERY 24: Delivery Performance by Delivery Time Bracket
-- ------------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN delivery_time_minutes <= 25 THEN 'Ultra Fast (<= 25m)'
        WHEN delivery_time_minutes <= 40 THEN 'On Time (26-40m)'
        WHEN delivery_time_minutes <= 55 THEN 'Moderate (41-55m)'
        ELSE 'Delayed (> 55m)'
    END AS delivery_speed_category,
    COUNT(order_id) AS order_count,
    ROUND(AVG(customer_rating), 2) AS avg_rating_achieved
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered' AND delivery_time_minutes > 0 
GROUP BY 
    CASE 
        WHEN delivery_time_minutes <= 25 THEN 'Ultra Fast (<= 25m)'
        WHEN delivery_time_minutes <= 40 THEN 'On Time (26-40m)'
        WHEN delivery_time_minutes <= 55 THEN 'Moderate (41-55m)'
        ELSE 'Delayed (> 55m)'
    END 
ORDER BY order_count DESC;

-- ------------------------------------------------------------------------------
-- QUERY 25: Customer Spending Analysis & Segmentation
-- ------------------------------------------------------------------------------
SELECT 
    spending_tier,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(total_spent), 2) AS avg_spend_per_customer
FROM (
    SELECT 
        customer_id, 
        SUM(total_amount) AS total_spent,
        CASE 
            WHEN SUM(total_amount) >= 3000 THEN 'Tier 1: VIP (>= 3000)'
            WHEN SUM(total_amount) >= 1500 THEN 'Tier 2: Regular (1500-2999)'
            ELSE 'Tier 3: Occasional (< 1500)'
        END AS spending_tier
    FROM food_delivery_cleaned 
    WHERE order_status = 'Delivered' 
    GROUP BY customer_id
) cust_summary 
GROUP BY spending_tier 
ORDER BY customer_count DESC;

-- ------------------------------------------------------------------------------
-- QUERY 26: Monthly Growth Rate Analysis (Window LAG Function)
-- ------------------------------------------------------------------------------
SELECT 
    m.order_month,
    m.monthly_rev,
    LAG(m.monthly_rev, 1) OVER (ORDER BY m.order_month) AS prev_month_rev,
    ROUND(
        ((m.monthly_rev - LAG(m.monthly_rev, 1) OVER (ORDER BY m.order_month)) * 100.0) / 
        LAG(m.monthly_rev, 1) OVER (ORDER BY m.order_month), 
        2
    ) AS mom_growth_rate_pct
FROM (
    SELECT 
        SUBSTR(order_date, 1, 7) AS order_month, 
        ROUND(SUM(total_amount), 2) AS monthly_rev 
    FROM food_delivery_cleaned 
    WHERE order_status = 'Delivered' 
    GROUP BY SUBSTR(order_date, 1, 7)
) m 
ORDER BY m.order_month;

-- ------------------------------------------------------------------------------
-- QUERY 27: Food Category Performance & Profitability
-- ------------------------------------------------------------------------------
SELECT 
    food_category, 
    COUNT(order_id) AS total_orders, 
    SUM(quantity) AS total_units_sold, 
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(customer_rating), 2) AS category_avg_rating
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered' 
GROUP BY food_category 
ORDER BY total_revenue DESC;

-- ------------------------------------------------------------------------------
-- QUERY 28: Restaurant Order Volume vs Revenue Matrix
-- ------------------------------------------------------------------------------
SELECT 
    restaurant_name, 
    COUNT(order_id) AS total_orders, 
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(SUM(total_amount) / COUNT(order_id), 2) AS avg_revenue_per_order
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered' 
GROUP BY restaurant_name 
ORDER BY total_orders DESC 
LIMIT 10;

-- ------------------------------------------------------------------------------
-- QUERY 29: Payment Method Performance & Preference
-- ------------------------------------------------------------------------------
SELECT 
    payment_method, 
    COUNT(order_id) AS total_transactions, 
    ROUND(AVG(total_amount), 2) AS avg_ticket_size, 
    ROUND(SUM(total_amount), 2) AS gross_payment_volume 
FROM food_delivery_cleaned 
WHERE order_status = 'Delivered' 
GROUP BY payment_method 
ORDER BY gross_payment_volume DESC;

-- ------------------------------------------------------------------------------
-- QUERY 30: Overall Enterprise Business Executive Summary
-- ------------------------------------------------------------------------------
SELECT 
    COUNT(order_id) AS total_orders,
    SUM(CASE WHEN order_status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(SUM(CASE WHEN order_status = 'Delivered' THEN total_amount ELSE 0 END), 2) AS total_revenue,
    ROUND(AVG(CASE WHEN order_status = 'Delivered' THEN total_amount ELSE NULL END), 2) AS average_order_value,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT restaurant_id) AS unique_restaurants,
    ROUND(AVG(CASE WHEN order_status = 'Delivered' AND customer_rating > 0 THEN customer_rating ELSE NULL END), 2) AS average_rating,
    ROUND(AVG(CASE WHEN order_status = 'Delivered' AND delivery_time_minutes > 0 THEN delivery_time_minutes ELSE NULL END), 1) AS avg_delivery_minutes
FROM food_delivery_cleaned;
