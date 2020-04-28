import sqlite3
from .schema import (
    PROJECT_SCHEMA,
    WORKSPACE_SCHEMA,
    TIME_ENTRIES_SCHEMA,
    PROJECT_NAME_SCHEMA,
)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Should rather use not nulls
def create_table_query(table_name, table_dict):
    create_table = f"CREATE TABLE {table_name} ("
    for k, v in table_dict.items():
        if k == "id":
            create_table += f"ID INT PRIMARY KEY NOT NULL "
        else:
            if type(v) == str:
                create_table += f", {k} TEXT"
            elif type(v) == int:
                create_table += f", {k} INT"
            elif type(v) == float:
                create_table += f", {k} REAL"
            elif type(v) == bool:
                create_table += f", {k} BOOL"
            else:
                create_table += f", {k} TEXT"
    create_table += ");"
    return create_table


# Should rather use values and specify the rows
def insert_query(table_name, row):
    keys = ",".join(row.keys())
    values = ",".join(["?" for i in range(len(row))])
    return f"""insert into {table_name} ({keys}) VALUES ({values})"""


def insert_table(conn, table_name, rows):
    for row in rows:
        query = insert_query(table_name, row), list(row.values())
        conn.execute(*query)


def bootstrap(db_name):
    conn = sqlite3.connect(db_name)
    conn.execute(create_table_query("workspace", WORKSPACE_SCHEMA))
    conn.execute(create_table_query("project", PROJECT_SCHEMA))
    conn.execute(create_table_query("time_entries", TIME_ENTRIES_SCHEMA))
    conn.execute(create_table_query("project_name", PROJECT_NAME_SCHEMA))
    conn.commit()
