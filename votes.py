from collections import defaultdict

from menus.radio import PagedRadioMenu
from filters.players import PlayerIter

class SimpleVote(PagedRadioMenu):
    def __init__(self, vote_callback=None, **kwargs):
        self._select_callback = kwargs["select_callback"] if "select_callback" in kwargs else None
        kwargs["select_callback"] = SimpleVote.select
        super().__init__(**kwargs)
        if vote_callback is not None:
            self.vote_callback = vote_callback
        self.votes = defaultdict(int)
        self.sent = False
        self.players = []

    def select(self, player_index, choice):
        self.votes[choice] += 1
        self.players.remove(player_index)
        if len(self.players) == 0:
            self.vote_callback(self.get_winning_option())

    def get_winning_option(self):
        v = list(self.votes.values())
        k = list(self.votes.keys())
        return k[v.index(max(v))]

    def send(self, *ply_indexes):
        if self.sent:
            return

        if not ply_indexes:
            ply_indexes = PlayerIter('human')

        for player_index in ply_indexes:
            self.players.append(player_index)
            queue = self.get_user_queue(player_index)
            queue.append(self)
            queue._refresh()

        self.sent = True

