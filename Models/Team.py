import json


class Team:
    players: dict = {}
    name: str = None
    url: str = None

    def __init__(self, name: str, url: str, players: dict):
        self.name = name
        self.url = url
        self.players = players

    def toJson(self, dumps: bool = True):
        data: dict = {}
        data['name'] = self.name
        data['url'] = self.url
        data['players'] = []

        for player in self.players:
            data['players'].append(player.toJson(False))

        if dumps:
            return json.dumps(data)

        return data
