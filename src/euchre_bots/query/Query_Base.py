# Query_Base.py
from euchre.Snapshot import Snapshot

from .Query_Stats import QueryStats


class QueryBase:
    def __init__(self, name):
        self.name = name
        self._stats = QueryStats()
        self._action = "no_action"
        self._data = None

    @property
    def stats(self):
        return self._stats

    @property
    def action(self):
        return self._action

    @property
    def data(self):
        return self._data

    def do(self, action, data=None):
        if not isinstance(action, str):
            raise TypeError(f"Expected str, found {type(action)}")
        self._action = action
        self._data = data
        return self

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

    def decide(self, _snap: Snapshot):
        raise NotImplementedError

    def playable(self, snap):
        return self.decide(snap).playable(snap)
