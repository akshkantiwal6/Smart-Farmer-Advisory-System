-- ============================================
-- SMART CROP MARKET INTELLIGENCE SYSTEM
-- Reusable SQL Queries
-- ============================================

------------------------------------------------
-- 1. Total Records
------------------------------------------------

SELECT COUNT(*) AS Total_Records
FROM market_data;


------------------------------------------------
-- 2. Top 10 Most Expensive Commodities
------------------------------------------------

SELECT
commodity_name,
ROUND(AVG(modal_price),2) AS Average_Price

FROM market_data

GROUP BY commodity_name

ORDER BY Average_Price DESC

LIMIT 10;


------------------------------------------------
-- 3. State-wise Average Price
------------------------------------------------

SELECT

state,

ROUND(AVG(modal_price),2) AS Average_Price

FROM market_data

GROUP BY state

ORDER BY Average_Price DESC;


------------------------------------------------
-- 4. Market-wise Highest Average Price
------------------------------------------------

SELECT

market,

ROUND(AVG(modal_price),2) AS Average_Price

FROM market_data

GROUP BY market

ORDER BY Average_Price DESC

LIMIT 20;


------------------------------------------------
-- 5. Commodity Count
------------------------------------------------

SELECT

commodity_name,

COUNT(*) AS Total_Records

FROM market_data

GROUP BY commodity_name

ORDER BY Total_Records DESC;


------------------------------------------------
-- 6. Monthly Average Price
------------------------------------------------

SELECT

strftime('%Y-%m', date) AS Month,

ROUND(AVG(modal_price),2) AS Average_Price

FROM market_data

GROUP BY Month

ORDER BY Month;