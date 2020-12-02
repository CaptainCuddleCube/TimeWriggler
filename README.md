# TimeWriggler

Welcome to TimeWriggler - the squirmiest way to wiggle and warp your Toggl time
into Google sheets.

_Works on the streets, freak in the sheets._

## Testimonials

"Wow! It worked just like that?" - _Ashton: core developer_

"It's really basic and needs a lot of work." - _Ashton: core developer_

"You probably should use this with caution, I haven't tested it a whole lot." - _Ashton: core developer_

"That is the best README!! 😂 hahaha nice man" - _Seem: core developer's friend_

"That's nice sweetie." - _core developer's mom_

## How to use

### Requirements

- Python3, and I've only tested it with python3.7, so, ja, good luck.
- A computer.
- An internet connection.
- A Toggl [account](https://toggl.com/) (it is free, you cheapskate).
- pip install requirements using `pip install -r requirements/base.txt`.

### Setting up your Toggl projects

The way TimeWriggler works, is it expects you to name your Toggl project `<google-sheets project> | <google-sheets task>`.
It's important that you have the project and the task separated by a space-pipe-space, ie: `|`.

If your `project | task` do not feature in the google sheet - **they will not be included in the upload.**

### Getting Google application settings

To use TimeWriggler, you will need to setup a Google API Project, and get yourself a `credentials.json`,
which you can create [here](https://console.developers.google.com/flows/enableapi?apiid=appsactivity&credential=client_key), or via the [express-route](https://developers.google.com/sheets/api/quickstart/python) (recommended).
Keep that `credentials.json` super safe - like the `creds/` directory (which is git ignored for your convenience).

### Installing

You can install TimeWriggler straight into your terminal using:
```
pip install git+https://github.com/CaptainCuddleCube/TimeWriggler.git
```

If everything is installed and ready, just use `timewriggler --help` to start.

### Configuration

TimeWriggler has a nice and friendly `configure` subcommand to help you set up things.

```
timewriggler configure run-setup
```


### Updating timesheet

Once you are all configured, just run `timewriggler update-timesheet --help`, and you can see your favourite settings to get it to run for your
snowflake case:
```
timewriggler update-timesheet --help
Usage: timewriggler update-timesheet [OPTIONS]

  Friendly command to help you update your sheets

Options:
  --start-date TEXT
  --dry-run / --no-dry-run    [default: False]
  --round-to-nearest FLOAT
  --round-up / --no-round-up  [default: False]
  --help                      Show this message and exit.
```

example:

```
timewriggler update-timesheet --round-to-nearest 0.25 --round-up --start-date 2020-11-30 --dry-run
```
