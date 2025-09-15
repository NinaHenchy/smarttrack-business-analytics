-- SmartTrack Business Analytics Database Schema
CREATE DATABASE IF NOT EXISTS smarttrack_db;
USE smarttrack_db;

-- Categories table for organizing products and expenses
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    category_type ENUM('expense', 'product') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category_type (category_type)
);

-- Products table for inventory management
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INT,
    unit_of_measure VARCHAR(50) DEFAULT 'piece',
    cost_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    selling_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    current_stock INT DEFAULT 0,
    minimum_stock_level INT DEFAULT 10,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    INDEX idx_product_name (name),
    INDEX idx_product_active (is_active),
    INDEX idx_product_stock (current_stock, minimum_stock_level)
);

-- Expenses table for tracking business costs
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(500) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    category_id INT,
    expense_date DATE NOT NULL,
    payment_method ENUM('cash', 'card', 'bank_transfer', 'check') DEFAULT 'cash',
    vendor_name VARCHAR(200),
    receipt_number VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    INDEX idx_expense_date (expense_date),
    INDEX idx_expense_amount (amount)
);

-- Sales table for transaction records
CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_method ENUM('cash', 'card', 'bank_transfer', 'mobile_money') DEFAULT 'cash',
    customer_name VARCHAR(200),
    discount_amount DECIMAL(10, 2) DEFAULT 0.00,
    tax_amount DECIMAL(10, 2) DEFAULT 0.00,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_sale_date (sale_date),
    INDEX idx_sale_amount (total_amount)
);

-- Sale items table for detailed transaction breakdown
CREATE TABLE sale_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    cost_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_sale_items_sale (sale_id),
    INDEX idx_sale_items_product (product_id)
);

-- Analytics view for product profitability
CREATE VIEW product_profit_view AS
SELECT
    p.id,
    p.name,
    COALESCE(c.name, 'Uncategorized') as category_name,
    COALESCE(SUM(si.quantity), 0) as total_quantity_sold,
    COALESCE(SUM(si.total_price), 0) as total_revenue,
    COALESCE(SUM(si.cost_price * si.quantity), 0) as total_cost,
    COALESCE(SUM(si.total_price - (si.cost_price * si.quantity)), 0) as total_profit
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN sale_items si ON p.id = si.product_id
GROUP BY p.id, p.name, c.name;

-- Triggers for automatic stock management
DELIMITER //

CREATE TRIGGER update_stock_on_sale
AFTER INSERT ON sale_items
FOR EACH ROW
BEGIN
    UPDATE products
    SET current_stock = current_stock - NEW.quantity,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.product_id;
END//

DELIMITER ;