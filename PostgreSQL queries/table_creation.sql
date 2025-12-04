-- 8 tables creation
CREATE TABLE IF NOT EXISTS customer_feedback(
	feedback_id BIGINT NOT NULL,
	order_id BIGINT,
	customer_id BIGINT,
	rating INT,
	feedback_text VARCHAR(255),
	feedback_category VARCHAR(50),
	sentiment VARCHAR(50),
	feedback_date DATE,
	PRIMARY KEY (feedback_id)
);

CREATE TABLE IF NOT EXISTS customers(
	customer_id INT NOT NULL,
	customer_name VARCHAR(100),
	email VARCHAR(100),
	phone BIGINT,
	address VARCHAR(255),
	area VARCHAR(50),
	pincode BIGINT,
	registration_date DATE,
	customer_segment VARCHAR(50),
	total_order INT,
	avg_order_val NUMERIC(10,2),
	PRIMARY KEY (customer_id)
);

CREATE TABLE IF NOT EXISTS delivery_performance(
	order_id BIGINT,
	delivery_partner_id BIGINT,
	promised_time TIME,
	actual_time TIME,
	promised_date DATE,
	actual_date DATE,
	delivery_time_mins INT,
	distance_km NUMERIC(10,2),
	delivery_status VARCHAR(50),
	delay_reason VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS inventory(
	product_id BIGINT,
	date_received DATE,
	stock_received INT,
	damaged_stock INT
);

CREATE TABLE IF NOT EXISTS marketing_performance(
	campaign_id BIGINT NOT NULL,
	campaign_name VARCHAR(255),
	campaign_date DATE,
	target_audience VARCHAR(50),
	channel VARCHAR(50),
	impressions INT,
	clicks INT,
	conversions INT,
	spend NUMERIC(10,2),
	revenue NUMERIC(10,2),
	return_from_ad NUMERIC(10,2),
	PRIMARY KEY(campaign_id)
);

CREATE TABLE IF NOT EXISTS order_items(
	order_id BIGINT,
	product_id BIGINT,
	quantity INT,
	unit_price NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS orders(
	order_id BIGINT NOT NULL,
	customer_id BIGINT,
	order_time TIME,
	order_date DATE,
	promised_delivery_time TIME,
	promised_delivery_date DATE,
	actual_delivery_time TIME,
	actual_delivery_date DATE,
	delivery_status VARCHAR(50),
	order_total NUMERIC(10,2),
	payment_method VARCHAR(50),
	delivery_partner_id BIGINT,
	store_id BIGINT,
	PRIMARY KEY (order_id)
);

CREATE TABLE IF NOT EXISTS products(
	product_id BIGINT NOT NULL,
	product_name VARCHAR(100),
	category VARCHAR(255),
	brand VARCHAR(255),
	price NUMERIC(10,2),
	max_sell_price NUMERIC(10,2),
	margin_percent INT,
	shell_life_days INT,
	min_stock INT,
	max_stock INT,
	PRIMARY KEY (product_id)
);

