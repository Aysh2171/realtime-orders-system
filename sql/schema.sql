CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    product_name VARCHAR(100),
    status VARCHAR(20) CHECK (status IN ('pending', 'shipped', 'delivered')),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);