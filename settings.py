import os

dirname = os.path.dirname(__file__)

PORT = 80
TEMPLATE_PATH = os.path.join(dirname, "templates")
STATIC_PATH = os.path.join(dirname, "static")
STATIC_PREFIX = "/static/"
DEBUG = False
MAX_NUMBER_OF_SHIPS = 5
BOARD_SIZE = 300
NUMBER_OF_CELLS = 10
