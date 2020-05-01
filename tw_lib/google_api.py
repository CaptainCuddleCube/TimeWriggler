import os
import pickle
from datetime import datetime
from itertools import product
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GoogleAPI:
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/spreadsheets",
    ]

    def __init__(
        self,
        spreadsheet_id,
        credentials_file,
        token_file,
        project_sheet="Projects!A5:B",
        time_sheet="timesheet!A2:D",
    ):
        self._project_sheet = project_sheet
        self._time_sheet = time_sheet
        self._credentails_file = credentials_file
        self._token_file = token_file
        self._sheet_id = spreadsheet_id
        self._creds = self._get_creds()

    def _get_creds(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self._token_file):
            with open(self._token_file, "rb") as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self._credentails_file, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self._token_file, "wb") as token:
                pickle.dump(creds, token)
        return creds

    def _run_get_query(self, range):
        service = build("sheets", "v4", credentials=self._creds)
        # Call the Sheets API
        sheet = service.spreadsheets()
        return sheet.values().get(spreadsheetId=self._sheet_id, range=range).execute()

    @property
    def projects(self):
        """
        get all the projects
        """
        result = self._run_get_query(range=self._project_sheet)
        projects = {"projects": [], "tasks": []}
        for i in result.get("values", []):
            if len(i) > 1:
                projects["tasks"].append(i[1])
            projects["projects"].append(i[0])
        return projects

    @property
    def available_projects(self):
        sheets_projects = self.projects
        return [
            {"id": i, "name": " | ".join(v)}
            for i, v in enumerate(
                product(sheets_projects["projects"], sheets_projects["tasks"])
            )
        ]

    def get_time_sheets(self):
        result = self._run_get_query(range="timesheet!A2:D")
        values = result.get("values", [])
        for i in values:
            i[0] = datetime.strptime(i[0], "%d %b %Y").isoformat()
        return values

    def append_to_time_sheets(self, data):
        """
        Append values to the timesheet
        """
        service = build("sheets", "v4", credentials=self._creds)
        body = {"range": self._time_sheet, "values": data}

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .append(
                spreadsheetId=self._sheet_id,
                range="timesheet!A2:D",
                body=body,
                valueInputOption="USER_ENTERED",
            )
            .execute()
        )
        return result.get("values", [])

    @property
    def last_entered_date(self):
        current_timesheets = self.get_time_sheets()
        return current_timesheets[-1][0]
