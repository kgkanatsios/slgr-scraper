# Greek Super League scraper

## Python Environment

1. Install [Python](https://www.python.org/).
2. Install [`virtualenv` tool](https://virtualenv.pypa.io/en/stable/): `pip install virtualenv`
3. Create the virtual environment: `python -m virtualenv venv`.
4. Activate the environment: `.\venv\Scripts\activate`.
5. Add libraries and create a `requirements.txt` file:
   1. This command creates a file called `requirements.txt` that enumerates the installed packages: `pip freeze > requirements.txt`
   2. This file can then be used by collaborators to update virtual environments using the following command: `pip install -r requirements.txt`
6. Diactivate the environment: `deactivate`.

## CLI Tool

Examples: 

1. Stats for OLYMPIACOS F.C.: `python main.py https://www.slgr.gr/en/team/785/teamComp/20/ https://www.slgr.gr/en/teamschedule/845/21/222301/ --export`
2. Stats for A.E.K. F.C.: `python main.py https://www.slgr.gr/en/team/837/teamComp/20/ https://www.slgr.gr/en/teamschedule/837/21/222301/ --export`
3. Stats for PANATHINAIKOS F.C.: `python main.py https://www.slgr.gr/en/team/787/teamComp/20/ https://www.slgr.gr/en/teamschedule/847/21/222301/ --export`
4. Stats for P.A.O.K. F.C.: `python main.py https://www.slgr.gr/en/team/849/teamComp/20/ https://www.slgr.gr/en/teamschedule/849/21/222301/ --export` 
5. Stats for ARIS F.C.: `python main.py https://www.slgr.gr/en/team/838/teamComp/20/ https://www.slgr.gr/en/teamschedule/838/21/222301/ --export` 
