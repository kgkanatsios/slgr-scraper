import json

from Helpers.StringHelper import *


class Team:
    players: list = []
    name: str
    season: str
    url: str

    def __init__(self, name: str, season: str, url: str, players: list):
        self.name = name
        self.season = season
        self.url = url
        self.players = players

    def __str__(self) -> str:
        return f"{sanitizeString(convertToKebabCase(self.name))}-season-{sanitizeString(convertToKebabCase(self.season))}"

    def toJson(self, dumps: bool = True) -> (str | dict):
        data: dict = {}
        data["name"] = self.name
        data["season"] = self.season
        data["url"] = self.url
        data["players"] = []

        for player in self.players:
            data["players"].append(player.toJson(False))

        if dumps:
            return json.dumps(data)

        return data
