import json
import sys

import tornado.web
import tornado.websocket
import tornado.autoreload
import tornado.httpserver

import games
if len(sys.argv) == 2 and sys.argv[1] == "debug":
    import settings_dev as settings
else:
    import settings
import resources


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", IndexPageHandler,),
            tornado.web.URLSpec(r"/join/([0-9a-f]{32})/", IndexPageHandler, name="join_handler"),
            tornado.web.URLSpec(r"/game/([0-9a-f]{32})/", GameHandler, name="game_handler")
        ]
        app_settings = {
            "template_path": settings.TEMPLATE_PATH,
            "static_path": settings.STATIC_PATH,
            "static_url_prefix": settings.STATIC_PREFIX,
            "debug": settings.DEBUG
        }
        super(Application, self).__init__(handlers, **app_settings)


class IndexPageHandler(tornado.web.RequestHandler):
    """
    Just handle main game page
    """
    def get(self, game_id=None):
        if game_id is None:
            game_id = games.new_game()
            join_link = "%s://%s%s" % (
                self.request.protocol,
                self.request.host,
                self.reverse_url("join_handler", game_id)
            )
        else:
            join_link = None
        websocket_url = "ws://%s%s" % (
            self.request.host,
            self.reverse_url("game_handler", game_id)
        )
        macroses = {
            "socket": websocket_url,
            "join_link": join_link,
            "settings": settings,
            "resources": resources,
            "board_size": settings.BOARD_SIZE,
            "number_of_ships": settings.MAX_NUMBER_OF_SHIPS
        }
        self.render("index.html", **macroses)


class GameHandler(tornado.websocket.WebSocketHandler):

    def open(self, game_id):
        game = games.get_game(game_id)
        self.player = game.new_player(self.to_client, self.end_connection)
        self.game_id = game_id

    def on_message(self, data):
        self.player.from_client(json.loads(data))

    def to_client(self, action):
        self.write_message(json.dumps(action))

    def end_connection(self):
        self.close()

    def on_close(self):
        if self.player:
            games.del_game(self.game_id)
            self.player.disconnect()
            self.player = None
            self.game_id = None


def main():
    application = Application()
    server = tornado.httpserver.HTTPServer(application)
    server.listen(settings.PORT)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
