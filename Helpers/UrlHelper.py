import requests


def getContentFromUrl(url: str):
    response = requests.get(url)
    return response.text
