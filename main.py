import typer
import json

from rich.progress import track

from Helpers.UrlHelper import getContentFromUrl
from Helpers.DomParserHelper import getFullTeam, getMatchdaysLinks, getGameLink, getFullGame
from Helpers.FileHelper import exportToFile, exportToJsonFile

from Services.SeasonComparisonService import SeasonComparisonService
from Services.PlayerResultsService import PlayerResultsService


def main(prev_season_squad_url: str = typer.Argument(..., help="Team's URL of the previous season squad. Example: https://www.slgr.gr/en/team/785/teamComp/20/"), current_season_schedule: str = typer.Argument(..., help="Team's URL of the current season schedule. Example: https://www.slgr.gr/en/teamschedule/845/21/222301/"), file_export: bool = typer.Option(False, "--export", help="Export data to JSON files")):
    prev_season_squad_html = getContentFromUrl(prev_season_squad_url)
    prev_season_team = getFullTeam(
        prev_season_squad_html, prev_season_squad_url)

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
        games.append(game)

    season_comparison = SeasonComparisonService(prev_season_team, games)
    season_comparison_result = season_comparison.getComparison()

    players_stats = PlayerResultsService(team_name, games)
    players_stats_result = players_stats.getPlayerResults()

    if file_export:
        exportToFile(team_name + "-games-squads",
                     json.dumps(list(map(lambda game: game.toJson(False), games))))
        exportToFile(prev_season_team, prev_season_team.toJson())
        exportToFile(team_name + "-season-comparison",
                     json.dumps(season_comparison_result))
        exportToJsonFile(team_name + "-player-results",
                         json.dumps(players_stats_result))


if __name__ == "__main__":
    typer.run(main)
