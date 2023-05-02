from Models.Game import Game
from Models.Team import Team

from Enums.GameResultEnum import GameResultEnum


class PlayerResultsService:
    team: Team
    current_season_games: list
    result: dict

    def __init__(self, team: Team, current_season_games: list):
        self.team = team
        self.current_season_games = current_season_games

    def getPlayerResults(self):
        self.result = {}
        for current_season_game in self.current_season_games:
            label = self.__getLabel(current_season_game)
            score_label = self.__getResultLabel(current_season_game).value

            squad = self.__getSquad(current_season_game)
            for player in squad:
                stats: dict = {}
                if player.url not in self.result.keys():
                    self.result[player.url]: list = []

                stats["name"] = player.name
                stats["label"] = label
                stats["score_label"] = score_label

                self.result[player.url].append(stats)

        return self.result

    def __getLabel(self, game: Game) -> str:
        opponent_name: str = game.home_team
        home_away_prefix: str = "(A)"
        if game.home_team_url in self.team.url:
            opponent_name: str = game.guest_team
            home_away_prefix: str = "(H)"

        return str(home_away_prefix + " vs " + opponent_name + ": " + str(game.home_score) + ":" + str(game.guest_score))

    def __getSquad(self, game: Game) -> list:
        if game.home_team_url in self.team.url:
            return game.home_players

        return game.guest_players

    def __getResultLabel(self, game: Game) -> GameResultEnum:
        if game.home_team_url in self.team.url:
            my_score: int = game.home_score
            opponent_score: int = game.guest_score
        else:
            my_score: int = game.guest_score
            opponent_score: int = game.home_score

        if (my_score == opponent_score):
            return GameResultEnum.DRAW

        if (my_score > opponent_score):
            return GameResultEnum.WIN

        return GameResultEnum.LOSE
