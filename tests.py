from datetime import datetime, timezone
import pytest  # type: ignore
import mock

from tw_lib.api import TimesheetAPI
from tw_lib.db import Database
from tw_lib.utils import group_by_date, parse_iso

# PUT: "https://toggl.com/api/v8/time_entries/{time_entry_id}/stop"


@pytest.fixture
def timesheet_api():
    return TimesheetAPI("mock-api-key")


@pytest.fixture
def db():
    return Database("file::memory:?cache=shared", bootstrap=True)


@pytest.fixture
def get_time_entries():
    def generator(*args, url, **kwargs):
        mock_response = mock.Mock()
        if url == "https://toggl.com/api/v8/time_entries":
            mock_response.ok = True
            mock_response.json.return_value = [
                {
                    "id": 1,
                    "pid": 1,
                    "start": "2020-05-08T08:05:50+00:00",
                    "duration": 3500,
                },
                {
                    "id": 2,
                    "pid": 1,
                    "start": "2020-05-08T13:05:50+00:00",
                    "duration": 1000,
                },
                {
                    "id": 3,
                    "pid": 2,
                    "start": "2020-05-08T13:05:50+00:00",
                    "duration": 684,
                },
                {
                    "id": 4,
                    "pid": 3,
                    "start": "2020-05-08T13:05:50+00:00",
                    "duration": 3600,
                },
            ]
        elif url == "https://toggl.com/api/v8/workspaces/1/projects":
            mock_response.ok = True
            mock_response.json.return_value = [
                {"id": 1, "wid": 1, "name": "Project | Task"},
                {"id": 2, "wid": 1, "name": "Project 2 | Task 2"},
                {"id": 3, "wid": 1, "name": "Invisible Project | Task"},
            ]
        else:
            mock_response.status_code = 404
            mock_response.ok = False
        return mock_response

    return generator


@pytest.fixture
def available_projects():
    return [
        {"id": 1, "name": "Project | Task"},
        {"id": 2, "name": "Something | else"},
        {"id": 3, "name": "Project 2 | Task 2"},
    ]


@pytest.fixture
def seeded_db(mocker, timesheet_api, db, get_time_entries, available_projects):
    mock_get = mocker.patch("requests.get")
    mock_get.side_effect = get_time_entries

    time_entries = timesheet_api.get_time_entries()
    project = timesheet_api.get_projects(1)

    db.update_table("time_entries", time_entries)
    db.update_table("project", project)
    db.update_table("project_name", available_projects)
    return db


@pytest.fixture
def toggl_stop_recording():
    def wrapper(running_task=True):
        def generator(*args, url, **kwargs):
            mock_response = mock.Mock()
            if url == "https://www.toggl.com/api/v8/time_entries/current":
                mock_response.ok = True
                mock_response.json.return_value = (
                    {"data": {"id": 1,}} if running_task else {"data": None}
                )
            elif url == "https://toggl.com/api/v8/time_entries/1/stop":
                mock_response.ok = True
                mock_response.json.return_value = {"data": None}
            return mock_response

        return generator

    return wrapper


def test_stopper_running_task(mocker, timesheet_api, toggl_stop_recording):
    mock_get = mocker.patch("requests.get")
    mock_get.side_effect = toggl_stop_recording(running_task=True)
    mock_put = mocker.patch("requests.put")
    mock_put.side_effect = toggl_stop_recording(running_task=True)
    assert timesheet_api.stop_running_entry() == {"data": None}


def test_stopper_no_running_task(mocker, timesheet_api, toggl_stop_recording):
    mock_get = mocker.patch("requests.get")
    mock_get.side_effect = toggl_stop_recording(running_task=False)
    mock_put = mocker.patch("requests.put")
    mock_put.side_effect = toggl_stop_recording(running_task=False)
    assert timesheet_api.stop_running_entry() == {"data": None}


def test_parse_iso():
    dt = datetime(year=2020, month=5, day=1).astimezone()
    assert parse_iso("2020-05-01") == dt
    assert parse_iso("2020-05-01T00:00:00") == dt
    assert parse_iso("2020-05-01T00:00:00+10:00") != dt
    with pytest.raises(ValueError):
        parse_iso("2020-05-1")


def test_timewriggler_round_to_nearest_half(seeded_db):
    latest_times = seeded_db.get_latest_time_entries("2020-05-01")
    grouped = group_by_date(latest_times, "%Y-%m-%d", True, 0.5)
    assert grouped == {
        "2020-05-08|Project|Task": ["2020-05-08", "Project", "Task", 1.5],
        "2020-05-08|Project 2|Task 2": ["2020-05-08", "Project 2", "Task 2", 0.5],
    }


def test_timewriggler_round_to_nearest_tenth(seeded_db):
    latest_times = seeded_db.get_latest_time_entries("2020-05-01")
    grouped = group_by_date(latest_times, "%Y-%m-%d", False, 0.1)
    assert grouped == {
        "2020-05-08|Project|Task": ["2020-05-08", "Project", "Task", 1.3],
        "2020-05-08|Project 2|Task 2": ["2020-05-08", "Project 2", "Task 2", 0.2],
    }


def test_timewriggler_test_time_filter(seeded_db):
    latest_times = seeded_db.get_latest_time_entries("2020-05-08")
    grouped = group_by_date(latest_times, "%Y-%m-%d", True, 0.5)
    assert grouped == {}


def test_timewriggler_test_grouper(seeded_db):
    latest_times = seeded_db.get_latest_time_entries("2020-05-01")
    grouped = group_by_date(latest_times, "%Y-%m-%d")
    assert grouped == {
        "2020-05-08|Project|Task": ["2020-05-08", "Project", "Task", 1.25],
        "2020-05-08|Project 2|Task 2": ["2020-05-08", "Project 2", "Task 2", 0.19],
    }
