from pathlib import Path

CONFIG_BASE_PATH = Path.home() / ".timewriggler"

# Ensure that the base bath exists
if not CONFIG_BASE_PATH.exists():
    CONFIG_BASE_PATH.mkdir()

CONFIG_PATH = CONFIG_BASE_PATH / "config.toml"
if not CONFIG_PATH.exists():
    CONFIG_PATH.touch()
