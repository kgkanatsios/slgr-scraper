from bs4 import BeautifulSoup

from Models.Player import Player
from Constants import UrlConstants
from .Sanitizer import *


def htmlParser(html: str):
    return BeautifulSoup(html, "html.parser")


def getPlayers(dom: BeautifulSoup) -> list:
    dom_elements = dom.find_all(
        'div', class_='item-team')

    players: list = []

    for dom_element in dom_elements:
        name = dom_element.find(
            'div', class_='player-name').string
        url = UrlConstants.BASE_URL + dom_element.a.get('href')
        position = dom_element.find(
            'div', class_='player-position').string

        player = Player(sanitizeString(name), sanitizeString(
            url), sanitizeString(position))
        players.append(player)

    return players


def getTeamName(dom: BeautifulSoup) -> str:
    return sanitizeString(dom.find(
        'div', class_='top-background-img').find(
        'img', class_='logo-title').parent.text)
