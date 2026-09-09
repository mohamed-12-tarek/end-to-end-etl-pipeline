import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine


load_dotenv()

REQUIRED_ENV = ("DB_USER", "DB_PASSWORD", "DB_HOST", "DB_NAME")

def get_engine() -> Engine:
    """Create the SQL Server engine from environment variables."""
    missing = [name for name in REQUIRED_ENV if not os.getenv(name)]
    if missing:
        raise RuntimeError(
            "Missing required database environment variables: "
            + ", ".join(missing)
        )

    connection_url = URL.create(
        "mssql+pyodbc",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.getenv("DB_PORT", "1433")),
        database=os.environ["DB_NAME"],
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "Encrypt": "yes",
            "TrustServerCertificate": "yes",
        },
    )

    return create_engine(
        connection_url,
        fast_executemany=True,
        pool_pre_ping=True,
        pool_recycle=1800,
    )
