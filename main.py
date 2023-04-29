import typer


def main(prev_season_squad: str = typer.Argument(..., help="Team's URL of the previous season squad. Example: https://www.slgr.gr/el/team/785/teamComp/20/"), current_season_schedule: str = typer.Argument(..., help="Team's URL of the current season schedule. Example: https://www.slgr.gr/el/teamschedule/845/21/222301/")):
    pass


if __name__ == "__main__":
    typer.run(main)
