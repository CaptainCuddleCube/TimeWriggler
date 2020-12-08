import typer
import toml

from .constants import CONFIG_PATH

CONFIG = toml.load(CONFIG_PATH)


app = typer.Typer(help="allows you to setup your config")


@app.command()
def run_setup():
    config = {}
    typer.echo("Welcome to the setup guide, this will help build your config!\n")
    typer.echo(
        "This config will use the existing config you have, and everything "
        "is saved to ~/.timewriggle/config.toml \n\n"
    )
    typer.echo("First, we will need some toggl information")
    toggl = CONFIG["toggl"] if "toggl" in CONFIG else {}
    toggl["api_token"] = typer.prompt(
        "What is your toggl API token? "
        "(Toggle -> Reports -> Profile Settings -> API Token)",
        type=str, default=toggl.get("api_token")
    )
    toggl["workspace"] = typer.prompt(
        "What workspace do you want tracked?", type=str, default=toggl.get("workspace")
    )
    config["toggl"] = toggl

    typer.echo("Now we need some of your google api information")
    google_api = CONFIG["google_api"] if "google_api" in CONFIG else {}
    google_api["spreadsheet_id"] = typer.prompt(
        "What is the Google sheet id to write to? "
        "(eg: https://docs.google.com/spreadsheets/d/<sheet_id>/edit)",
        type=str, default=google_api.get("spreadsheet_id")
    )
    google_api["credentials_file"] = typer.prompt(
        "Where is the credentials file?",
        type=str,
        default=google_api.get("credentials_file", "creds/credentials.json"),
    )
    google_api["token_file"] = typer.prompt(
        "Where should the token file be persisted?",
        type=str,
        default=google_api.get("token_file", "creds/token.py"),
    )
    google_api["project_sheet"] = typer.prompt(
        "Where are the project sheets? (the default should work 99% of the time)",
        type=str,
        default=google_api.get("project_sheet", "Projects!A4:B"),
    )
    google_api["time_sheet"] = typer.prompt(
        "Where are the time sheets? (the default should work 99% of the time)",
        type=str,
        default=google_api.get("time_sheet", "timesheet!A2:D"),
    )
    google_api["date_format"] = typer.prompt(
        "What is the date format? Note: this is really important for parsing",
        type=str,
        default=google_api.get("date_format", "%Y-%m-%d"),
    )
    config["google_api"] = google_api
    typer.echo("\nThese are your current settings:")
    typer.echo(toml.dumps(config))
    typer.confirm("Are you happy with these settings?", abort=True)
    with open(CONFIG_PATH, "w") as file:
        toml.dump(config, file)


@app.command()
def show_config():
    typer.echo(toml.dumps(CONFIG))


@app.command()
def set_date_format(date_fmt: str):
    CONFIG["google_api"]["date_format"] = date_fmt
    with open(CONFIG_PATH, "w") as file:
        toml.dump(CONFIG, file)


@app.command()
def set_sheet_id(sheet_id: str):
    CONFIG["google_api"]["spreadsheet_id"] = sheet_id
    with open(CONFIG_PATH, "w") as file:
        toml.dump(CONFIG, file)


if __name__ == "__main__":
    app()
