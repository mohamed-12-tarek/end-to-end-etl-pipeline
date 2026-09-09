-- 1. Customers
IF OBJECT_ID('dbo.stg_customers', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.stg_customers
    (
        customer_id INT,
        first_name NVARCHAR(100),
        last_name NVARCHAR(100),
        email NVARCHAR(200),
        phone NVARCHAR(50),
        street NVARCHAR(200),
        city NVARCHAR(100),
        state NVARCHAR(100),
        zip_code NVARCHAR(20)
    );
END;
GO


-- 2. Products
IF OBJECT_ID('dbo.stg_products', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.stg_products
    (
        product_id INT,
        product_name NVARCHAR(200),
        brand_id INT,
        category_id INT,
        model_year INT,
        list_price DECIMAL(10,2)
    );
END;
GO


-- 3. Brands
IF OBJECT_ID('dbo.stg_brands', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.stg_brands
    (
        brand_id INT,
        brand_name NVARCHAR(100)
    );
END;
GO


-- 4. Categories
IF OBJECT_ID('dbo.stg_categories', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.stg_categories
    (
        category_id INT,
        category_name NVARCHAR(100)
    );
END;
GO


-- 5. Orders
IF OBJECT_ID('dbo.stg_orders', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.stg_orders
    (
        order_id INT,
        customer_id INT,
        order_status INT,
        order_date DATE,
        required_date DATE,
        shipped_date DATE,
        store_id INT,
        staff_id INT
    );
END;
GO


-- 6. Order Items
IF OBJECT_ID('dbo.stg_order_items', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.stg_order_items
    (
        order_id INT,
        item_id INT,
        product_id INT,
        quantity INT,
        list_price DECIMAL(10,2),
        discount DECIMAL(5,2)
    );
END;
GO


-- 7. Staff
IF OBJECT_ID('dbo.stg_staffs', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.stg_staffs
    (
        staff_id INT,
        first_name NVARCHAR(100),
        last_name NVARCHAR(100),
        email NVARCHAR(200),
        phone NVARCHAR(50),
        active BIT,
        store_id INT,
        manager_id INT
    );
END;
GO


-- 8. Stores
IF OBJECT_ID('dbo.stg_stores', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.stg_stores
    (
        store_id INT,
        store_name NVARCHAR(200),
        phone NVARCHAR(50),
        email NVARCHAR(200),
        street NVARCHAR(200),
        city NVARCHAR(100),
        state NVARCHAR(100),
        zip_code NVARCHAR(20)
    );
END;
GO