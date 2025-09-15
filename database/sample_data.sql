-- Sample Data for SmartTrack Business Analytics
USE smarttrack_db;

-- Insert sample categories
INSERT INTO categories (name, description, category_type) VALUES
('Fresh Produce', 'Fresh fruits and vegetables', 'product'),
('Dairy & Eggs', 'Milk, cheese, yogurt, and eggs', 'product'),
('Beverages', 'Soft drinks, juices, and water', 'product'),
('Snacks & Confectionery', 'Chips, chocolates, and candies', 'product'),
('Household Essentials', 'Cleaning supplies and toiletries', 'product'),

('Inventory Purchase', 'Cost of goods purchased for resale', 'expense'),
('Staff Salaries', 'Employee wages and benefits', 'expense'),
('Utilities', 'Electricity, water, internet bills', 'expense'),
('Rent & Property', 'Store rent and property expenses', 'expense'),
('Marketing & Advertising', 'Promotional and advertising costs', 'expense');

-- Insert sample products
INSERT INTO products (name, description, category_id, unit_of_measure, cost_price, selling_price, current_stock, minimum_stock_level) VALUES
-- Fresh Produce
('Bananas', 'Fresh yellow bananas', 1, 'kg', 150.00, 200.00, 50, 10),
('Tomatoes', 'Fresh red tomatoes', 1, 'kg', 200.00, 280.00, 35, 15),
('Onions', 'Fresh yellow onions', 1, 'kg', 180.00, 250.00, 40, 20),
('Carrots', 'Fresh orange carrots', 1, 'kg', 120.00, 180.00, 25, 10),

-- Dairy & Eggs
('Fresh Milk', 'Peak milk 1 liter', 2, 'liter', 280.00, 350.00, 60, 20),
('Cheese Slices', 'Processed cheese 200g', 2, 'pack', 450.00, 580.00, 30, 15),
('Greek Yogurt', 'Natural yogurt 500ml', 2, 'cup', 320.00, 420.00, 40, 20),
('Fresh Eggs', 'Farm fresh eggs', 2, 'dozen', 400.00, 500.00, 50, 25),

-- Beverages
('Coca Cola', 'Coca Cola 50cl bottle', 3, 'bottle', 80.00, 120.00, 100, 30),
('Orange Juice', 'Fresh orange juice 1L', 3, 'liter', 200.00, 300.00, 25, 10),
('Bottled Water', 'Pure water 75cl', 3, 'bottle', 50.00, 80.00, 120, 40),

-- Snacks
('Chocolate Bar', 'Cadbury dairy milk 45g', 4, 'bar', 150.00, 200.00, 80, 25),
('Potato Chips', 'Pringles original 165g', 4, 'tube', 350.00, 450.00, 40, 15),
('Biscuits', 'Digestive biscuits pack', 4, 'pack', 120.00, 180.00, 60, 20),

-- Household
('Laundry Detergent', 'Washing powder 1kg', 5, 'pack', 280.00, 380.00, 30, 10),
('Toilet Tissue', '4-roll tissue paper', 5, 'pack', 200.00, 280.00, 45, 15);

-- Insert sample expenses (last 3 months)
INSERT INTO expenses (description, amount, category_id, expense_date, payment_method, vendor_name, receipt_number) VALUES
-- November 2024
('Monthly store rent', 150000.00, 9, '2024-11-01', 'bank_transfer', 'Lagos Properties Ltd', 'LP-NOV-001'),
('Electricity bill', 25000.00, 8, '2024-11-05', 'bank_transfer', 'Ikeja Electric', 'IE-NOV-2024'),
('Staff salaries', 180000.00, 7, '2024-11-30', 'bank_transfer', NULL, 'SAL-NOV-2024'),
('Product restocking', 320000.00, 6, '2024-11-10', 'bank_transfer', 'Alaba Market Suppliers', 'AMS-001'),
('Internet and phone', 8000.00, 8, '2024-11-15', 'card', 'MTN Nigeria', 'MTN-NOV'),

-- December 2024
('Monthly store rent', 150000.00, 9, '2024-12-01', 'bank_transfer', 'Lagos Properties Ltd', 'LP-DEC-001'),
('Electricity bill', 28000.00, 8, '2024-12-05', 'bank_transfer', 'Ikeja Electric', 'IE-DEC-2024'),
('Staff salaries', 180000.00, 7, '2024-12-31', 'bank_transfer', NULL, 'SAL-DEC-2024'),
('Product restocking', 450000.00, 6, '2024-12-12', 'bank_transfer', 'Alaba Market Suppliers', 'AMS-002'),
('Marketing flyers', 15000.00, 10, '2024-12-20', 'cash', 'Quick Print', 'QP-001'),

-- January 2025
('Monthly store rent', 150000.00, 9, '2025-01-01', 'bank_transfer', 'Lagos Properties Ltd', 'LP-JAN-001'),
('Electricity bill', 32000.00, 8, '2025-01-05', 'bank_transfer', 'Ikeja Electric', 'IE-JAN-2025'),
('Staff salaries', 180000.00, 7, '2025-01-31', 'bank_transfer', NULL, 'SAL-JAN-2025'),
('Product restocking', 380000.00, 6, '2025-01-08', 'bank_transfer', 'Alaba Market Suppliers', 'AMS-003');

-- Insert sample sales (recent transactions)
INSERT INTO sales (sale_date, total_amount, payment_method, customer_name, discount_amount, tax_amount, notes) VALUES
('2025-01-10', 2400.00, 'cash', NULL, 0.00, 0.00, 'Walk-in customer'),
('2025-01-11', 1850.00, 'card', 'Mrs. Johnson', 0.00, 0.00, 'Regular customer'),
('2025-01-12', 3200.00, 'cash', NULL, 100.00, 0.00, 'Bulk purchase discount'),
('2025-01-13', 2800.00, 'mobile_money', 'Mr. Adebayo', 0.00, 0.00, 'Mobile payment'),
('2025-01-14', 4100.00, 'cash', 'Grace Foods Ltd', 200.00, 0.00, 'Corporate customer'),
('2025-01-15', 1950.00, 'card', NULL, 0.00, 0.00, 'Card payment'),
('2025-01-16', 3500.00, 'cash', 'Mama Ngozi', 150.00, 0.00, 'Long-time customer');

-- Insert sample sale items
INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, total_price, cost_price) VALUES
-- Sale 1 (2025-01-10)
(1, 1, 5, 200.00, 1000.00, 150.00),  -- Bananas
(1, 2, 4, 280.00, 1120.00, 200.00),  -- Tomatoes
(1, 9, 2, 120.00, 240.00, 80.00),    -- Coca Cola

-- Sale 2 (2025-01-11)
(2, 5, 3, 350.00, 1050.00, 280.00),  -- Fresh Milk
(2, 12, 4, 200.00, 800.00, 150.00),  -- Chocolate Bar

-- Sale 3 (2025-01-12)
(3, 1, 8, 200.00, 1600.00, 150.00),  -- Bananas
(3, 3, 6, 250.00, 1500.00, 180.00),  -- Onions
(3, 15, 2, 380.00, 760.00, 280.00),  -- Laundry Detergent

-- Sale 4 (2025-01-13)
(4, 6, 4, 580.00, 2320.00, 450.00),  -- Cheese Slices
(4, 13, 1, 450.00, 450.00, 350.00),  -- Potato Chips

-- Sale 5 (2025-01-14)
(5, 8, 6, 500.00, 3000.00, 400.00),  -- Fresh Eggs
(5, 10, 5, 300.00, 1500.00, 200.00), -- Orange Juice

-- Sale 6 (2025-01-15)
(6, 4, 8, 180.00, 1440.00, 120.00),  -- Carrots
(6, 14, 3, 180.00, 540.00, 120.00),  -- Biscuits

-- Sale 7 (2025-01-16)
(7, 7, 5, 420.00, 2100.00, 320.00),  -- Greek Yogurt
(7, 11, 15, 80.00, 1200.00, 50.00),  -- Bottled Water
(7, 16, 1, 280.00, 280.00, 200.00);  -- Toilet Tissue