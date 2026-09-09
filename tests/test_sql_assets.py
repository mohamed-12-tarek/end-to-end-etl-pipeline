import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SQL = ROOT / "sql"


class TestSQLAssets(unittest.TestCase):
    def read(self, filename: str) -> str:
        return (SQL / filename).read_text(encoding="utf-8")

    def test_required_sql_assets_exist(self):
        for filename in (
            "create_olap_schema.sql",
            "stage_tables.sql",
            "transformation_views.sql",
            "dim_date.sql",
        ):
            self.assertTrue((SQL / filename).is_file(), filename)

    def test_sql_is_split_into_go_batches(self):
        for filename in ("stage_tables.sql", "transformation_views.sql"):
            content = self.read(filename)
            self.assertRegex(content, r"(?im)^\s*GO\s*$", filename)

    def test_fact_grain_is_enforced(self):
        content = self.read("create_olap_schema.sql")
        self.assertIn("UQ_fact_sales_order_item UNIQUE (order_id, item_id)", content)

    def test_scd2_current_rows_are_unique(self):
        content = self.read("create_olap_schema.sql")
        self.assertIn("UX_dim_customer_current", content)
        self.assertIn("UX_dim_staff_current", content)
        self.assertIn("WHERE current_flag = 'Y'", content)

    def test_fact_resolves_scd2_as_of_order_date(self):
        content = (ROOT / "tasks" / "fact_table.py").read_text(encoding="utf-8")
        self.assertIn("o.order_date >= dc.start_date", content)
        self.assertIn("o.order_date <= dc.end_date", content)
        self.assertIn("o.order_date >= dsf.start_date", content)
        self.assertIn("o.order_date <= dsf.end_date", content)

    def test_sql_server_unsupported_index_syntax_is_absent(self):
        content = self.read("create_olap_schema.sql")
        self.assertIsNone(re.search(r"CREATE\s+INDEX\s+IF\s+NOT\s+EXISTS", content, re.I))


if __name__ == "__main__":
    unittest.main()
