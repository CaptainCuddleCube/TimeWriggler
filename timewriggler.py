#! /usr/bin/env python3

import os
import argparse
import toml

from tw_lib.api import TimesheetAPI
from tw_lib.db import Database
from tw_lib.google_api import GoogleAPI
from tw_lib.utils import group_by_date, get_workspace_id

parser = argparse.ArgumentParser(
    description="TimeWriggler - your one stop time-sheeter"
)

parser.add_argument(
    "--update_projects",
    action="store_true",
    default=False,
    help="If you have made any changes to your toggl projects, use this command.",
)

parser.add_argument(
    "--bootstrap",
    action="store_true",
    default=False,
    help="Want to start from scratch? This will trash the local database.",
)

parser.add_argument(
    "--dry_run",
    default=False,
    action="store_true",
    help="Not sure this will work? Check out what will be uploaded!",
)

parser.add_argument(
    "--preserve_time_entries",
    default=False,
    action="store_true",
    help="While testing, you might just want to use the system's internal state for time entries.",
)

parser.add_argument(
    "--round_up",
    default=False,
    action="store_true",
    help="This will ceiling the values, unless they are really close to the hour.",
)

parser.add_argument(
    "--config",
    default="config.toml",
    help="If you want to store your config somewhere else.",
)

args = parser.parse_args()

settings = toml.load(args.config)
SQLITE_DB = settings["local"]["sqlite_db"]
TOGGL = settings["toggl"]
GOOGLE_SETTINGS = settings["google_api"]
WORKSPACE = TOGGL["workspace"]


api = TimesheetAPI(TOGGL["api_token"])
g_api = GoogleAPI(**GOOGLE_SETTINGS)
db = Database(SQLITE_DB)

if args.bootstrap:
    os.remove(f"./{SQLITE_DB}")

if not os.path.exists(f"./{SQLITE_DB}"):
    print("Bootstrapping...")
    db.bootstrap()
    db.update_table("time_entries", api.get_time_entries())
    db.update_table("project", api.get_projects(get_workspace_id(api, WORKSPACE)))
    db.update_table("project_name", g_api.available_projects)
else:
    if not args.preserve_time_entries:
        print("Updating the time entries...")
        db.update_table("time_entries", api.get_time_entries())
    if args.update_projects:
        print("Updating the projects...")
        db.update_table("project", api.get_projects(get_workspace_id(api, WORKSPACE)))
        db.update_table("project_name", g_api.available_projects)

print("Thumbing your Toggl timesheets into google sheet format...")
grouped = group_by_date(
    db.get_latest_time_entries(g_api.last_entered_date), args.round_up
)
published_values = list(grouped.values())

if args.dry_run:
    print("Dry run results:")
    print(published_values)
elif len(published_values) > 0:
    print(f"Sending times for days: {list(grouped.keys())}")
    g_api.append_to_time_sheets(published_values)
    print("Sent!")
else:
    print("No new timesheets available, you should probably do some work.")
