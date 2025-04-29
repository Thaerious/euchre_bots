# Card_Selection_Set.py
from euchre.utility import del_string
from euchre.card import card_rank_factory, ORDER, SUITS, RANKS, COMPL
from collections.abc import Iterable
import re

class CardSelectionSet(set):
    def __init__(self, phrase = None, trump = None):
        super().__init__()
        self.flag_left_bower = False
        self.trump = trump
        if phrase: self.select(phrase)

    @property
    def size(self):
        return len(self)

    def copy(self):
        set = CardSelectionSet(self)
        set.trump = self.trump
        return set

    def select(self, phrase):        
        if isinstance(phrase, str):
            for split in phrase.split():
                self._select(split)
        elif isinstance(phrase, int):            
                self.add(phrase)
        elif isinstance(phrase, Iterable):
            for item in phrase:
                self.select(item)
        else:
            self.select((str)(phrase))           
        return self

    def as_card_strings(self):
        for card_idx in self:
            yield ORDER[card_idx]

    def playable(self, lead):
        lead_set = CardSelectionSet(lead, trump=self.trump)
        playable = lead_set & self
        print(f"{lead}: {playable} = {lead_set} & {self}")
        if len(playable) > 0: return playable
        return self.copy()

    def best(self, lead = None):
        fn = card_rank_factory(self.trump, lead)
        return max(self.as_card_strings(), key=fn)

    def worst(self, lead = None):
        fn = card_rank_factory(self.trump, lead)
        return min(self.as_card_strings(), key=fn)

    def normalize(self, trump):
        norm = CardSelectionSet(trump=trump)
        shift = SUITS[trump] - SUITS[self.trump]

        for card_idx in self:
            new_idx = (card_idx + (6 * shift)) % 24
            norm.add(new_idx)
        return norm

    def __and__(self, other):
            result = super().__and__(other)
            return CardSelectionSet(result)

    def _select(self, phrase):
        if phrase == "*":
            self.update(range(24))
            return

        ranks = re.findall(r"10|[9JQKAL]", phrase)
        suits = re.findall(r"[♠♥♣♦]", phrase)

        fn = self.add
        if phrase.startswith("~"): fn = self.remove

        if len(suits) == 0:
            suits = SUITS.keys()

        if len(ranks) == 0:
            ranks = list(RANKS.keys())
            if self.trump in suits:
                ranks.append("L")

        print(ranks, suits)
        return self._iterate(ranks, suits, fn)

    def _iterate(self, ranks, suits, fn):
        for rank in ranks:
            for suit in suits:
                if rank == "L":
                    rank = "J"
                    suit = COMPL[suit]

                idx = ORDER.inv[f"{rank}{suit}"]
                fn(idx)

    def __str__(self):
        cards = []
        for idx in self:
            cards.append(ORDER[idx])
        return "{" + del_string(cards) + "}"