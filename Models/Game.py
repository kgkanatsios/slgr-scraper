from ..Enums.GameResultEnum import GameResultEnum


class Game:
    players: dict = {}
    result: GameResultEnum = None
    name: str = None
    url: str = None

    def __init__(self, players: dict, result: GameResultEnum, name: str, url: str):
        self.name = name
        self.url = url
