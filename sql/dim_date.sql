IF NOT EXISTS (SELECT 1 FROM dbo.dim_date)
BEGIN

    WITH DateGenerator AS
    (
        SELECT CAST('2000-01-01' AS DATE) AS full_date

        UNION ALL

        SELECT DATEADD(DAY, 1, full_date)
        FROM DateGenerator
        WHERE full_date < '2050-12-31'
    )
    INSERT INTO dbo.dim_date
    (
        date_sk,
        full_date,
        day,
        month,
        month_name,
        quarter,
        year,
        weekday_name
    )
    SELECT
        CAST(
            CONVERT(VARCHAR(4), YEAR(full_date)) +
            RIGHT('00' + CONVERT(VARCHAR(2), MONTH(full_date)), 2) +
            RIGHT('00' + CONVERT(VARCHAR(2), DAY(full_date)), 2)
            AS INT
        ) AS date_sk,
        full_date,
        DAY(full_date),
        MONTH(full_date),
        DATENAME(MONTH, full_date),
        DATEPART(QUARTER, full_date),
        YEAR(full_date),
        DATENAME(WEEKDAY, full_date)
    FROM DateGenerator
    OPTION (MAXRECURSION 0);

END;