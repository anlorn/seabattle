"""
Contains various actions which can be sent through websocket
"""
from seabattle import resources


def paint_cell(board, color, col, row):
    return (resources.PAINT_ACTION, board, color, col, row,)


def set_text(text):
    return (resources.SET_TEXT_ACTION, text, )
