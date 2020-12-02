import os
import sqlite3
from typing import Callable, List, Dict, Tuple
from .schema import SCHEMA


def dict_factory(cur: sqlite3.Cursor, row: List) -> Dict:
    return {col[0]: row[i] for i, col in enumerate(cur.description)}


# Should rather use not nulls
def create_table_query(table_name: str, table_cols: List[str]) -> str:
    return f"CREATE TABLE {table_name} ({','.join(table_cols)})"


# Should rather use values and specify the rows
def insert_query(table_name: str, row: Dict) -> str:
    keys: str = ",".join(row.keys())
    values: str = ",".join(["?" for i in range(len(row))])
    return f"""INSERT INTO {table_name} ({keys}) VALUES ({values})"""


def insert_table(conn: sqlite3.Connection, table_name: str, rows: Dict):
    for row in rows:
        filtered_values = schema_values(table_name, row)
        query = (
            insert_query(table_name, filtered_values),
            list(filtered_values.values()),
        )
        conn.execute(*query)


def schema_values(table_name: str, row: Dict) -> Dict:
    schema: List = SCHEMA[table_name]
    available_cols: List = [i.split(" ")[0] for i in schema]
    return {k: row.get(k) for k in available_cols}


def truncate_table(conn: sqlite3.Connection, table_name: str):
    conn.execute(f"DROP TABLE {table_name}")
    conn.execute(create_table_query(table_name, SCHEMA[table_name]))


class Database:
    def __init__(self, db_name: str, bootstrap: bool = False):
        self._db_name = db_name
        # If an in memory db is used we need to keep a connection alive.
        if not os.path.exists(db_name):
            bootstrap = True
        elif bootstrap:
            os.remove(db_name)

        self._conn = sqlite3.connect(db_name)
        self.new_db = False
        if bootstrap:
            print("Bootstrapping...")
            self.bootstrap()
            self.new_db = True

    def __del__(self):
        "Commiting and removing the last connection."
        self._conn.commit()
        self._conn.close()

    def bootstrap(self):
        with sqlite3.connect(self._db_name) as conn:
            for table, schema in SCHEMA.items():
                conn.execute(create_table_query(table, schema))

    def get_latest_time_entries(
        self, start_time: str, row_factory: Callable = dict_factory
    ):
        with sqlite3.connect(self._db_name) as conn:
            conn.row_factory = dict_factory
            data = conn.execute(
                f"""
                SELECT start, duration, name
                FROM time_entries LEFT JOIN project ON pid=project.id
                WHERE DATE(start) > ? AND name IN (SELECT name FROM project_name);
                """,
                (start_time,),
            ).fetchall()
        return data

    def update_table(self, table: str, values: Dict) -> None:
        with sqlite3.connect(self._db_name) as conn:
            truncate_table(conn, table)
            insert_table(conn, table, values)
