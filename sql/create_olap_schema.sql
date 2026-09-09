IF OBJECT_ID('dbo.dim_date', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.dim_date (
        date_sk INT NOT NULL PRIMARY KEY,
        full_date DATE NOT NULL UNIQUE,
        day INT NOT NULL,
        month INT NOT NULL,
        month_name NVARCHAR(20) NOT NULL,
        quarter INT NOT NULL,
        year INT NOT NULL,
        weekday_name NVARCHAR(20) NOT NULL
    );
END;
GO

-- SCD Type 2
IF OBJECT_ID('dbo.dim_customer', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.dim_customer (
        customer_sk INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        customer_id INT NOT NULL,
        full_name NVARCHAR(200),
        email NVARCHAR(200),
        phone NVARCHAR(50),
        city NVARCHAR(100),
        state NVARCHAR(100),
        zip_code NVARCHAR(20),
        start_date DATE NOT NULL,
        end_date DATE NULL,
        current_flag CHAR(1) NOT NULL
            CONSTRAINT CK_dim_customer_current_flag CHECK (current_flag IN ('Y', 'N'))
    );
END;
GO

-- SCD Type 1
IF OBJECT_ID('dbo.dim_product', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.dim_product (
        product_sk INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        product_id INT NOT NULL,
        product_name NVARCHAR(200),
        category_id INT,
        category_name NVARCHAR(100),
        brand_id INT,
        brand_name NVARCHAR(100),
        model_year INT,
        list_price DECIMAL(10,2)
    );
END;
GO

-- SCD Type 2
IF OBJECT_ID('dbo.dim_staff', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.dim_staff (
        staff_sk INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        staff_id INT NOT NULL,
        full_name NVARCHAR(200),
        email NVARCHAR(200),
        phone NVARCHAR(50),
        store_id INT,
        manager_id INT,
        start_date DATE NOT NULL,
        end_date DATE NULL,
        current_flag CHAR(1) NOT NULL
            CONSTRAINT CK_dim_staff_current_flag CHECK (current_flag IN ('Y', 'N'))
    );
END;
GO

-- SCD Type 1
IF OBJECT_ID('dbo.dim_store', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.dim_store (
        store_sk INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        store_id INT NOT NULL,
        store_name NVARCHAR(200),
        street NVARCHAR(200),
        city NVARCHAR(100),
        state NVARCHAR(100),
        zip_code NVARCHAR(20)
    );
END;
GO

-- Fact Sales
IF OBJECT_ID('dbo.fact_sales', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.fact_sales (
        sales_sk INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        order_id INT NOT NULL,
        item_id INT NOT NULL,
        customer_sk INT NULL,
        product_sk INT NULL,
        staff_sk INT NULL,
        store_sk INT NULL,
        order_date_sk INT NULL,
        quantity INT NOT NULL,
        list_price DECIMAL(10,2) NOT NULL,
        discount DECIMAL(5,4) NOT NULL,
        total_price DECIMAL(10,2) NOT NULL,
        CONSTRAINT UQ_fact_sales_order_item UNIQUE (order_id, item_id),
        CONSTRAINT CK_fact_sales_quantity CHECK (quantity > 0),
        CONSTRAINT CK_fact_sales_discount CHECK (discount >= 0 AND discount <= 1)
    );
END;
GO

-- indexes
IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'UX_dim_customer_current'
      AND object_id = OBJECT_ID('dbo.dim_customer')
)
BEGIN
    CREATE UNIQUE INDEX UX_dim_customer_current
        ON dbo.dim_customer(customer_id)
        WHERE current_flag = 'Y';
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'UX_dim_staff_current'
      AND object_id = OBJECT_ID('dbo.dim_staff')
)
BEGIN
    CREATE UNIQUE INDEX UX_dim_staff_current
        ON dbo.dim_staff(staff_id)
        WHERE current_flag = 'Y';
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'UX_dim_product_business_key'
      AND object_id = OBJECT_ID('dbo.dim_product')
)
BEGIN
    CREATE UNIQUE INDEX UX_dim_product_business_key
        ON dbo.dim_product(product_id);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'UX_dim_store_business_key'
      AND object_id = OBJECT_ID('dbo.dim_store')
)
BEGIN
    CREATE UNIQUE INDEX UX_dim_store_business_key
        ON dbo.dim_store(store_id);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_fact_sales_customer'
      AND object_id = OBJECT_ID('dbo.fact_sales')
)
BEGIN
    CREATE INDEX IX_fact_sales_customer
        ON dbo.fact_sales(customer_sk);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_fact_sales_product'
      AND object_id = OBJECT_ID('dbo.fact_sales')
)
BEGIN
    CREATE INDEX IX_fact_sales_product
        ON dbo.fact_sales(product_sk);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_fact_sales_date'
      AND object_id = OBJECT_ID('dbo.fact_sales')
)
BEGIN
    CREATE INDEX IX_fact_sales_date
        ON dbo.fact_sales(order_date_sk);
END;
GO
