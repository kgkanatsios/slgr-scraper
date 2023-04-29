import typer
from rich import print

from Helpers.UrlHelper import getContentFromUrl
from Helpers.DomParserHelper import htmlParser, getPlayers, getTeamName

from Models.Team import Team


def main(prev_season_squad_url: str = typer.Argument(..., help="Team's URL of the previous season squad. Example: https://www.slgr.gr/en/team/785/teamComp/20/"), current_season_schedule: str = typer.Argument(..., help="Team's URL of the current season schedule. Example: https://www.slgr.gr/en/teamschedule/845/21/222301/")):
    prev_season_squad_html = getContentFromUrl(prev_season_squad_url)
    prev_season_squad_dom = htmlParser(prev_season_squad_html)

    players: list = getPlayers(prev_season_squad_dom)
    team_name: str = getTeamName(prev_season_squad_dom)
    prev_season_team = Team(team_name, prev_season_squad_url, players)


if __name__ == "__main__":
    typer.run(main)
