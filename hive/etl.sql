-- ==============================================================================
-- STEP 8: Hive ETL Process (Extract, Transform, Load)
-- Database: food_delivery_db
-- Source:   /opt/data/food_delivery.csv -> food_delivery_raw
-- Target:   food_delivery_cleaned
-- ==============================================================================

USE food_delivery_db;

-- ------------------------------------------------------------------------------
-- 1. EXTRACT: Ingest Raw CSV Data into Staging Table
-- ------------------------------------------------------------------------------
LOAD DATA LOCAL INPATH '/opt/data/food_delivery.csv' OVERWRITE INTO TABLE food_delivery_raw;

-- Record verification in staging
SELECT 'RAW_DATA_COUNT' AS metric, COUNT(*) AS val FROM food_delivery_raw;

-- ------------------------------------------------------------------------------
-- 2. TRANSFORM & LOAD:
-- - Deduplicate via ROW_NUMBER() window function on order_id
-- - Filter out NULL / blank order_id and customer_id
-- - Validate price > 0 and quantity > 0
-- - Validate delivery_time_minutes >= 0
-- - Standardize food categories and payment methods
-- - Calculate total_amount = (quantity * price + delivery_fee - discount)
-- - Populate clean analytics table in optimized ORC format
-- ------------------------------------------------------------------------------
INSERT OVERWRITE TABLE food_delivery_cleaned
SELECT
    dedup.order_id,
    dedup.customer_id,
    dedup.restaurant_id,
    dedup.restaurant_name,
    dedup.customer_city,
    dedup.order_date,
    dedup.order_time,
    -- Standardize food category casing
    CASE 
        WHEN LOWER(TRIM(dedup.food_category)) = 'pizza' THEN 'Pizza'
        WHEN LOWER(TRIM(dedup.food_category)) = 'burger' THEN 'Burger'
        WHEN LOWER(TRIM(dedup.food_category)) = 'biryani' THEN 'Biryani'
        WHEN LOWER(TRIM(dedup.food_category)) = 'indian' THEN 'Indian'
        WHEN LOWER(TRIM(dedup.food_category)) = 'chinese' THEN 'Chinese'
        WHEN LOWER(TRIM(dedup.food_category)) = 'fast food' THEN 'Fast Food'
        WHEN LOWER(TRIM(dedup.food_category)) = 'desserts' THEN 'Desserts'
        WHEN LOWER(TRIM(dedup.food_category)) = 'beverages' THEN 'Beverages'
        ELSE INITCAP(TRIM(dedup.food_category))
    END AS food_category,
    dedup.item_name,
    dedup.quantity,
    dedup.price,
    COALESCE(dedup.delivery_fee, 0.0) AS delivery_fee,
    COALESCE(dedup.discount, 0.0) AS discount,
    -- Derived KPI: Total Amount Formula
    ROUND((dedup.quantity * dedup.price + COALESCE(dedup.delivery_fee, 0.0) - COALESCE(dedup.discount, 0.0)), 2) AS total_amount,
    -- Standardize payment method casing
    CASE 
        WHEN LOWER(TRIM(dedup.payment_method)) = 'upi' THEN 'UPI'
        WHEN LOWER(TRIM(dedup.payment_method)) = 'cash' THEN 'Cash'
        WHEN LOWER(TRIM(dedup.payment_method)) = 'credit card' THEN 'Credit Card'
        WHEN LOWER(TRIM(dedup.payment_method)) = 'debit card' THEN 'Debit Card'
        WHEN LOWER(TRIM(dedup.payment_method)) = 'wallet' THEN 'Wallet'
        ELSE INITCAP(TRIM(dedup.payment_method))
    END AS payment_method,
    -- Standardize order status casing
    CASE 
        WHEN LOWER(TRIM(dedup.order_status)) = 'delivered' THEN 'Delivered'
        WHEN LOWER(TRIM(dedup.order_status)) = 'cancelled' THEN 'Cancelled'
        WHEN LOWER(TRIM(dedup.order_status)) = 'pending' THEN 'Pending'
        ELSE INITCAP(TRIM(dedup.order_status))
    END AS order_status,
    COALESCE(dedup.delivery_time_minutes, 0) AS delivery_time_minutes,
    COALESCE(dedup.customer_rating, 0.0) AS customer_rating
FROM (
    SELECT 
        r.*,
        ROW_NUMBER() OVER (
            PARTITION BY r.order_id 
            ORDER BY r.order_date DESC, r.order_time DESC
        ) AS rn
    FROM food_delivery_raw r
    WHERE r.order_id IS NOT NULL 
      AND TRIM(r.order_id) != ''
      AND r.customer_id IS NOT NULL 
      AND TRIM(r.customer_id) != ''
      AND r.price IS NOT NULL 
      AND r.price > 0
      AND r.quantity IS NOT NULL 
      AND r.quantity > 0
      AND (r.delivery_time_minutes IS NULL OR r.delivery_time_minutes >= 0)
) dedup
WHERE dedup.rn = 1;

-- Record verification in cleaned production table
SELECT 'CLEANED_DATA_COUNT' AS metric, COUNT(*) AS val FROM food_delivery_cleaned;
