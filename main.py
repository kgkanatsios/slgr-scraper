import typer
import json

import inquirer

from rich.progress import track, Progress, SpinnerColumn, TextColumn

from Helpers.UrlHelper import getContentFromUrl
from Helpers.DomParserHelper import getFullTeam, getMatchdaysLinks, getGameLink, getFullGame, getAllTeams, getTeamScheduleUrl, getTeamSquadUrl, getTeamSeasons
from Helpers.FileHelper import exportToFile

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
    for matchdays_url in track(matchdays_urls, description="Fetching games..."):
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
                     ("Compare starting 11 players with a previous season's roster", "season_comparison")],
            default=[],
        ),
    ]
    service_answer = inquirer.prompt(service_question)

    if "all_games" in service_answer["services"]:
        exportToFile(team_name + "-games-squads",
                     json.dumps(list(map(lambda game: game.toJson(False), games))))

    if "player_results" in service_answer["services"]:
        players_stats = PlayerResultsService(team, games)
        players_stats_result = players_stats.getPlayerResults()
        exportToFile(team_name + "-player-results",
                     json.dumps(players_stats_result))

    if "season_comparison" in service_answer["services"]:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description="Getting previous seasons...", total=None)
            team_html = getContentFromUrl(team_url)
            seasons = getTeamSeasons(team_html)

        season_question = [
            inquirer.List('season',
                          message="Select the season to compare:",
                          choices=seasons.values(),
                          ),
        ]
        season_answer = inquirer.prompt(season_question)
        season = {key: value for (
            key, value) in seasons.items() if value == season_answer['season']}
        season_url = list(season.keys())[0]
        season_label = list(season.values())[0]

        season_squad_html = getContentFromUrl(season_url)
        season_team = getFullTeam(season_squad_html, season_url)

        season_comparison = SeasonComparisonService(season_team, games)
        season_comparison_result = season_comparison.getComparison()

        exportToFile(team_name + "-season-comparison-vs-" + season_label,
                     json.dumps(season_comparison_result))


if __name__ == "__main__":
    typer.run(main)
