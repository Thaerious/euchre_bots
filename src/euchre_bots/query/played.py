from euchre import Snapshot
from .Card_Selection_Set import CardSelectionSet as CSS

def played(snapshot: Snapshot):
    played = CSS(trump=snapshot.trump)

    for trick in snapshot.tricks:
        played.select(trick)

    return played