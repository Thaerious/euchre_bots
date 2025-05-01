# Bot_X4.py
from euchre import Snapshot
from ..query.Card_Selection_Set import CardSelectionSet as CSS
from ..ABotInterface import ABotInterface
from ..utility import allowed_suits

class Bot_X4(ABotInterface):
    def decide(self, snapshot: Snapshot) -> tuple[str, object]:
        """
        Returns a tuple of action and either a Card or a suit (str) depending on state.
        """
        fnname = f"state_{snapshot.state}"
        method = getattr(self, fnname)
        return method(snapshot)

    def state_1(self, snapshot: Snapshot):
        return("pass", None)

    def state_2(self, snapshot: Snapshot):
        return("down", None)

    def state_3(self, snapshot: Snapshot):
        return("pass", None)

    def state_4(self, snapshot: Snapshot):        
        suits = allowed_suits(snapshot.down_card.suit)
        counts = {suit: CSS(suit).size for suit in suits}
        max_suit = max(counts, key=counts.get)
        return("make", max_suit)

    def state_5(self, snapshot: Snapshot):
        lead = snapshot.tricks[-1].lead_suit
        css = CSS(snapshot.hand, trump=snapshot.trump).playable(lead)
        return("play", css.best())
