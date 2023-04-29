import typer
import json

from rich import print
from rich.progress import track

from Helpers.UrlHelper import getContentFromUrl
from Helpers.StringHelper import filenameFormater
from Helpers.DomParserHelper import getFullTeam, getMatchdaysLinks, getGameLink, getFullGame

from Constants import LocalFoldersConstants


def main(prev_season_squad_url: str = typer.Argument(..., help="Team's URL of the previous season squad. Example: https://www.slgr.gr/en/team/785/teamComp/20/"), current_season_schedule: str = typer.Argument(..., help="Team's URL of the current season schedule. Example: https://www.slgr.gr/en/teamschedule/845/21/222301/")):
    prev_season_squad_html = getContentFromUrl(prev_season_squad_url)
    prev_season_team = getFullTeam(
        prev_season_squad_html, prev_season_squad_url)

    with open(LocalFoldersConstants.EXPORTS_FOLDER + str(prev_season_team) + ".json", "w") as outfile:
        outfile.write(prev_season_team.toJson())

    current_season_schedule_html = getContentFromUrl(current_season_schedule)
    team_name, matchdays_urls = getMatchdaysLinks(current_season_schedule_html)

    game_urls = []
    for matchdays_url in track(matchdays_urls, description="Fetching game urls..."):
        matchday_html = getContentFromUrl(matchdays_url)
        game_link = getGameLink(matchday_html)
        if game_link is not None:
            game_urls.append(game_link)

    games = []
    for game_url in track(game_urls, description="Fetching squads..."):
        game_html = getContentFromUrl(game_url)
        game = getFullGame(game_html, game_url)
        games.append(game.toJson(False))

    with open(LocalFoldersConstants.EXPORTS_FOLDER + filenameFormater(team_name) + "-games-squads.json", "w") as outfile:
        outfile.write(json.dumps(games))


if __name__ == "__main__":
    typer.run(main)
