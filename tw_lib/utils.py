from datetime import datetime
from .db import insert_table, truncate_table
from math import ceil, isclose


def group_by_date(data, date_format, round_up=False):
    group_by_date = {}
    for entry in data:
        date = datetime.fromisoformat(entry["start"]).date().strftime(date_format)
        if date in group_by_date:
            group_by_date[date][-1] += entry["duration"] / 60 / 60
        else:
            project, task = entry["name"].split(" | ")
            group_by_date[date] = [date, project, task, entry["duration"] / 60 / 60]
    if round_up:
        for v in group_by_date.values():
            if isclose(v[-1], int(v[-1]), abs_tol=0.1):
                v[-1] = int(v[-1])
            else:
                v[-1] = ceil(v[-1])
    return group_by_date


def get_workspace_id(api, workspace_name):
    return [i for i in api.get_workspaces() if i["name"] == workspace_name][0]["id"]
