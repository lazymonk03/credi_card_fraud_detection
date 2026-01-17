/* =========================================================
   Project: Credit Card Fraud Detection (ASK → ACT)
   Phase  : PREPARE – SQL Data Loading & Validation
   DB     : PostgreSQL
   Author : Amar Jeet
   Notes  :
   - Time column stored as DOUBLE PRECISION
   - Source CSV contains scientific notation values (e.g., 1e+05)
   ========================================================= */

-- STEP 1: Create Database (run once from postgres DB)
-- CREATE DATABASE credit_fraud_db;

-- STEP 2: Connect to Database
-- \c credit_fraud_db


-- STEP 3: Drop table if it already exists
DROP TABLE IF EXISTS credit_card_transactions;


-- STEP 4: Create Table Schema
CREATE TABLE credit_card_transactions (
    time DOUBLE PRECISION,
    v1 DOUBLE PRECISION,
    v2 DOUBLE PRECISION,
    v3 DOUBLE PRECISION,
    v4 DOUBLE PRECISION,
    v5 DOUBLE PRECISION,
    v6 DOUBLE PRECISION,
    v7 DOUBLE PRECISION,
    v8 DOUBLE PRECISION,
    v9 DOUBLE PRECISION,
    v10 DOUBLE PRECISION,
    v11 DOUBLE PRECISION,
    v12 DOUBLE PRECISION,
    v13 DOUBLE PRECISION,
    v14 DOUBLE PRECISION,
    v15 DOUBLE PRECISION,
    v16 DOUBLE PRECISION,
    v17 DOUBLE PRECISION,
    v18 DOUBLE PRECISION,
    v19 DOUBLE PRECISION,
    v20 DOUBLE PRECISION,
    v21 DOUBLE PRECISION,
    v22 DOUBLE PRECISION,
    v23 DOUBLE PRECISION,
    v24 DOUBLE PRECISION,
    v25 DOUBLE PRECISION,
    v26 DOUBLE PRECISION,
    v27 DOUBLE PRECISION,
    v28 DOUBLE PRECISION,
    amount DOUBLE PRECISION,
    class INTEGER
);


-- STEP 5: Load CSV Data
-- IMPORTANT:
-- Replace YOUR_USERNAME with your Mac username

-- Example:
-- /Users/amarjeet/Desktop/credi_fraud/creditcard.csv

\copy credit_card_transactions
FROM '/Users/YOUR_USERNAME/Desktop/credi_fraud/creditcard.csv'
DELIMITER ','
CSV HEADER;


-- STEP 6: Data Validation Checks

-- 6.1 Total Row Count
SELECT COUNT(*) AS total_rows
FROM credit_card_transactions;


-- 6.2 Fraud vs Non-Fraud Distribution
SELECT
    class,
    COUNT(*) AS transaction_count
FROM credit_card_transactions
GROUP BY class;


-- 6.3 Fraud Percentage (Critical Business Metric)
SELECT
    class,
    COUNT(*) AS cnt,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER(),
        4
    ) AS percentage
FROM credit_card_transactions
GROUP BY class;


-- 6.4 Null Value Check (Data Quality)
SELECT
    COUNT(*) FILTER (WHERE time IS NULL)   AS time_nulls,
    COUNT(*) FILTER (WHERE amount IS NULL) AS amount_nulls
FROM credit_card_transactions;


-- 6.5 Sample Records Check
SELECT *
FROM credit_card_transactions
LIMIT 10;

