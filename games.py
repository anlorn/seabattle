import random
import hashlib

from seabattle import game

games = {}


def new_game():
    """
    Creates new game and returns id for this game

    :rtype: `str`
    """
    while True:
        game_id = hashlib.md5(
            str(random.random()).encode()
        ).hexdigest()
        if game_id not in games:
            games[game_id] = game.GameSession()
            break
    return game_id


def del_game(game_id):
    """
    :type game_id: `str`
    """
    games.pop(game_id, None)


def get_game(game_id):
    """
    :rtype: `str` returns game with passed id or None if game doesn't exist
    """
    return games.get(game_id, None)
