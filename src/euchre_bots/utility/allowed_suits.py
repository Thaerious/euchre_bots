from euchre.card.card_rank_factory import SUITS

def allowed_suits(suit):
    a = list(SUITS.keys())
    a.remove(suit)
    return a