# Greek Super League scraper

Get the following statistics from the [Official Greek Super League website](https://www.slgr.gr/en/) in JSON format:

1. All the games of the selected team.
2. Results per player for the selected team.
3. Comparison between the starting 11 players and the previous season's roster.


## Python Environment

1. Install [Python](https://www.python.org/).
2. Install [`virtualenv` tool](https://virtualenv.pypa.io/en/stable/): `pip install virtualenv`
3. Create the virtual environment: `python -m virtualenv venv`.
4. Activate the environment: `.\venv\Scripts\activate`.
5. Add libraries and create a `requirements.txt` file:
   1. This file can then be used by collaborators to update virtual environments using the following command: `pip install -r requirements.txt`.
   2. This command creates a file called `requirements.txt` that enumerates the installed packages: `pip freeze > requirements.txt`.
6. Deactivate the environment: `deactivate`.

## CLI Tool

1. Open a new terminal.
2. Execute: `python main.py`

### Demo

[![IMAGE ALT TEXT](https://img.youtube.com/vi/1v0rUf2yCV8/maxresdefault.jpg)](https://www.youtube.com/watch?v=1v0rUf2yCV8 "Web scraper for Greek Super League website")
