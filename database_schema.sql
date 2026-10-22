
CREATE TABLE customers (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name TEXT NOT NULL,
	email TEXT NOT NULL,
	role TEXT NOT NULL DEFAULT 'user'
);

CREATE TABLE products (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name TEXT NOT NULL,
	price NUMERIC(10,2) NOT NULL,
	stock INTEGER NOT NULL,
	CONSTRAINT products_price_nonnegative CHECK (price >= 0),
	CONSTRAINT products_stock_nonnegative CHECK (stock >= 0)
);


CREATE TABLE orders_new (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	customer_id INTEGER NOT NULL,
	FOREIGN KEY (customer_id) REFERENCES customers(id)
);


CREATE TABLE order_items (
	order_id integer,
	product_id integer,
	quantity INTEGER NOT NULL CHECK(quantity > 0),
	PRIMARY KEY(order_id, product_id),
	CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) 
	REFERENCES orders_new(id) ON DELETE CASCADE,
	FOREIGN KEY (product_id) REFERENCES products(id)
);
