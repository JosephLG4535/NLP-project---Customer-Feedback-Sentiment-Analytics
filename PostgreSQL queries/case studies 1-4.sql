/* case 1 : positive vs negative delivery feedback by premium and regular customers
			in year 2023 and year 2024 */
			
-- positive/negative feedback on delivery by premium and regular customers 
-- for year 2024 and year 2023
SELECT cu_fb.feedback_id, cu.customer_name, cu_fb.feedback_category, cu_fb.feedback_text,
	cu_fb.rating, cu_fb.sentiment, cu.customer_segment, 
	cu.total_order,cu.avg_order_val, cu_fb.feedback_date
FROM customer_feedback AS cu_fb
INNER JOIN customers AS cu
	ON cu_fb.customer_id = cu.customer_id
WHERE customer_segment IN ('Premium','Regular')
	AND feedback_category = 'Delivery'
	AND sentiment != 'Neutral'
ORDER BY sentiment, feedback_date;

-- positive/negative feedback distribution for delivery on regular and premium customers 
-- for year 2024 and year 2023
SELECT customer_segment, sentiment, EXTRACT(YEAR FROM cu_fb.feedback_date) 
	AS feedback_year, COUNT(cu_fb.feedback_id) AS no_of_feedback,
	ROUND(100.0 * COUNT(cu_fb.feedback_id) / SUM(COUNT(cu_fb.feedback_id)) 
		OVER (PARTITION BY cu.customer_segment, EXTRACT(YEAR FROM cu_fb.feedback_date)), 2) 
		AS percentage
FROM customer_feedback AS cu_fb
INNER JOIN customers AS cu
	ON cu_fb.customer_id = cu.customer_id
WHERE customer_segment IN ('Premium','Regular')
	AND feedback_category = 'Delivery'
	AND sentiment != 'Neutral'
GROUP BY cu.customer_segment, cu_fb.sentiment, feedback_year
ORDER BY feedback_year, cu.customer_segment, sentiment DESC;





/* case 2 : top 5 products with most positive vs negative feedback
			by premium,regular and new customers */
			
-- positive/negative feedback for every orders with product detail 
-- for "New", "Regular" and "Premium"
SELECT pd.product_id, pd.product_name, pd.category, cu.customer_segment, cu_fb.feedback_id,
	cu_fb.order_id, cu_fb.sentiment, cu_fb.feedback_category
FROM order_items AS od_it
INNER JOIN customer_feedback AS cu_fb
	ON od_it.order_id = cu_fb.order_id
INNER JOIN products AS pd
	ON od_it.product_id = pd.product_id
INNER JOIN customers AS cu
	ON cu_fb.customer_id = cu.customer_id
WHERE sentiment != 'Neutral'
	AND customer_segment != 'Inactive'
ORDER BY pd.product_id, cu_fb.sentiment DESC, cu.customer_segment;


-- product with most positive and negative feedback for "New", "Regular" and "Premium"
WITH feedback_percent AS (
SELECT pd.product_name, cu_fb.sentiment, 
	COUNT(cu_fb.feedback_id) AS no_of_feedback, 
	ROUND(100.0 * COUNT(cu_fb.feedback_id) / SUM(COUNT(cu_fb.feedback_id))
		OVER (PARTITION BY pd.product_name), 2) AS percentage
FROM order_items AS od_it
INNER JOIN customer_feedback AS cu_fb
	ON od_it.order_id = cu_fb.order_id
INNER JOIN products AS pd
	ON od_it.product_id = pd.product_id
INNER JOIN customers AS cu
	ON cu_fb.customer_id = cu.customer_id
WHERE sentiment != 'Neutral'
	AND customer_segment != 'Inactive'
GROUP BY pd.product_name, cu_fb.sentiment
ORDER BY pd.product_name, cu_fb.sentiment DESC
),
ranked_feedback AS (
	SELECT *, ROW_NUMBER() OVER (PARTITION BY sentiment ORDER BY no_of_feedback DESC) AS rnk
	FROM feedback_percent
)
SELECT product_name, sentiment, no_of_feedback
FROM ranked_feedback
WHERE rnk <= 5
ORDER BY sentiment DESC, no_of_feedback DESC;


-- get top 5 categories with most feedback
WITH feedback_percent AS (
SELECT pd.category, cu_fb.sentiment, 
	COUNT(cu_fb.feedback_id) AS no_of_feedback, 
	ROUND(100.0 * COUNT(cu_fb.feedback_id) / SUM(COUNT(cu_fb.feedback_id))
		OVER (PARTITION BY pd.category), 2) AS percentage
FROM order_items AS od_it
INNER JOIN customer_feedback AS cu_fb
	ON od_it.order_id = cu_fb.order_id
INNER JOIN products AS pd
	ON od_it.product_id = pd.product_id
INNER JOIN customers AS cu
	ON cu_fb.customer_id = cu.customer_id
WHERE sentiment != 'Neutral'
	AND customer_segment != 'Inactive'
GROUP BY pd.category, cu_fb.sentiment
ORDER BY pd.category, cu_fb.sentiment DESC
),
ranked_feedback AS (
	SELECT *, ROW_NUMBER() OVER (PARTITION BY sentiment ORDER BY no_of_feedback DESC) AS rnk
	FROM feedback_percent
)
SELECT category, sentiment, no_of_feedback, rnk
FROM ranked_feedback
WHERE rnk <= 5
ORDER BY sentiment DESC, no_of_feedback DESC;



/* case 3 : Finding Top 5 Areas with Highest Average Order Value 
			and Delivery Performance in those Areas */

-- getting average order values for each area
WITH area_revenue AS (
SELECT area, SUM(total_order) AS no_of_order, 
	ROUND(AVG(avg_order_val),2) AS avg_order_amt
FROM customers 
GROUP BY area
),
-- getting ranks based on average order values
ranked_avg_order AS(
	SELECT *, ROW_NUMBER() OVER (ORDER BY avg_order_amt DESC) AS rnk
	FROM area_revenue
)
SELECT area, no_of_order, avg_order_amt
FROM ranked_avg_order
WHERE rnk <= 5;


-- getting number of orders for each area
WITH area_revenue AS (
SELECT area, SUM(total_order) AS no_of_order, 
	ROUND(AVG(avg_order_val),2) AS avg_order_amt
FROM customers 
GROUP BY area
),
-- getting ranks based on number of orders 
ranked_no_order AS(
	SELECT *, ROW_NUMBER() OVER (ORDER BY no_of_order DESC) AS rnk
	FROM area_revenue
)
SELECT area, avg_order_amt, no_of_order
FROM ranked_no_order
WHERE rnk <=5;



-- finding the average_delivery_mins in the areas
-- avg : Suryapet, Phusro, Kulti, Nadiad, Siwan
-- no_of_order : Deoghar, Orai, Jalna, Bathinda, Machilipatnam
WITH area_deli_mins AS (
	SELECT area, ROUND(AVG(deli_pf.delivery_time_mins),2) AS avg_delivery_mins
	FROM customers AS cu
	INNER JOIN customer_feedback AS cu_fb
		ON cu.customer_id = cu_fb.customer_id
	INNER JOIN delivery_performance AS deli_pf
		ON cu_fb.order_id = deli_pf.order_id
	WHERE cu.area IN ('Suryapet', 'Phusro', 'Kulti', 'Nadiad', 'Siwan','Deoghar','Orai',
		'Jalna','Bathinda','Machilipatnam')
	GROUP BY area 
)
SELECT *, 
	CASE
		WHEN avg_delivery_mins < 5 THEN 'Good'
		WHEN avg_delivery_mins > 10 THEN 'Bad'
		ELSE 'Decent'
	END AS performance
FROM area_deli_mins
ORDER BY avg_delivery_mins;



/* case 4 : Finding Products that are Selling and Not Selling in Year 2024 */
-- for year 2024
WITH sales_tab AS (
	SELECT od.order_id, od_it.product_id, pd.product_name, pd.category, 
		pd.price, od_it.quantity, (pd.price * od_it.quantity) AS total_amt
	FROM order_items AS od_it
	INNER JOIN orders AS od
		ON od_it.order_id = od.order_id
	INNER JOIN products AS pd
		ON od_it.product_id = pd.product_id
	WHERE od.order_date > '2023-12-31'
),
sales_calc AS (
	SELECT product_name, SUM(total_amt) AS total_sales_2024
	FROM sales_tab
	GROUP BY product_name
),
-- for year 2023
sales_tab2 AS (
	SELECT od.order_id, od_it.product_id, pd.product_name, pd.category, 
		pd.price, od_it.quantity, (pd.price * od_it.quantity) AS total_amt
	FROM order_items AS od_it
	INNER JOIN orders AS od
		ON od_it.order_id = od.order_id
	INNER JOIN products AS pd
		ON od_it.product_id = pd.product_id
	WHERE od.order_date < '2024-01-01'
),
sales_calc2 AS (
	SELECT product_name, SUM(total_amt) AS total_sales_2023
	FROM sales_tab2
	GROUP BY product_name
),
-- change ROW_NUMBER() OVER (ORDER BY total_sales_2024 ASC) to get lowest sales
ranked_sales AS ( 
	SELECT *, ROW_NUMBER() OVER (ORDER BY total_sales_2024 ASC) AS rnk
	FROM sales_calc
)
SELECT calc1.product_name, total_sales_2023, total_sales_2024, 
	ROUND((total_sales_2024/total_sales_2023)*100.0,0) AS growth_pct
FROM ranked_sales AS calc1
INNER JOIN sales_calc2 AS calc2
	ON calc1.product_name = calc2.product_name
WHERE rnk <= 10;


-- finding category top 3
-- for year 2024
WITH sales_tab AS (
	SELECT od.order_id, od_it.product_id, pd.product_name, pd.category, 
		pd.price, od_it.quantity, (pd.price * od_it.quantity) AS total_amt
	FROM order_items AS od_it
	INNER JOIN orders AS od
		ON od_it.order_id = od.order_id
	INNER JOIN products AS pd
		ON od_it.product_id = pd.product_id
	WHERE od.order_date > '2023-12-31'
),
sales_calc AS (
	SELECT category, SUM(total_amt) AS total_sales_2024
	FROM sales_tab
	GROUP BY category
),
-- for year 2023
sales_tab2 AS (
	SELECT od.order_id, od_it.product_id, pd.product_name, pd.category, 
		pd.price, od_it.quantity, (pd.price * od_it.quantity) AS total_amt
	FROM order_items AS od_it
	INNER JOIN orders AS od
		ON od_it.order_id = od.order_id
	INNER JOIN products AS pd
		ON od_it.product_id = pd.product_id
	WHERE od.order_date < '2024-01-01'
),
sales_calc2 AS (
	SELECT category, SUM(total_amt) AS total_sales_2023
	FROM sales_tab2
	GROUP BY category
),
-- change ROW_NUMBER() OVER (ORDER BY total_sales_2024 ASC) to get lowest sales
ranked_sales AS ( 
	SELECT *, ROW_NUMBER() OVER (ORDER BY total_sales_2024 DESC) AS rnk
	FROM sales_calc
)
SELECT calc1.category, total_sales_2023, total_sales_2024, 
	ROUND((total_sales_2024/total_sales_2023)*100.0,0) AS growth_pct
FROM ranked_sales AS calc1
INNER JOIN sales_calc2 AS calc2
	ON calc1.category = calc2.category
WHERE rnk <= 3;


-- rank by product sales growth
WITH sales_tab AS (
	SELECT od.order_id, od_it.product_id, pd.product_name, pd.category, 
		pd.price, od_it.quantity, (pd.price * od_it.quantity) AS total_amt
	FROM order_items AS od_it
	INNER JOIN orders AS od
		ON od_it.order_id = od.order_id
	INNER JOIN products AS pd
		ON od_it.product_id = pd.product_id
	WHERE od.order_date > '2023-12-31'
),
sales_calc AS (
	SELECT product_name, SUM(total_amt) AS total_sales_2024
	FROM sales_tab
	GROUP BY product_name
),
-- for year 2023
sales_tab2 AS (
	SELECT od.order_id, od_it.product_id, pd.product_name, pd.category, 
		pd.price, od_it.quantity, (pd.price * od_it.quantity) AS total_amt
	FROM order_items AS od_it
	INNER JOIN orders AS od
		ON od_it.order_id = od.order_id
	INNER JOIN products AS pd
		ON od_it.product_id = pd.product_id
	WHERE od.order_date < '2024-01-01'
),
sales_calc2 AS (
	SELECT product_name, SUM(total_amt) AS total_sales_2023
	FROM sales_tab2
	GROUP BY product_name
),
ranked_sales AS (
	SELECT calc1.product_name, total_sales_2023, total_sales_2024, 
	ROUND((total_sales_2024/total_sales_2023)*100.0,0) AS growth_pct
	FROM sales_calc AS calc1
	INNER JOIN sales_calc2 AS calc2
		ON calc1.product_name = calc2.product_name
),
-- change ROW_NUMBER() OVER (ORDER BY ..... ASC) to get lowest sales
ranked_growth AS ( 
	SELECT *, ROW_NUMBER() OVER (ORDER BY growth_pct DESC) AS rnk
	FROM ranked_sales
)
SELECT product_name, total_sales_2023, total_sales_2024, growth_pct
FROM ranked_growth
WHERE rnk <= 10;

