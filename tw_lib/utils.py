from datetime import datetime
from .db import insert_table, truncate_table
from math import ceil, isclose


def ceil_to_nearest(value, nearest):
    return ceil(value / nearest) * nearest


def group_by_date(data, date_format, round_up=False, round_to_nearest=None):
    group_by_date = {}
    for entry in data:
        date = datetime.fromisoformat(entry["start"]).date().strftime(date_format)
        project, task = entry["name"].split(" | ")
        if f"{date}|{project}|{task}" in group_by_date and entry["duration"] > 0:
            group_by_date[f"{date}|{project}|{task}"][-1] += entry["duration"] / 60 / 60
        elif entry["duration"] > 0:
            project, task = entry["name"].split(" | ")
            group_by_date[f"{date}|{project}|{task}"] = [
                date,
                project,
                task,
                entry["duration"] / 60 / 60,
            ]
    round_to_nearest = 1 if round_up and round_to_nearest is None else round_to_nearest

    if round_to_nearest is not None:
        for v in group_by_date.values():
            if isclose(v[-1], int(v[-1]), abs_tol=0.1):
                v[-1] = int(v[-1])
            else:
                v[-1] = ceil_to_nearest(v[-1], round_to_nearest)
    return group_by_date


def get_workspace_id(api, workspace_name):
    return [i for i in api.get_workspaces() if i["name"] == workspace_name][0]["id"]


def parse_iso(iso_date):
    if iso_date is None:
        return None
    return datetime.fromisoformat(iso_date).astimezone()
