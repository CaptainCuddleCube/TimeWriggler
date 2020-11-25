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
        "What is your toggl API token?", type=str, default=toggl.get("api_token")
    )
    toggl["workspace"] = typer.prompt(
        "What workspace do you want tracked?", type=str, default=toggl.get("workspace")
    )
    config["toggl"] = toggl

    typer.echo("Now we need some of your google api information")
    google_api = CONFIG["google_api"] if "google_api" in CONFIG else {}
    google_api["spreadsheet_id"] = typer.prompt(
        "What is the sheet id?", type=str, default=google_api.get("spreadsheet_id")
    )
    google_api["credentials_file"] = typer.prompt(
        "where is the credentials file? eg: creds/credentials.json",
        type=str,
        default=google_api.get("credentials_file"),
    )
    google_api["token_file"] = typer.prompt(
        "where is the token file? eg: creds/token.pickle",
        type=str,
        default=google_api.get("token_file"),
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
        "What is the date format? Note; this is really important for parsring",
        type=str,
        default=google_api.get("date_format", "%Y-%m-%d"),
    )
    config["google_api"] = google_api
    typer.echo("\nThese are your current settings:")
    typer.echo(toml.dumps(config))
    if not typer.prompt(f"Are you happy with these settings?", type=bool):
        raise typer.Abort()
    with open(CONFIG_PATH, "w") as f:
        toml.dump(config, f)


@app.command()
def show_config():
    typer.echo(toml.dumps(CONFIG))


@app.command()
def set_date_format(date_fmt: str):
    CONFIG["google_api"]["date_format"] = date_fmt
    with open(CONFIG_PATH, "w") as f:
        toml.dump(CONFIG, f)


@app.command()
def set_sheet_id(sheet_id: str):
    CONFIG["google_api"]["spreadsheet_id"] = sheet_id
    with open(CONFIG_PATH, "w") as f:
        toml.dump(CONFIG, f)


if __name__ == "__main__":
    app()
