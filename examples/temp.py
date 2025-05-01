# temp.py
from euchre_bots.query.Card_Selection_Set import SUITS, RANKS

print("{", end="")

i = 0
for suit in SUITS.keys():
    for rank in RANKS.keys():
        print(f"{i}:'{rank}{suit}', ", end="")
        i += 1

print("}", end="")