-- ==============================================================================
-- STEP 6 & STEP 7: Hive Tables Definition
-- Database: food_delivery_db
-- Tables:
--   1. food_delivery_raw     (Raw CSV Staging Table)
--   2. food_delivery_cleaned (Production Transformed & Validated Table)
-- ==============================================================================

USE food_delivery_db;

-- ------------------------------------------------------------------------------
-- 1. RAW STAGING TABLE
-- Maps directly to the incoming CSV data mounted at /opt/data/food_delivery.csv
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS food_delivery_raw;

CREATE TABLE IF NOT EXISTS food_delivery_raw (
    order_id STRING,
    customer_id STRING,
    restaurant_id STRING,
    restaurant_name STRING,
    customer_city STRING,
    order_date STRING,
    order_time STRING,
    food_category STRING,
    item_name STRING,
    quantity INT,
    price DOUBLE,
    delivery_fee DOUBLE,
    discount DOUBLE,
    payment_method STRING,
    order_status STRING,
    delivery_time_minutes INT,
    customer_rating DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

-- ------------------------------------------------------------------------------
-- 2. CLEANED PRODUCTION ANALYTICS TABLE
-- Contains cleansed, deduplicated, standardized records with total_amount
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS food_delivery_cleaned;

CREATE TABLE IF NOT EXISTS food_delivery_cleaned (
    order_id STRING,
    customer_id STRING,
    restaurant_id STRING,
    restaurant_name STRING,
    customer_city STRING,
    order_date STRING,
    order_time STRING,
    food_category STRING,
    item_name STRING,
    quantity INT,
    price DOUBLE,
    delivery_fee DOUBLE,
    discount DOUBLE,
    total_amount DOUBLE,
    payment_method STRING,
    order_status STRING,
    delivery_time_minutes INT,
    customer_rating DOUBLE
)
STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY");

-- Display table status
SHOW TABLES;
