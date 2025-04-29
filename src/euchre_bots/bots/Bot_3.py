# Bot_3.py
from . import Bot0

# ["♠", "♥", "♣", "♦"]


def report_query(query, snap, all=[]):
    print(f"{query}, {snap.down_card}, [{snap.hand}]:{snap.trump}, {all}")


class Bot3(Bot0):
    def setup(self):
        super().setup()

        self.prepend(
            {
                "state_1": [],
                "state_2": [],
                "state_3": [],
                "state_4": [],
                "state_5": [],
            }
        )
