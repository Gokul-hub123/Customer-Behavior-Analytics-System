from __future__ import annotations

import sqlite3
from pathlib import Path

from backend.config import BASE_DIR, USE_MYSQL

DB_PATH = BASE_DIR / "customer_behavior.db"


def get_sqlite_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def get_mysql_connection():
    if not USE_MYSQL:
        raise RuntimeError("MySQL is disabled in the current configuration.")

    import mysql.connector

    conn = mysql.connector.connect(
        host=BASE_DIR.parent.as_posix() if False else None,
        user=None,
        password=None,
        database=None,
    )
    return conn


def init_db():
    try:
        if USE_MYSQL:
            import mysql.connector
            from backend.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

            conn = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                autocommit=True,
            )
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id VARCHAR(100) PRIMARY KEY,
                    customer_name VARCHAR(150),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id VARCHAR(100) PRIMARY KEY,
                    product_name VARCHAR(200),
                    category VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id VARCHAR(100) PRIMARY KEY,
                    customer_id VARCHAR(100),
                    product_id VARCHAR(100),
                    transaction_date DATE,
                    quantity DOUBLE,
                    unit_price DOUBLE,
                    total_amount DOUBLE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS customer_segments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_id VARCHAR(100),
                    recency DOUBLE,
                    frequency DOUBLE,
                    monetary DOUBLE,
                    cluster INT,
                    cluster_label VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS forecasts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    forecast_month VARCHAR(50),
                    predicted_sales DOUBLE,
                    model_name VARCHAR(100),
                    mae DOUBLE,
                    rmse DOUBLE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.close()
            return
    except Exception:
        pass

    conn = get_sqlite_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            customer_name TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            customer_id TEXT,
            product_id TEXT,
            transaction_date TEXT,
            quantity REAL,
            unit_price REAL,
            total_amount REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS customer_segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            recency REAL,
            frequency REAL,
            monetary REAL,
            cluster INTEGER,
            cluster_label TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            forecast_month TEXT,
            predicted_sales REAL,
            model_name TEXT,
            mae REAL,
            rmse REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def save_current_dataset(df):
    if df is not None and not df.empty:
        df.to_csv(BASE_DIR / "data/current_dataset.csv", index=False)


def load_current_dataset():
    path = BASE_DIR / "data/current_dataset.csv"
    if path.exists():
        import pandas as pd

        return pd.read_csv(path)
    return None


def save_cleaned_dataset(df):
    if df is not None and not df.empty:
        df.to_csv(BASE_DIR / "data/cleaned_dataset.csv", index=False)


def load_cleaned_dataset():
    path = BASE_DIR / "data/cleaned_dataset.csv"
    if path.exists():
        import pandas as pd

        return pd.read_csv(path)
    return None


def save_segments(df):
    if df is not None and not df.empty:
        df.to_csv(BASE_DIR / "data/segments.csv", index=False)
        _store_segments_in_db(df)


def load_segments():
    path = BASE_DIR / "data/segments.csv"
    if path.exists():
        import pandas as pd

        return pd.read_csv(path)
    return None


def save_forecast(df):
    if df is not None and not df.empty:
        df.to_csv(BASE_DIR / "data/forecast.csv", index=False)
        _store_forecast_in_db(df)


def load_forecast():
    path = BASE_DIR / "data/forecast.csv"
    if path.exists():
        import pandas as pd

        return pd.read_csv(path)
    return None


def _store_segments_in_db(df):
    if df is None or df.empty:
        return

    try:
        if USE_MYSQL:
            import mysql.connector
            from backend.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

            conn = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                autocommit=True,
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customer_segments")
            for _, row in df.iterrows():
                cursor.execute(
                    """
                    INSERT INTO customer_segments (customer_id, recency, frequency, monetary, cluster, cluster_label)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        str(row.get("customer_id", "")),
                        float(row.get("recency", 0)),
                        float(row.get("frequency", 0)),
                        float(row.get("monetary", 0)),
                        int(row.get("cluster", 0)),
                        str(row.get("cluster_label", "")),
                    ),
                )
            conn.close()
            return
    except Exception:
        pass

    conn = get_sqlite_connection()
    conn.execute("DELETE FROM customer_segments")
    for _, row in df.iterrows():
        conn.execute(
            """
            INSERT INTO customer_segments (customer_id, recency, frequency, monetary, cluster, cluster_label)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                str(row.get("customer_id", "")),
                float(row.get("recency", 0)),
                float(row.get("frequency", 0)),
                float(row.get("monetary", 0)),
                int(row.get("cluster", 0)),
                str(row.get("cluster_label", "")),
            ),
        )
    conn.commit()
    conn.close()


def _store_forecast_in_db(df):
    if df is None or df.empty:
        return

    try:
        if USE_MYSQL:
            import mysql.connector
            from backend.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

            conn = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                autocommit=True,
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM forecasts")
            for _, row in df.iterrows():
                cursor.execute(
                    """
                    INSERT INTO forecasts (forecast_month, predicted_sales, model_name, mae, rmse)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        str(row.get("forecast_month", "")),
                        float(row.get("predicted_sales", 0)),
                        "Linear Regression",
                        float(row.get("mae", 0)),
                        float(row.get("rmse", 0)),
                    ),
                )
            conn.close()
            return
    except Exception:
        pass

    conn = get_sqlite_connection()
    conn.execute("DELETE FROM forecasts")
    for _, row in df.iterrows():
        conn.execute(
            """
            INSERT INTO forecasts (forecast_month, predicted_sales, model_name, mae, rmse)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(row.get("forecast_month", "")),
                float(row.get("predicted_sales", 0)),
                "Linear Regression",
                float(row.get("mae", 0)),
                float(row.get("rmse", 0)),
            ),
        )
    conn.commit()
    conn.close()


def store_dataset_in_db(df):
    if df is None or df.empty:
        return

    try:
        if USE_MYSQL:
            import mysql.connector
            from backend.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

            conn = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                autocommit=True,
            )
            cursor = conn.cursor()

            cursor.execute("DELETE FROM transactions")
            cursor.execute("DELETE FROM products")
            cursor.execute("DELETE FROM customers")

            for _, row in df.iterrows():
                customer_id = str(row.get("customer_id", ""))
                product_id = str(row.get("product_id", row.get("product_name", "P000")))
                product_name = str(row.get("product_name", product_id))
                category = str(row.get("category", "General"))
                cursor.execute(
                    """
                    INSERT INTO customers (customer_id, customer_name) VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE customer_name = VALUES(customer_name)
                    """,
                    (customer_id, customer_id),
                )
                cursor.execute(
                    """
                    INSERT INTO products (product_id, product_name, category) VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE product_name = VALUES(product_name), category = VALUES(category)
                    """,
                    (product_id, product_name, category),
                )
                cursor.execute(
                    """
                    INSERT INTO transactions (transaction_id, customer_id, product_id, transaction_date, quantity, unit_price, total_amount)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE customer_id = VALUES(customer_id), product_id = VALUES(product_id),
                    transaction_date = VALUES(transaction_date), quantity = VALUES(quantity), unit_price = VALUES(unit_price), total_amount = VALUES(total_amount)
                    """,
                    (
                        str(row.get("transaction_id", f"TXN_{customer_id}_{product_id}_{len(df)}")),
                        customer_id,
                        product_id,
                        str(row.get("date", "2024-01-01"))[:10],
                        float(row.get("quantity", 0)),
                        float(row.get("unit_price", 0)),
                        float(row.get("total_amount", 0)),
                    ),
                )
            conn.close()
            return
    except Exception:
        pass

    conn = get_sqlite_connection()
    conn.execute("DELETE FROM transactions")
    conn.execute("DELETE FROM products")
    conn.execute("DELETE FROM customers")
    for _, row in df.iterrows():
        customer_id = str(row.get("customer_id", ""))
        product_id = str(row.get("product_id", row.get("product_name", "P000")))
        product_name = str(row.get("product_name", product_id))
        category = str(row.get("category", "General"))
        conn.execute(
            "INSERT OR REPLACE INTO customers (customer_id, customer_name) VALUES (?, ?)",
            (customer_id, customer_id),
        )
        conn.execute(
            "INSERT OR REPLACE INTO products (product_id, product_name, category) VALUES (?, ?, ?)",
            (product_id, product_name, category),
        )
        conn.execute(
            "INSERT OR REPLACE INTO transactions (transaction_id, customer_id, product_id, transaction_date, quantity, unit_price, total_amount) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                str(row.get("transaction_id", f"TXN_{customer_id}_{product_id}_{len(df)}")),
                customer_id,
                product_id,
                str(row.get("date", "2024-01-01"))[:10],
                float(row.get("quantity", 0)),
                float(row.get("unit_price", 0)),
                float(row.get("total_amount", 0)),
            ),
        )
    conn.commit()
    conn.close()
