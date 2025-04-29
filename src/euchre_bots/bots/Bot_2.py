# Bot_2.py
from . import Bot1

# ["♠", "♥", "♣", "♦"]


def report_query(query, snap, all):
    print(query, snap.up_card, f"[{snap.hand}]", all)


class Bot2(Bot1):
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
