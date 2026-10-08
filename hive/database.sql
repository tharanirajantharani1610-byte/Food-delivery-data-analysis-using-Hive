-- ==============================================================================
-- STEP 5: Create Food Delivery Hive Database
-- ==============================================================================

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS food_delivery_db
COMMENT 'Enterprise Food Delivery Analytics Database'
WITH DBPROPERTIES ('creator' = 'BigDataEngineer', 'created_date' = '2024');

-- Switch to database context
USE food_delivery_db;

-- Display confirmation
SHOW DATABASES;
