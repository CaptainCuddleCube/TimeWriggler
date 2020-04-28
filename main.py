import os
import sqlite3
from itertools import product
from datetime import datetime
from lib.api import TimesheetAPI
from lib.db import bootstrap, insert_table, dict_factory, create_table_query
from lib.google_api import GoogleAPI
import toml

settings = toml.load("config.toml")
SQLITE_DB = settings["local"]["sqlite_db"]

api = TimesheetAPI(settings["toggl"]["api_token"])
g_api = GoogleAPI(
    settings["google_api"]["spreadsheet_id"],
    settings["google_api"]["credentials_file"],
    settings["google_api"]["token_file"],
)


if settings["local"]["bootstrap"] or not os.path.exists(f"./{SQLITE_DB}"):
    print("Bootstrapping")
    if os.path.exists(f"./{SQLITE_DB}"):
        os.remove(f"{SQLITE_DB}")

    bootstrap(SQLITE_DB)
    conn = sqlite3.connect(SQLITE_DB)
    selected_workspace = settings["toggl"]["WORKSPACE"]
    workspace = [i for i in api.get_workspaces() if i["name"] == selected_workspace][0]
    print("getting time entries")
    projects = api.get_projects(workspace["id"])
    print("inserting projects")
    insert_table(conn, "project", projects)

    print("getting time entries")
    time_entries = api.get_time_entries()
    print("inserting time entries")
    insert_table(conn, "time_entries", time_entries)

    sheets_projects = g_api.get_projects()

    available_projects = [
        {"id": i, "name": " | ".join(v)}
        for i, v in enumerate(
            product(sheets_projects["projects"], sheets_projects["tasks"])
        )
    ]
    insert_table(conn, "project_name", available_projects)

    conn.commit()

conn = sqlite3.connect(SQLITE_DB)
conn.row_factory = dict_factory

current_timesheets = g_api.get_time_sheets()
last_entry = current_timesheets[-1]


data = conn.execute(
    f"""
    SELECT start, duration, name
    FROM time_entries LEFT JOIN project ON pid=project.id
    WHERE DATE(start) > ? AND name IN (SELECT name FROM project_name);
    """,
    (last_entry[0],),
).fetchall()


def group_by_date(data):
    group_by_date = {}
    for entry in data:
        date = datetime.fromisoformat(entry["start"]).date().strftime("%d %b %Y")
        if date in group_by_date:
            group_by_date[date][-1] += entry["duration"] / 60 / 60
        else:
            project, task = entry["name"].split(" | ")
            group_by_date[date] = [date, project, task, entry["duration"] / 60 / 60]
    return group_by_date


grouped = group_by_date(data)

published_values = [v for k, v in grouped.items()]
if len(published_values) > 0:
    print(f"Sending times for {grouped.keys()}")
    g_api.append_to_time_sheets(published_values)
else:
    print("No new timesheets available.")
