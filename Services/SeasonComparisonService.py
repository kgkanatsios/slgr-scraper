from Models.Team import Team
from Models.Game import Game

from Enums.GameResultEnum import GameResultEnum


class SeasonComparisonService:
    prev_season_team: Team
    current_season_games: list
    result: dict

    def __init__(self, prev_season_team: Team, current_season_games: list):
        self.prev_season_team = prev_season_team
        self.current_season_games = current_season_games

    def getComparison(self):
        self.result = []
        prev_season_players = self.prev_season_team.players
        for current_season_game in self.current_season_games:
            game_stats: dict = {}
            label = self.__getLabel(current_season_game)
            score_label = self.__getResultLabel(current_season_game).value

            game_stats['label'] = label
            game_stats['score_label'] = score_label

            squad = self.__getSquad(current_season_game)
            prev_season_players_in_game = []
            for player in squad:
                for prev_season_player in prev_season_players:
                    if prev_season_player.url == player.url:
                        prev_season_players_in_game.append(
                            player.toJson(False))
                        break

            game_stats['prev_season_players'] = prev_season_players_in_game
            game_stats['prev_season_players_num'] = len(
                prev_season_players_in_game)
            game_stats['prev_season_players_percent'] = self.__CalcPercent(
                len(squad), len(prev_season_players_in_game))
            self.result.append(game_stats)

        return self.result

    def __getLabel(self, game: Game) -> str:
        home_team: str = game.home_team
        opponent_name: str = game.home_team
        home_away_prefix: str = "(A)"
        if home_team in self.prev_season_team.name:
            opponent_name: str = game.guest_team
            home_away_prefix: str = "(H)"

        return str(home_away_prefix + " vs " + opponent_name + ": " + str(game.home_score) + ":" + str(game.guest_score))

    def __getSquad(self, game: Game) -> list:
        home_team: str = game.home_team
        if home_team in self.prev_season_team.name:
            return game.home_players

        return game.guest_players

    def __getResultLabel(self, game: Game) -> GameResultEnum:
        home_team: str = game.home_team

        if home_team in self.prev_season_team.name:
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

    def __CalcPercent(self, total: int, part: int):
        result: float = 0
        if (total == 0):
            return result

        result = (part * 100) / total

        return result
