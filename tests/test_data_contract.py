import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


EXPECTED_COLUMNS = {
    "customers.csv": ["customer_id", "first_name", "last_name", "phone", "email", "street", "city", "state", "zip_code"],
    "products.csv": ["product_id", "product_name", "brand_id", "category_id", "model_year", "list_price"],
    "brands.csv": ["brand_id", "brand_name"],
    "categories.csv": ["category_id", "category_name"],
    "orders.csv": ["order_id", "customer_id", "order_status", "order_date", "required_date", "shipped_date", "store_id", "staff_id"],
    "order_items.csv": ["order_id", "item_id", "product_id", "quantity", "list_price", "discount"],
    "staffs.csv": ["staff_id", "first_name", "last_name", "email", "phone", "active", "store_id", "manager_id"],
    "stores.csv": ["store_id", "store_name", "phone", "email", "street", "city", "state", "zip_code"],
}


class TestDataContract(unittest.TestCase):
    def read(self, filename: str) -> pd.DataFrame:
        return pd.read_csv(DATA / filename, na_values=["NULL", "null", "Null"])

    def test_all_source_files_exist(self):
        for filename in EXPECTED_COLUMNS:
            self.assertTrue((DATA / filename).is_file(), filename)

    def test_source_columns_match_staging_contract(self):
        for filename, expected in EXPECTED_COLUMNS.items():
            self.assertEqual(list(self.read(filename).columns), expected, filename)

    def test_business_keys_are_unique(self):
        for filename, key in (
            ("customers.csv", "customer_id"),
            ("products.csv", "product_id"),
            ("brands.csv", "brand_id"),
            ("categories.csv", "category_id"),
            ("orders.csv", "order_id"),
            ("stores.csv", "store_id"),
            ("staffs.csv", "staff_id"),
        ):
            df = self.read(filename)
            self.assertFalse(df[key].isna().any(), f"Null {key} in {filename}")
            self.assertFalse(df[key].duplicated().any(), f"Duplicate {key} in {filename}")

    def test_order_item_grain_is_unique(self):
        df = self.read("order_items.csv")
        self.assertFalse(df[["order_id", "item_id"]].duplicated().any())

    def test_customers_null_phone_is_normalized(self):
        df = self.read("customers.csv")
        self.assertTrue(df["phone"].isna().any())

    def test_order_item_measures_are_valid(self):
        df = self.read("order_items.csv")
        self.assertTrue((df["quantity"] > 0).all())
        self.assertTrue((df["list_price"] > 0).all())
        self.assertTrue(df["discount"].between(0, 1).all())

    def test_order_dates_are_consistent(self):
        df = self.read("orders.csv")
        for column in ("order_date", "required_date", "shipped_date"):
            df[column] = pd.to_datetime(df[column], errors="coerce")
        self.assertFalse(df["order_date"].isna().any())
        self.assertTrue((df["required_date"].isna() | (df["required_date"] >= df["order_date"])).all())
        self.assertTrue((df["shipped_date"].isna() | (df["shipped_date"] >= df["order_date"])).all())

    def test_referential_integrity(self):
        customers = set(self.read("customers.csv")["customer_id"])
        products = set(self.read("products.csv")["product_id"])
        brands = set(self.read("brands.csv")["brand_id"])
        categories = set(self.read("categories.csv")["category_id"])
        stores = set(self.read("stores.csv")["store_id"])
        staffs = set(self.read("staffs.csv")["staff_id"])
        orders = self.read("orders.csv")
        items = self.read("order_items.csv")
        product_rows = self.read("products.csv")

        self.assertTrue(set(orders["customer_id"]).issubset(customers))
        self.assertTrue(set(orders["store_id"]).issubset(stores))
        self.assertTrue(set(orders["staff_id"]).issubset(staffs))
        self.assertTrue(set(items["order_id"]).issubset(set(orders["order_id"])))
        self.assertTrue(set(items["product_id"]).issubset(products))
        self.assertTrue(set(product_rows["brand_id"]).issubset(brands))
        self.assertTrue(set(product_rows["category_id"]).issubset(categories))


if __name__ == "__main__":
    unittest.main()
