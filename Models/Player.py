import json


class Player:
    name: str
    url: str
    position: str

    def __init__(self, name: str, url: str, position: str):
        self.name = name
        self.url = url
        self.position = position

    def toJson(self, dumps: bool = True):
        data: dict = {}
        data["name"] = self.name
        data["url"] = self.url
        data["position"] = self.position

        if dumps:
            return json.dumps(data)

        return data
