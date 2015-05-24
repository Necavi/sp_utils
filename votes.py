import random

from copy import deepcopy
from collections import defaultdict

from menus.radio import PagedRadioMenu, SimpleRadioMenu, SimpleRadioOption
from filters.players import PlayerIter

class SimplePagedVote(PagedRadioMenu):
    def __init__(self, vote_callback=None, revote_on_tie=True, **kwargs):
        self._select_callback = kwargs["select_callback"] if "select_callback" in kwargs else None
        kwargs["select_callback"] = SimplePagedVote.select
        self.revote_on_tie = revote_on_tie
        super().__init__(**kwargs)
        if vote_callback is not None:
            self.vote_callback = vote_callback
        self.votes = defaultdict(int)
        self.sent = False
        self.players = []
        self.remaining_players = []

    def select(self, player_index, choice):
        print(choice.text)
        self.votes[choice] += 1
        self.remaining_players.remove(player_index)
        if len(self.remaining_players) == 0:
            winning_options = self.get_winning_options()
            if len(winning_options) == 1:
                self.vote_callback(winning_options[0])
            else:
                if self.revote_on_tie:
                    self.clear()
                    self.extend(winning_options)
                    self.sent = False
                    self.send(self.players)
                    self.revote_on_tie = False
                else:
                    self.vote_callback(random.choice(winning_options))

        if self._select_callback is not None:
            self._select_callback(self, player_index, choice)

    def get_winning_options(self):
        max_value = 0
        max_keys = []

        for k, v in self.votes.items():
            if v >= max_value:
                if v > max_value:
                    max_value = v
                    max_keys = [k]
                else:
                    max_keys.append(k)
        return max_keys

    def send(self, *ply_indexes):
        if self.sent:
            return

        if not ply_indexes:
            ply_indexes = PlayerIter('human')

        for player_index in ply_indexes:
            self.players.append(player_index)
            self.remaining_players.extend(self.players)
            queue = self.get_user_queue(player_index)
            queue.append(self)
            queue._refresh()

        self.sent = True

class SimpleRadioVote(SimpleRadioMenu):
    def __init__(self, title=None, vote_callback=None, revote_on_tie=True, **kwargs):
        self._select_callback = kwargs["select_callback"] if "select_callback" in kwargs else None
        kwargs["select_callback"] = SimpleRadioVote.select
        self.revote_on_tie = revote_on_tie
        super().__init__(**kwargs)
        if title is not None:
            self.insert(0, title)
        if vote_callback is not None:
            self.vote_callback = vote_callback
        self.sent = False
        self.votes = defaultdict(int)
        self.players = set()
        self.remaining_players = set()

    def select(self, player_index, choice):
        print(choice.text)
        self.votes[choice] += 1
        self.remaining_players.remove(player_index)
        if len(self.remaining_players) == 0:
            print("Vote over")
            winning_options = self.get_winning_options()
            if len(winning_options) == 1:
                self.vote_callback(winning_options[0])
            else:
                if self.revote_on_tie:
                    self.clear()
                    self.extend([SimpleRadioOption(i + 1, winning_options[i].text) for i in range(0, len(winning_options))])
                    self.insert(0, "Tie Breaker")
                    self.sent = False
                    self.revote_on_tie = False
                    self.send(*self.players)
                else:
                    self.vote_callback(random.choice(winning_options))

        if self._select_callback is not None:
            self._select_callback(self, player_index, choice)

    def get_winning_options(self):
        max_value = 0
        max_keys = []

        for k, v in self.votes.items():
            if v >= max_value:
                if v > max_value:
                    max_value = v
                    max_keys = [k]
                else:
                    max_keys.append(k)
        print(max_value)
        print(str([key.text for key in max_keys]))
        return max_keys

    def send(self, *ply_indexes):
        if self.sent:
            return

        if not ply_indexes:
            ply_indexes = PlayerIter('human')

        self.votes = defaultdict(int)
        self.players = set()
        self.remaining_players = set()

        for player_index in ply_indexes:
            self.players.add(player_index)
            self.remaining_players.update(deepcopy(self.players))
            queue = self.get_user_queue(player_index)
            queue.append(self)
            queue._refresh()

        self.sent = True
