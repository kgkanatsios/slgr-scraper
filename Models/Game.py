import json


class Game:
    home_team: str
    home_team_url: str
    guest_team: str
    guest_team_url: str
    date: str
    matchday: str
    home_score: int
    guest_score: int
    home_players: list = []
    guest_players: list = []
    url: str

    def __init__(self, home_team: str, home_team_url: str, guest_team: str, guest_team_url: str, date: str, matchday: str, home_score: int, guest_score: int, home_players: list, guest_players: list, url: str):
        self.home_team = home_team
        self.home_team_url = home_team_url
        self.guest_team = guest_team
        self.guest_team_url = guest_team_url
        self.date = date
        self.matchday = matchday
        self.home_score = home_score
        self.guest_score = guest_score
        self.home_players = home_players
        self.guest_players = guest_players
        self.url = url

    def getGameSummary(self):
        return str(self.home_team + " vs " + self.guest_team + ": " + str(self.home_score) + ":" + str(self.guest_score))

    def toJson(self, dumps: bool = True):
        data: dict = {}
        data["home_team"] = self.home_team
        data["home_team_url"] = self.home_team_url
        data["guest_team"] = self.guest_team
        data["guest_team_url"] = self.guest_team_url
        data["date"] = self.date
        data["matchday"] = self.matchday
        data["home_score"] = self.home_score
        data["guest_score"] = self.guest_score
        data["url"] = self.url
        data["home_players"] = []
        data["guest_players"] = []

        for home_player in self.home_players:
            data["home_players"].append(home_player.toJson(False))

        for guest_player in self.guest_players:
            data["guest_players"].append(guest_player.toJson(False))

        if dumps:
            return json.dumps(data)

        return data
