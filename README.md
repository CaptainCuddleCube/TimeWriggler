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
- A Toggl [account](https://toggl.com/) (it's are free you cheapskate).

### Setting up your Toggl projects

The way TimeWriggler works, is it expects you to name your Toggl project `<google-sheets project> | <google-sheets task>`.
It's important that you have the project and the task separated by a space-pipe-space, ie: `|`.

If your `project | task` do not feature in the google sheet - **they will not be included in the upload.**

### Getting Google application settings

To use TimeWriggler, you will need to setup a Google API Project, and get yourself a `credentials.json`,
which you can create [here](https://console.developers.google.com/flows/enableapi?apiid=appsactivity&credential=client_key).
Keep that `credentials.json` super safe - like the `creds/` directory (which is git ignored for your convenience).

### Configuration

TimeWriggler uses TOML for its configuration, and you can see an example of this in `example.config.toml`. Once you have
all the values needed to run your config - just rename it to `config.toml` and you will be good to go.

By default, you should just leave the sqlite3 db as an in-memory database - that way is should clean itself up when done.
If, however, you have a massive number of projects, or you want to persist things, then opt to use a stored database.

### Running

Once you are all configured, just run `./timewriggler.py`, and you can add your favourite settings to get it to run for your
snowflake case:

```
usage: timewriggler.py [-h] [--update_projects] [--bootstrap] [--dry_run]
                       [--preserve_time_entries] [--round_up]
                       [--config CONFIG]

TimeWriggler - sheet out of Toggl into Google sheets.

optional arguments:
  -h, --help            show this help message and exit
  --update_projects     If you have made any changes to your toggl projects,
                        use this command.
  --bootstrap           Want to start from scratch? This will trash the local
                        database.
  --dry_run             Not sure this will work? Check out what will be
                        uploaded!
  --preserve_time_entries
                        While testing, you might just want to use the system's
                        internal state for time entries.
  --round_up            This will ceiling the values, unless they are really
                        close to the hour.
  --config CONFIG       If you want to store your config somewhere else.
```
