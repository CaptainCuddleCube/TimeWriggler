import requests
from requests.auth import HTTPBasicAuth


class TimesheetAPI:
    def __init__(self, api_key):
        self._auth = HTTPBasicAuth(api_key, "api_token")
        self._headers = {"content-type": "application/json"}

    def get_time_entries(self, start_date=None, end_date=None):
        params = dict(start_date=start_date, end_date=end_date)
        return self.run_query(
            url="https://toggl.com/api/v8/time_entries", params=params,
        )

    def get_running_time_entry(self):
        return self.run_query(url="https://www.toggl.com/api/v8/time_entries/current")

    def stop_time_entry(self, time_entry_id):
        return self.run_query(
            url=f"https://toggl.com/api/v8/time_entries/{time_entry_id}/stop",
            type="PUT",
        )

    def stop_running_entry(self):
        running_entry = self.get_running_time_entry()
        if running_entry["data"]:
            return self.stop_time_entry(running_entry["data"]["id"])
        return {"data": None}

    def get_projects(self, workspace_id):
        return self.run_query(
            url=f"https://toggl.com/api/v8/workspaces/{workspace_id}/projects"
        )

    def get_workspaces(self):
        return self.run_query(url="https://toggl.com/api/v8/workspaces")

    def run_query(self, url, params=None, type="GET"):
        if type == "GET":
            resp = requests.get(
                url=url, params=params, auth=self._auth, headers=self._headers,
            )
        elif type == "PUT":
            resp = requests.put(
                url=url, params=params, auth=self._auth, headers=self._headers,
            )
        else:
            raise NotImplementedError("We haven't implemented this yet...")

        if not resp.ok:
            raise requests.exceptions.BaseHTTPError(
                f"Got status code: {resp.status_code}"
            )
        return resp.json()
