# Bot_3A1.py
from euchre import Snapshot
from euchre.card import SUITS
from ..query.Card_Selection_Set import CardSelectionSet as CSS
from ..query import played
from ..ABotInterface import ABotInterface
from ..utility import allowed_suits
from .Bot_3 import Bot_3

def short_suits(hand):
    return sum(1 for s in SUITS if (hand & CSS(s)).size > 1)

class Bot_3A1(Bot_3):
    def __init__(self):
        self.param = [0, 3, 3, 0]
