create database ecommerce_project;
use ecommerce_project;
select count(*) from ecommerce_sales;

select * from ecommerce_sales limit 10;

describe ecommerce_sales;

ALTER TABLE ecommerce_sales
DROP COLUMN MyUnknownColumn;

ALTER TABLE ecommerce_sales
CHANGE COLUMN `ï»¿Order_ID` Order_ID TEXT;

ALTER TABLE ecommerce_sales
ADD COLUMN Order_Date_New DATE;

UPDATE ecommerce_sales
SET Order_Date_New = STR_TO_DATE(Order_Date,'%d-%m-%Y');

ALTER TABLE ecommerce_sales
DROP COLUMN Order_Date;

ALTER TABLE ecommerce_sales
CHANGE COLUMN Order_Date_New Order_Date DATE;

describe ecommerce_sales;

-- Total Orders --
select count(*) as Total_Orders
from ecommerce_sales;

-- Total Revenue --
select 
round(sum(Revenue),2) as Total_Revenue
from ecommerce_sales;

-- Total Profit --
select 
round(sum(Profit),2) as Total_Profit
from ecommerce_sales;

-- Profit Margin --
select 
round(sum(Profit)/sum(Revenue)*100,2) as Profit_Margin_Percent
from ecommerce_sales;

-- Revenue by Category --
select Category,
round(sum(Revenue),2) as Revenue
from ecommerce_sales
group by Category
order by Revenue desc;

-- Profit by Category --
select Category,
round(sum(Profit),2) as Profit
from ecommerce_sales
group by Category
order by Profit desc;

-- Revenue by Region --
select Region,
round(sum(Revenue),2) as Revenue
from ecommerce_sales
group by Region
order by Revenue desc;

-- Payment Method Usage --
select Payment_Method,
count(*) as Total_Orders
from ecommerce_sales
group by Payment_Method
order by Total_Orders desc;

-- Monthly Revenue Trend --
select
date_format(Order_Date,'%Y-%m') as Month,
round(sum(Revenue),2) as Revenue
from ecommerce_sales
group by Month
order by Month;

-- Top 10 Products by Revenue --
select Product_Name,
round(sum(Revenue),2) as Revenue
from ecommerce_sales
group by Product_Name
order by Revenue
limit 10;

-- Find products that earn more than average revenue --
SELECT Product_Name,
round(SUM(Revenue),2) AS Total_Revenue
FROM ecommerce_sales
GROUP BY Product_Name
HAVING SUM(Revenue) > (
    SELECT AVG(product_revenue)
    FROM (
        SELECT SUM(Revenue) AS product_revenue
        FROM ecommerce_sales
        GROUP BY Product_Name
    ) AS avg_table
);

-- Find top revenue categories --
WITH category_revenue AS (
SELECT 
Category,
round(SUM(Revenue),2) AS Total_Revenue
FROM ecommerce_sales
GROUP BY Category
)

SELECT *
FROM category_revenue
ORDER BY Total_Revenue DESC;

-- Rank regions by revenue --
SELECT 
Region,
round(SUM(Revenue),2) AS Revenue,
RANK() OVER (ORDER BY SUM(Revenue) DESC) AS Revenue_Rank
FROM ecommerce_sales
GROUP BY Region;

-- Find top customers --
WITH customer_revenue AS (
SELECT 
Customer_ID,
round(SUM(Revenue),2) AS Total_Revenue
FROM ecommerce_sales
GROUP BY Customer_ID
)

SELECT *
FROM customer_revenue
ORDER BY Total_Revenue DESC
LIMIT 10;