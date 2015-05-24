import random
import hashlib

import game

games = {}


def new_game():
    while True:
        game_id = hashlib.md5(
            str(random.random()).encode()
        ).hexdigest()
        if game_id not in games:
            games[game_id] = game.GameSession()
            break
    return game_id


def del_game(game_id):
    games.pop(game_id, None)


def get_game(game_id):
    return games.get(game_id, None)
