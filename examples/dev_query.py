# dev_query.py
from euchre_bots.query import CardSelectionSet as CSS

# set = CSS("9JL♥ QK♣", trump="♥")
# print(set)
# print(set.normalize("♠"))
# print(set.normalize("♠").normalize("♥"))
# print(set.playable(lead=None))
# print(set.playable(lead=None).best())

# print("♣", CSS("♣"))
# set = CSS("Q♥ 10♣ K♦").playable("♣")
# print(set)

set = CSS("9JL♥ QK♣", trump="♥")
print(set)
print(set.beats("A♠", lead="♠"))
