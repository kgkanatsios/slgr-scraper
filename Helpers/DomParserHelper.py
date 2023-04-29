from bs4 import BeautifulSoup

from Models.Player import Player
from Models.Team import Team
from Models.Game import Game

from Constants import UrlConstants
from .StringHelper import *


def getFullTeam(html: str, url: str) -> Team:
    dom = htmlParser(html)

    players: list = getPlayers(dom)
    name: str = getTeamName(dom)
    season: str = getSeason(dom)

    return Team(name, season, url, players)


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


def getSeason(dom: BeautifulSoup) -> str:
    return sanitizeString(dom.find(
        'ul', class_='sf-filter').find(
        'div', class_='f16').string)


def getMatchdaysLinks(html: str) -> list:
    dom = htmlParser(html)

    team_name = getTeamName(dom)
    matchdays_urls_elements = dom.find(
        'ul', class_='sf-filter').find('ul', class_='sub-current').find_next('ul', class_='sub-current').find_all('a')

    urls = []

    for matchdays_urls_element in matchdays_urls_elements:
        urls.append(UrlConstants.BASE_URL +
                    matchdays_urls_element.get('href'))

    return team_name, urls


def getFullGame(html: str, url: str) -> Game:
    dom = htmlParser(html)

    home_team, guest_team = getGameTeams(dom)
    date: str = getGameDate(dom)
    matchday: str = getGameMatchday(dom)
    home_score, guest_score = getGameScore(dom)
    # players: list = getGamePlayers(dom)
    home_players: list = []
    guest_players: list = []

    return Game(home_team, guest_team, date, matchday, home_score, guest_score, home_players, guest_players, url)


def getGameTeams(dom: BeautifulSoup) -> tuple:
    return sanitizeString(dom.find(
        'div', class_='team').find(
        'div', class_='name').string), sanitizeString(dom.find(
            'div', class_='team').find_next(
            'div', class_='team').find(
            'div', class_='name').string)


def getGameDate(dom: BeautifulSoup) -> str:
    return sanitizeString(dom.find(
        'h2', class_='game-date').string)


def getGameMatchday(dom: BeautifulSoup) -> str:
    return sanitizeString(dom.find(
        'h3', class_='leg-name').string)


def getGameScore(dom: BeautifulSoup) -> tuple:
    home_score_element = dom.find(
        'span', class_='home-team-score')
    guest_score_element = dom.find(
        'span', class_='away-team-score')

    home_score = None
    guest_score = None
    if home_score_element is not None:
        home_score = int(sanitizeString(home_score_element.string))

    if guest_score_element is not None:
        guest_score = int(sanitizeString(guest_score_element.string))

    return home_score, guest_score


def getGamePlayers(dom: BeautifulSoup) -> list:
    return sanitizeString(dom.find(
        'ul', class_='sf-filter').find(
        'div', class_='f16').string)


def getGameLink(html: str) -> str:
    dom = htmlParser(html)
    a_element = dom.find('a', class_='d-inline-block text-right arrow-details')

    if a_element is not None:
        return UrlConstants.BASE_URL + a_element.get('href') + UrlConstants.GAME_SQUADS_PATH_SUFFIX
