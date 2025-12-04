/* case 5 : Finding Top 3 Products and Product Categories Order Rate 
			for Each Customer Segment  */
SELECT pd.product_name,  cu.customer_segment, COUNT(od.order_id) AS no_of_order
FROM orders AS od 
INNER JOIN customers AS cu
	ON od.customer_id = cu.customer_id
INNER JOIN order_items AS od_it
	ON od.order_id = od_it.order_id
INNER JOIN products AS pd
	ON od_it.product_id = pd.product_id
GROUP BY pd.product_name, cu.customer_segment
ORDER BY no_of_order DESC;

-- top 3 products for each customer segment
WITH ranked_product AS (
	SELECT pd.product_name || ' (' || pd.category || ')' AS item,  
	cu.customer_segment, COUNT(od.order_id) AS no_of_order,
	ROW_NUMBER() OVER (PARTITION BY cu.customer_segment 
		ORDER BY COUNT(od.order_id) DESC) AS rnk
	FROM orders AS od 
	INNER JOIN customers AS cu
		ON od.customer_id = cu.customer_id
	INNER JOIN order_items AS od_it
		ON od.order_id = od_it.order_id
	INNER JOIN products AS pd
		ON od_it.product_id = pd.product_id
	GROUP BY pd.product_name, pd.category, cu.customer_segment
)
SELECT item, customer_segment, no_of_order
FROM ranked_product
WHERE rnk <= 3   
ORDER BY
	CASE customer_segment
		WHEN 'Premium' THEN 1
		WHEN 'Regular' THEN 2
		WHEN 'New' THEN 3
		ELSE 4
	END, no_of_order DESC;


-- top 3 categories for each customer segment
WITH ranked_cat AS (
	SELECT pd.category,  
	cu.customer_segment, COUNT(od.order_id) AS no_of_order,
	ROW_NUMBER() OVER (PARTITION BY cu.customer_segment 
		ORDER BY COUNT(od.order_id) DESC) AS rnk
	FROM orders AS od 
	INNER JOIN customers AS cu
		ON od.customer_id = cu.customer_id
	INNER JOIN order_items AS od_it
		ON od.order_id = od_it.order_id
	INNER JOIN products AS pd
		ON od_it.product_id = pd.product_id
	GROUP BY pd.category, cu.customer_segment
)
SELECT category, customer_segment, no_of_order
FROM ranked_cat
WHERE rnk <= 3   
ORDER BY
	CASE customer_segment
		WHEN 'Premium' THEN 1
		WHEN 'Regular' THEN 2
		WHEN 'New' THEN 3
		ELSE 4
	END, no_of_order DESC;

/*
WITH ranked_product AS (
	SELECT pd.product_name,  
	cu.customer_segment, COUNT(od.order_id) AS no_of_order,
	ROW_NUMBER() OVER (PARTITION BY cu.customer_segment 
		ORDER BY COUNT(od.order_id) DESC) AS rnk
	FROM orders AS od 
	INNER JOIN customers AS cu
		ON od.customer_id = cu.customer_id
	INNER JOIN order_items AS od_it
		ON od.order_id = od_it.order_id
	INNER JOIN products AS pd
		ON od_it.product_id = pd.product_id
	GROUP BY pd.product_name, cu.customer_segment
)
SELECT product_name, customer_segment, no_of_order
FROM ranked_product
WHERE rnk <= 3   
ORDER BY
	CASE customer_segment
		WHEN 'Premium' THEN 1
		WHEN 'Regular' THEN 2
		WHEN 'New' THEN 3
		ELSE 4
	END, no_of_order DESC;
*/





/* case 6 :  Finding Engagement Rate for Marketing Campaign Held in Each Channel 
			 for the Year 2024 */
WITH engage_rate AS (
	SELECT target_audience, channel,
    	SUM(impressions*0.15 + clicks*0.35 + conversions*0.5) AS engagement_rate
	FROM marketing_performance
	WHERE campaign_date > '2023-12-31'
	GROUP BY target_audience, channel
),
total_engage AS (
	SELECT *, SUM(engagement_rate) OVER (PARTITION BY channel, target_audience) 
		AS total_engagement
	FROM engage_rate
)
SELECT channel, target_audience, total_engagement
FROM total_engage
WHERE target_audience != 'All'
ORDER BY channel, total_engagement DESC;

WITH engage_rate AS (
	SELECT channel,
    	SUM(impressions*0.15 + clicks*0.35 + conversions*0.5) AS engagement_rate
	FROM marketing_performance
	WHERE campaign_date > '2023-12-31'
	GROUP BY channel
),
total_engage AS (
	SELECT *, SUM(engagement_rate) OVER (PARTITION BY channel) 
		AS total_engagement
	FROM engage_rate
)
SELECT channel, total_engagement
FROM total_engage
ORDER BY total_engagement DESC;






/* case 7 : Finding Overall Campaign Effectiveness on "New Users" and "Inactive" Customers
			for "App" and "Social Media" Channels*/
WITH campaign_profit AS (
	SELECT channel, target_audience, 
	ROUND(AVG(return_from_ad),2) AS avg_gain
	FROM marketing_performance
	WHERE channel IN ('App','Social Media') 
		AND target_audience IN ('New Users','Inactive')
	GROUP BY target_audience, channel
)
SELECT * 
FROM campaign_profit
ORDER BY channel ASC, avg_gain DESC;





/* case 8 : Finding Stock Info for the Latest Year (2024) for Top 3 Products 
			for "Regular" and "Premium" Customers based on Order Total in Store */
WITH total_tab AS (
	SELECT pd.product_id, pd.product_name, pd.brand, cu.customer_segment, 
	SUM (od.order_total) AS total_profit
	FROM order_items AS od_it
	INNER JOIN orders AS od
		ON od.order_id = od_it.order_id
	INNER JOIN products AS pd
		ON pd.product_id = od_it.product_id
	INNER JOIN customers AS cu
		ON od.customer_id = cu.customer_id
	WHERE cu.customer_segment IN ('Regular','Premium') 
	GROUP BY pd.product_id, pd.product_name, cu.customer_segment
),
ranked_profit AS (
	SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_segment 
		ORDER BY total_profit DESC) AS rnk
	FROM total_tab
)
SELECT product_id, product_name, brand, customer_segment, total_profit
FROM ranked_profit
WHERE rnk <= 3;	

-- Find inventory and stock level for top products
-- "Premium" products : 604184, 337168, 123983
-- "Regular" products : 114414, 34186, 487931
WITH stock_tab AS (
    SELECT pd.product_id, pd.product_name, pd.brand, 
		MAX(DATE_TRUNC('year', date_received)) AS max_year
    FROM inventory AS inv
    LEFT JOIN products AS pd
        ON pd.product_id = inv.product_id
    WHERE pd.product_id IN ('604184', '337168', '123983','114414', '34186', '487931')
    GROUP BY pd.product_id
),
latest_stock AS (
	SELECT news.product_id, news.product_name, news.brand, pd.shell_life_days,
		SUM(inv.stock_received) AS received_no, SUM(inv.damaged_stock) AS faulty_no,
		news.max_year
	FROM stock_tab AS news
	LEFT JOIN inventory AS inv
		ON inv.product_id = news.product_id
	LEFT JOIN products AS pd
    	ON news.product_id = pd.product_id
	WHERE DATE_TRUNC('year', inv.date_received) = max_year
	GROUP BY news.product_id, news.product_name, news.brand, pd.shell_life_days, 
		news.max_year
)
SELECT news.product_id, news.product_name, news.brand, news.received_no, 
	news.faulty_no, received_no - faulty_no AS qty_sellable, 
	SUM(od_it.quantity) AS qty_sold, news.shell_life_days
FROM latest_stock AS news
LEFT JOIN order_items AS od_it
    ON news.product_id = od_it.product_id
LEFT JOIN orders AS od
    ON od.order_id = od_it.order_id
WHERE DATE_TRUNC('year', od.order_date) = news.max_year
GROUP BY news.product_id, news.product_name, news.brand, news.shell_life_days,
	news.received_no, news.faulty_no;





