SELECT cu_fb.feedback_id, cu_fb.order_id, cu_fb.customer_id, cu_fb.rating, 
	cu_fb.feedback_text, cu_fb.feedback_category, cu_fb.sentiment,
	EXTRACT(YEAR FROM cu_fb.feedback_date) AS feedback_year, 
	EXTRACT(MONTH FROM cu_fb.feedback_date) AS feedback_month,
	EXTRACT(DAY FROM cu_fb.feedback_date) AS feedback_day, 
	CASE 
        WHEN EXTRACT(DOW FROM cu_fb.feedback_date) IN (0, 6) THEN 'Weekend'
        ELSE 'Weekday'
	END AS day_type, cu.area, cu.customer_segment,
	TO_CHAR(od.order_time,'HH24:MI') AS orders_time, od.delivery_status, deli_pf.delivery_time_mins
FROM customer_feedback AS cu_fb
LEFT JOIN customers AS cu
	ON cu_fb.customer_id = cu.customer_id
INNER JOIN orders AS od
	ON cu_fb.order_id = od.order_id
LEFT JOIN delivery_performance AS deli_pf
	ON cu_fb.order_id = deli_pf.order_id;