#! /usr/bin/env python3

import argparse
import os
import toml
from pathlib import Path

import typer

from .tw_lib.api import TimesheetAPI
from .tw_lib.db import Database
from .tw_lib.google_api import GoogleAPI
from .tw_lib.utils import group_by_date, get_workspace_id, parse_iso
from .constants import CONFIG_PATH
from .config import app as config_app


settings = toml.load(CONFIG_PATH)
TOGGL = settings["toggl"]
GOOGLE_SETTINGS = settings["google_api"]
WORKSPACE = TOGGL["workspace"]


app = typer.Typer(help="TimeWriggler - Helping you sheet Toggl into Google.")
app.add_typer(config_app, name="configure")


@app.command(help="Friendly command to help you upload your sheets")
def upload(
    start_date: str = typer.Option(None),
    dry_run: bool = typer.Option(False),
    round_to_nearest: float = typer.Option(None),
    round_up: bool = typer.Option(False),
):
    api = TimesheetAPI(TOGGL["api_token"])
    g_api = GoogleAPI(**GOOGLE_SETTINGS)
    db = Database("file::memory:?cache=shared", bootstrap=True)
    parsed_start = parse_iso(start_date).isoformat() if start_date else None
    workspaces = [i["name"] for i in api.get_workspaces()]
    if WORKSPACE not in workspaces:
        typer.echo(
            f"The workspace {WORKSPACE} does not exist, the options are:{workspaces}"
        )
        raise typer.Abort()
    typer.echo("Stopping running entries...")
    api.stop_running_entry()
    typer.echo("Updating the time entries...")
    db.update_table("time_entries", api.get_time_entries(start_date=parsed_start))
    typer.echo("Updating the projects...")
    db.update_table("project", api.get_projects(get_workspace_id(api, WORKSPACE)))
    db.update_table("project_name", g_api.available_projects)

    typer.echo("Thumbing your Toggl timesheets into google sheet format...")

    insert_time = parse_iso(
        g_api.last_entered_date(default_datetime=parse_iso(parsed_start))
    )

    grouped = group_by_date(
        db.get_latest_time_entries(insert_time),
        settings["google_api"]["date_format"],
        round_up,
        round_to_nearest,
    )
    published_values = list(grouped.values())

    if dry_run:
        typer.echo("Dry run results:")
        typer.echo(published_values)
    elif len(published_values) > 0:
        typer.echo(f"Sending times for days: {list(grouped.keys())}")
        g_api.append_to_time_sheets(published_values)
        typer.echo("Sent!")
    else:
        typer.echo("No new timesheets available, you should probably do some work.")


if __name__ == "__main__":
    app()
