# Bot_1A1.py
from euchre import Snapshot
from euchre.card import SUITS
from ..query.Card_Selection_Set import CardSelectionSet as CSS
from ..query import played
from ..ABotInterface import ABotInterface
from ..utility import allowed_suits
import inspect

# A simple bot that follows preset rules
# Performs a little worse that 1A2

class Bot_1A1(ABotInterface):
    def decide(self, snap: Snapshot) -> tuple[str, object]:
        """
        Returns a tuple of action and either a Card or a suit (str) depending on state.
        """        
        fnname = f"state_{snap.state}"
        method = getattr(self, fnname)
        tuple = method(snap)
        return tuple

    def state_1(self, snap: Snapshot):
        if snap.dealer.index == snap.for_index:
            test = CSS("JLAKQ♠", trump="♠")
            hand = CSS(snap.hand, trump=snap.up_card.suit).normalize("♠")
            hand.select(snap.up_card)
            eval = test & hand
            if eval.size >= 2: return self.return_action("order", None)
        else:
            test = CSS("JLAKQ♠", trump="♠")
            hand = CSS(snap.hand, trump=snap.up_card.suit).normalize("♠")
            eval = test & hand
            if eval.size >= 2: return self.return_action("order", None)

        return self.return_action("pass", None)

    def state_2(self, snap: Snapshot):
        hand = CSS(snap.hand, trump=snap.up_card.suit)
        hand.select(snap.up_card)
        if hand.worst() == (str)(snap.up_card):
            return self.return_action("down", None)
        else:
            return self.return_action("up", hand.worst())

    def state_3(self, snap: Snapshot):
        suits = list(SUITS.keys())
        suits.remove(snap.down_card.suit)

        for suit in suits:
            hand = CSS(snap.hand, trump=suit).normalize("♠")
            if (hand & CSS("♠")).size < 3: continue
            if (hand & CSS("JLA♠")).size < 1: continue
            if (hand & CSS("♠ A♦♣♥")).size == 5: return self.return_action("alone", suit)
            return self.return_action("make", suit)

        return self.return_action("pass", None)

    def state_4(self, snap: Snapshot):  
        suits = allowed_suits(snap.down_card.suit)

        for suit in suits:
            hand = CSS(snap.hand, trump=suit).normalize("♠")
            if (hand & CSS("♠")).size < 3: continue
            if (hand & CSS("JLA♠")).size < 1: continue
            if (hand & CSS("♠ A♦♣♥")).size == 5: return self.return_action("alone", suit)
            return self.return_action("make", suit)

        # otherwise choose the suit with the most cards
        suits = allowed_suits(snap.down_card.suit)
        counts = {suit: CSS(suit).size for suit in suits}
        max_suit = max(counts, key=counts.get)
        return self.return_action("make", max_suit)

    def state_5(self, snap: Snapshot):
        if snap.lead_player.index == snap.for_index:
            return self.state_5_lead(snap)
        else:            
            return self.state_5_follow(snap)

    def state_5_lead(self, snap: Snapshot):
        lead = snap.tricks[-1].lead_suit
        hand = CSS(snap.hand, trump=snap.trump).playable(lead)
        not_played = played(snap).complement()

        # play the best card if you have it
        if not_played.best() in hand:
            return self.return_action("play", hand.best(lead))

        # play the best card in a non-trump suit
        not_trump = hand & CSS("♠").complement()
        if not_trump.size > 0:
            return self.return_action("play", not_trump.best(lead))

        # play your worst trump
        is_trump = hand & CSS("♠")
        return self.return_action ("play", is_trump.best(lead))
    
    def state_5_follow(self, snap: Snapshot):
        lead = snap.tricks[-1].lead_suit
        hand = CSS(snap.hand, trump=snap.trump).playable(lead)        
        partner = (snap.for_index + 2) % 4

        # play the worst card if partner is winning
        if snap.tricks[-1].winner == partner:
            return self.return_action ("play", hand.worst(lead))
        
        # if you have a card that will win, play it
        best = snap.tricks[-1].best_card
        beats = hand.beats(best, lead)
        if beats.size > 0:
            return self.return_action ("play", beats.worst(lead))
    
        # otherwise, play worst card
        return self.return_action ("play", hand.worst(lead))

    def state_6(self, snap: Snapshot): 
        return self.return_action("continue", None)

    def state_7(self, snap: Snapshot): 
        return self.return_action("continue", None)
    
    def return_action(self, action, data):
        self.trace = inspect.stack()
        return (action, data)