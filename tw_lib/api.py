import requests
from requests.auth import HTTPBasicAuth


class TimesheetAPI:
    def __init__(self, api_key):
        self._auth = HTTPBasicAuth(api_key, "api_token")
        self._headers = {"content-type": "application/json"}

    def get_time_entries(self, start_time=None, end_time=None):
        params = dict(start_time=start_time, end_time=end_time)
        return self.run_query(
            url="https://toggl.com/api/v8/time_entries", params=params,
        )

    def get_projects(self, workspace_id):
        return self.run_query(
            url=f"https://toggl.com/api/v8/workspaces/{workspace_id}/projects"
        )

    def get_workspaces(self):
        return self.run_query(url="https://toggl.com/api/v8/workspaces")

    def run_query(self, url, params=None):
        resp = requests.get(
            url=url, params=params, auth=self._auth, headers=self._headers,
        )
        if not resp.ok:
            raise requests.exceptions.BaseHTTPError(
                f"Got status code: {resp.status_code}"
            )
        return resp.json()
