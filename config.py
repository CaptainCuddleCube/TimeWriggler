import typer
import toml

app = typer.Typer(name="TimeWriggler")


@app.command()
def config(setting: str = typer.Option(None)):
    print(setting)


if __name__ == "__main__":
    app()

