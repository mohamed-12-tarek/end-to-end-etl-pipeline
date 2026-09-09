# End-to-End ETL Pipeline

A production-style batch ETL and analytics project built around a SQL Server data warehouse. The pipeline demonstrates how raw CSV sources can be ingested, staged, transformed, modeled into an OLAP layer, and exposed through reusable analytics views and a Streamlit dashboard.

## Project Overview

This project implements an end-to-end data engineering workflow:

```text
CSV Sources
    ↓
Real Staging
    ↓
Transformation Views
    ↓
Core / OLAP Data Warehouse
    ↓
Dimensions + Fact Table
    ↓
Analytics Views
    ↓
Streamlit Dashboard
```

The orchestration layer is implemented with Prefect, data loading uses Pandas, database access uses SQLAlchemy + ODBC Driver 18, and the warehouse runs on Microsoft SQL Server.

## Architecture

### 1. Source Layer

The project uses CSV files as the source system. The source data represents a bike-store transactional domain and is treated as an external operational source.

### 2. Staging Layer

Raw source records are loaded into real SQL Server staging tables before transformation. Each staging table mirrors the corresponding source structure and provides a controlled landing area for the ETL process.

### 3. Transformation Layer

SQL Server views are used to prepare and standardize staged data before loading the warehouse. Transformations include joins, data preparation, business-key handling, and calculations required by downstream warehouse loads.

### 4. Core / OLAP Layer

The warehouse uses dimensional modeling with separate dimension and fact tables.

#### Dimensions

| Dimension | Strategy | Purpose |
|---|---|---|
| `dim_customer` | SCD Type 2 | Preserve customer history |
| `dim_staff` | SCD Type 2 | Preserve staff history |
| `dim_product` | SCD Type 1 | Maintain the current product state |
| `dim_store` | SCD Type 1 | Maintain the current store state |
| `dim_date` | Static date dimension | Provide reusable calendar attributes |

#### Fact Table

`fact_sales` stores sales transactions at the following grain:

> **One row per `(order_id, item_id)`**

The fact table contains the measures and foreign keys required for analytical queries.

## Slowly Changing Dimensions

The project demonstrates both major dimension-maintenance strategies used in the warehouse:

### SCD Type 1

Used for dimensions where historical attribute versions are not required. Existing records are updated in place.

Implemented for:

- `dim_product`
- `dim_store`

### SCD Type 2

Used when historical versions must be preserved. The pipeline maintains effective dates and current-version information so that historical warehouse records can be associated with the correct dimension version.

Implemented for:

- `dim_customer`
- `dim_staff`

Because the source files do not provide a reliable change timestamp, the pipeline uses the ETL load date as the effective date for detected changes.

## ETL Pipeline

The main Prefect flow is defined in `flow.py`.

The pipeline performs the following operations:

1. Create the warehouse schema and required OLAP objects.
2. Create staging tables.
3. Create transformation views.
4. Load source CSV files into real staging tables.
5. Populate the date dimension.
6. Apply SCD Type 2 processing to customer and staff dimensions.
7. Apply SCD Type 1 processing to product and store dimensions.
8. Rebuild the sales fact table.
9. Execute analytics SQL views.

Each major operation is implemented as a task or reusable database operation, with Prefect providing orchestration, logging, and retry behavior.

## Analytics Layer

The analytics layer contains reusable SQL Server views designed for business analysis rather than raw warehouse access.

Current analytics views include:

- Sales overview
- Sales by store
- Sales by product
- Sales by category
- Sales by staff
- Monthly sales
- Product performance
- Sales summary / KPI metrics

The dashboard consumes these views instead of embedding analytical SQL directly in the Streamlit application.

## Dashboard

The project includes a Streamlit dashboard organized around business areas and stakeholder questions.

```text
Stakeholder Question
        ↓
Analytics View
        ↓
Pandas DataFrame
        ↓
Visualization
        ↓
Business Insight
```

Dashboard areas include:

- Overview
- Sales
- Products
- Stores
- Staff

The dashboard is intentionally separated from the ETL and warehouse logic so that the presentation layer can evolve independently.

## Data Quality & Testing

The project includes database-independent tests covering important ETL and warehouse rules, including:

- Source schema validation
- Business-key uniqueness
- Fact-table grain
- NULL handling
- Measure ranges
- Date consistency
- Referential integrity
- Critical SQL rules
- SCD Type 2 logic

Run the test suite with:

```bash
python -m unittest discover -s tests -v
```

Compile-check the Python project with:

```bash
python -m compileall -q .
```

GitHub Actions is configured to run the automated checks on repository changes.

## Tech Stack

| Technology | Role |
|---|---|
| Python 3.14+ | ETL application and orchestration code |
| Pandas | CSV ingestion and tabular processing |
| Prefect | Workflow orchestration, retries, and logging |
| SQL Server | Staging, warehouse, transformations, and analytics |
| SQLAlchemy | Python database connectivity |
| pyodbc | SQL Server ODBC connectivity |
| ODBC Driver 18 | SQL Server database driver |
| Streamlit | Analytics dashboard |
| Matplotlib / Seaborn | Data visualization |
| unittest | Automated testing |
| GitHub Actions | Continuous integration |

## Project Structure

```text
end-to-end-etl-pipeline/
├── data/                       # Source CSV files
├── sql/
│   ├── analytics/              # Business-ready analytics views
│   ├── create_olap_schema.sql  # Warehouse schema and core objects
│   ├── stage_tables.sql        # Staging table definitions
│   ├── transformation_views.sql# Transformation layer
│   └── dim_date.sql            # Date dimension population
├── tasks/
│   ├── fact_table.py           # Fact table loading
│   ├── scd_type1.py             # SCD Type 1 processing
│   └── scd_type2.py             # SCD Type 2 processing
├── dashboard/
│   ├── app.py                  # Streamlit application
│   ├── charts.py               # Chart rendering
│   ├── database.py             # Analytics view access
│   ├── insights.py             # Business insight generation
│   ├── questions.py             # Stakeholder question configuration
│   └── utils.py                # Dashboard utilities
├── tests/                      # Data and ETL tests
├── config.py                   # Shared database configuration
├── flow.py                     # Prefect ETL flow
├── pyproject.toml              # Project metadata and dependencies
├── .env.example                # Environment variable template
└── README.md
```

## Setup

### Prerequisites

- Python 3.14 or later
- Microsoft SQL Server
- Microsoft ODBC Driver 18 for SQL Server
- A target SQL Server database

### Installation

Clone the repository and install the project dependencies:

```bash
git clone https://github.com/mohamed-12-tarek/end-to-end-etl-pipeline.git
cd end-to-end-etl-pipeline
pip install -e .
```

Alternatively, if you use `uv`:

```bash
uv sync
```

### Environment Variables

Copy the environment template:

```bash
cp .env.example .env
```

Configure the database connection values in `.env`:

```text
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=1433
DB_NAME=your_database
```

Do not commit `.env` or database credentials to source control.

## Running the Pipeline

Run the Prefect ETL flow from the repository root:

```bash
python flow.py
```

The flow is responsible for building and loading the warehouse and preparing the analytics layer.

## Running the Dashboard

After the warehouse and analytics views have been populated, start Streamlit with:

```bash
streamlit run dashboard/app.py
```

The dashboard reads the reusable analytics views from SQL Server through the shared database configuration.

## Batch Processing Design

This project currently follows a batch full-reload design.

The source files do not expose a reliable CDC mechanism or watermark column such as `updated_at`. Therefore, the pipeline does not attempt to infer incremental changes from source files.

A production incremental version could introduce:

- Source-side `updated_at` timestamps
- CDC or change tracking
- Watermark management
- Incremental staging
- MERGE/upsert-based fact and dimension loading
- Pipeline metadata and audit tables

## Design Principles

The project follows several data engineering principles:

- Separate ingestion, transformation, warehouse, and presentation layers.
- Keep business logic in reusable SQL views and warehouse transformations.
- Define and preserve fact-table grain explicitly.
- Use SCD Type 1 and Type 2 according to business-history requirements.
- Centralize database configuration.
- Make ETL operations observable through Prefect logging and retries.
- Validate important data and modeling rules through automated tests.
- Keep dashboard presentation logic separate from ETL logic.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
