import pandas as pd
from sqlalchemy import text

from config import get_engine


def read_view(view_name: str) -> pd.DataFrame:
    """Read a controlled analytics view into a DataFrame."""
    engine = get_engine()
    query = text(f"SELECT * FROM {view_name}")
    with engine.connect() as connection:
        return pd.read_sql(query, connection)
