import player


class GameSession:

    _ready_players = 0
    _current_turn = None

    def __init__(self):
        self._players = []

    def new_player(self, to_client_func, on_game_end):
        """
        Creates new player and return it

        :param to_client_func: Func which will be called when player wants to send data to the client
        :type to_client_fund: `callable`

        :param on_game_end: Func which will be called when player wants to end the game
        :type on_game_end: `callable`

        :rtype: :class:`seabattle.player.Player` or None if game is full
        """
        if len(self._players) < 2:
            new_player = player.Player(len(self._players), self, to_client_func, on_game_end)
            self._players.append(new_player)
            return new_player

    def ready_for_begin(self, player):
        """
        Callback when player is ready to begin the battle
        """
        self._ready_players += 1
        if len(self._players) == 2 and self._ready_players == len(self._players):  # all players are ready
            self.next_turn()
        else:  # some player are not ready at this moment
            player.wait_other_player_ready()

    def fire(self, player, col, row):
        """
        Callback when active player do fire
        """
        passive_player = self._get_passive_player()
        fire_result = passive_player.enemy_fire(col, row)
        if fire_result:
            player.my_hit(col, row)
            if not passive_player.has_ships():
                player.win()
                passive_player.lost()
                self.finish_game()
        else:
            player.my_miss(col, row)
            self.next_turn()

    def player_disconnect(self, player):
        """
        When some player leave the game. We notify other players and finish game
        """
        for pl in self._all_players_except(player):
            pl.error_other_player_leave()
            pl.finish_game()
        self._players = []

    def finish_game(self):
        """
        When game is finished
        """
        for pl in self._players:
            pl.finish_game()
        self._players = []

    def next_turn(self):
        if self._current_turn is None:
            self._current_turn = 0
        else:
            self._current_turn += 1
        active_player = self._get_active_player()
        passive_player = self._get_passive_player()
        active_player.your_turn()
        passive_player.wait_other_player_turn()

    def _get_active_player(self):
        """
        Return player who can fire now
        """
        return self._players[self._current_turn % len(self._players)]

    def _get_passive_player(self):
        """
        Return player who can't fire now
        """
        return self._players[(self._current_turn + 1) % len(self._players)]

    def _all_players_except(self, except_player):
        for current_player in self._players:
            if current_player != except_player:
                yield current_player
        raise StopIteration
