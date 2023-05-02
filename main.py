import typer
import json

import inquirer

from rich.progress import track, Progress, SpinnerColumn, TextColumn

from Helpers.UrlHelper import getContentFromUrl
from Helpers.DomParserHelper import getFullTeam, getMatchdaysLinks, getGameLink, getFullGame, getAllTeams, getTeamScheduleUrl, getTeamSquadUrl
from Helpers.FileHelper import exportToFile, exportToJsonFile

from Services.SeasonComparisonService import SeasonComparisonService
from Services.PlayerResultsService import PlayerResultsService

from Constants.UrlConstants import HOME_PAGE_URL


def main():
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Initializing...", total=None)
        home_page_html = getContentFromUrl(HOME_PAGE_URL)
        teams = getAllTeams(home_page_html)

    team_question = [
        inquirer.List('team',
                      message="Select the team:",
                      choices=teams.values(),
                      ),
    ]
    team_answer = inquirer.prompt(team_question)
    team = {key: value for (
        key, value) in teams.items() if value == team_answer['team']}
    team_url = list(team.keys())[0]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Get team's data...", total=None)
        team_html = getContentFromUrl(team_url)

        team_squad_url = getTeamSquadUrl(team_html)
        team_squad_html = getContentFromUrl(team_squad_url)
        team = getFullTeam(team_squad_html, team_squad_url)

        team_schedule_url = getTeamScheduleUrl(team_html)
        team_schedule_html = getContentFromUrl(team_schedule_url)
        team_name, matchdays_urls = getMatchdaysLinks(team_schedule_html)

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

    service_question = [
        inquirer.Checkbox(
            "services",
            message="What are you interested in?",
            choices=[("All the games", "all_games"), ("Results per player", "player_results"),
                     ("Compare squad with previous season", "season_comparison")],
            default=["all_games", "player_results"],
        ),
    ]
    service_answer = inquirer.prompt(service_question)

    if "all_games" in service_answer["services"]:
        exportToFile(team_name + "-games-squads",
                     json.dumps(list(map(lambda game: game.toJson(False), games))))

    if "player_results" in service_answer["services"]:
        players_stats = PlayerResultsService(team, games)
        players_stats_result = players_stats.getPlayerResults()
        exportToJsonFile(team_name + "-player-results",
                         json.dumps(players_stats_result))

    return
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
