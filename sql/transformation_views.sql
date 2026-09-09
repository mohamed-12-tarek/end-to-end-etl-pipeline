CREATE OR ALTER VIEW dbo.vw_tr_customers
AS
SELECT
    customer_id,

    NULLIF(
        LTRIM(RTRIM(
            CONCAT(
                UPPER(LEFT(LTRIM(RTRIM(first_name)), 1)),
                LOWER(SUBSTRING(
                    LTRIM(RTRIM(first_name)),
                    2,
                    LEN(LTRIM(RTRIM(first_name)))
                )),
                ' ',
                UPPER(LEFT(LTRIM(RTRIM(last_name)), 1)),
                LOWER(SUBSTRING(
                    LTRIM(RTRIM(last_name)),
                    2,
                    LEN(LTRIM(RTRIM(last_name)))
                ))
            )
        )),
        ''
    ) AS full_name,

    LOWER(NULLIF(LTRIM(RTRIM(email)), '')) AS email,
    NULLIF(LTRIM(RTRIM(phone)), '') AS phone,
    NULLIF(LTRIM(RTRIM(city)), '') AS city,
    UPPER(NULLIF(LTRIM(RTRIM(state)), '')) AS state,
    NULLIF(LTRIM(RTRIM(zip_code)), '') AS zip_code

FROM dbo.stg_customers;
GO


CREATE OR ALTER VIEW dbo.vw_tr_staffs
AS
SELECT
    staff_id,
    NULLIF(
        LTRIM(RTRIM(
            CONCAT(
                UPPER(LEFT(LTRIM(RTRIM(first_name)), 1)),
                LOWER(SUBSTRING(
                    LTRIM(RTRIM(first_name)),
                    2,
                    LEN(LTRIM(RTRIM(first_name)))
                )),
                ' ',
                UPPER(LEFT(LTRIM(RTRIM(last_name)), 1)),
                LOWER(SUBSTRING(
                    LTRIM(RTRIM(last_name)),
                    2,
                    LEN(LTRIM(RTRIM(last_name)))
                ))
            )
        )),
        ''
    ) AS full_name,

    LOWER(NULLIF(LTRIM(RTRIM(email)), '')) AS email,
    NULLIF(LTRIM(RTRIM(phone)), '') AS phone,
    active,
    store_id,
    manager_id

FROM dbo.stg_staffs;
GO


CREATE OR ALTER VIEW dbo.vw_tr_brands
AS
SELECT DISTINCT
    brand_id,
    NULLIF(LTRIM(RTRIM(brand_name)), '') AS brand_name
FROM dbo.stg_brands
WHERE brand_id IS NOT NULL;
GO


CREATE OR ALTER VIEW dbo.vw_tr_categories
AS
SELECT DISTINCT
    category_id,
    NULLIF(LTRIM(RTRIM(category_name)), '') AS category_name
FROM dbo.stg_categories
WHERE category_id IS NOT NULL;
GO


CREATE OR ALTER VIEW dbo.vw_tr_products
AS
WITH cleaned_products AS
(
    SELECT
        product_id,
        NULLIF(LTRIM(RTRIM(product_name)), '') AS product_name,
        brand_id,
        category_id,
        model_year,
        list_price,

        ROW_NUMBER() OVER
        (
            PARTITION BY product_id
            ORDER BY product_id
        ) AS rn

    FROM dbo.stg_products
)
SELECT
    p.product_id,
    p.product_name,
    p.category_id,
    c.category_name,
    p.brand_id,
    b.brand_name,
    p.model_year,

    CASE
        WHEN p.list_price > 0
        THEN p.list_price
        ELSE NULL
    END AS list_price

FROM cleaned_products p

LEFT JOIN dbo.vw_tr_categories c
    ON p.category_id = c.category_id

LEFT JOIN dbo.vw_tr_brands b
    ON p.brand_id = b.brand_id

WHERE p.rn = 1;
GO


CREATE OR ALTER VIEW dbo.vw_tr_stores
AS
WITH cleaned_stores AS
(
    SELECT
        store_id,
        NULLIF(LTRIM(RTRIM(store_name)), '') AS store_name,
        NULLIF(LTRIM(RTRIM(street)), '') AS street,
        NULLIF(LTRIM(RTRIM(city)), '') AS city,
        UPPER(NULLIF(LTRIM(RTRIM(state)), '')) AS state,
        NULLIF(LTRIM(RTRIM(zip_code)), '') AS zip_code,
        ROW_NUMBER() OVER
        (
            PARTITION BY store_id
            ORDER BY store_id
        ) AS rn

    FROM dbo.stg_stores
)
SELECT
    store_id,
    store_name,
    street,
    city,
    state,
    zip_code
FROM cleaned_stores
WHERE rn = 1;
GO


CREATE OR ALTER VIEW dbo.vw_tr_orders
AS
WITH cleaned_orders AS
(
    SELECT
        order_id,
        customer_id,
        order_status,
        order_date,
        required_date,
        shipped_date,
        store_id,
        staff_id,

        ROW_NUMBER() OVER
        (
            PARTITION BY order_id
            ORDER BY order_id
        ) AS rn

    FROM dbo.stg_orders
)
SELECT
    order_id,
    customer_id,
    order_status,
    order_date,
    required_date,
    shipped_date,
    store_id,
    staff_id

FROM cleaned_orders

WHERE rn = 1
  AND
    (
        required_date IS NULL
        OR order_date IS NULL
        OR required_date >= order_date
    )
  AND
    (
        shipped_date IS NULL
        OR order_date IS NULL
        OR shipped_date >= order_date
    );
GO


CREATE OR ALTER VIEW dbo.vw_tr_order_items
AS
WITH cleaned_items AS
(
    SELECT
        order_id,
        item_id,
        product_id,
        quantity,
        list_price,
        discount,
        ROW_NUMBER() OVER
        (
            PARTITION BY order_id, item_id
            ORDER BY order_id, item_id
        ) AS rn

    FROM dbo.stg_order_items
)
SELECT
    order_id,
    item_id,
    product_id,
    quantity,
    list_price,
    discount

FROM cleaned_items

WHERE rn = 1
  AND quantity > 0
  AND list_price > 0
  AND discount BETWEEN 0 AND 1;
GO


