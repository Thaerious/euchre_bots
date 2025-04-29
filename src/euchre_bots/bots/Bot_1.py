# Bot_1.py
from euchre import Snapshot

from ..query import Query, QueryBase, QueryCollection
from . import Bot0

# ["♠", "♥", "♣", "♦"]


class PrintQuery(QueryBase):
    name = "print"

    def decide(self, snap: Snapshot):
        print(snap)
        return QueryCollection()


class Bot1(Bot0):
    def setup(self):
        super().setup()

        self.prepend(
            {
                "state_1": [
                    Query("J♥ J♦ A♥").up_card("♥").count("3").do("order"),
                    Query("J♦ J♥ A♦").up_card("♦").count("3").do("order"),
                    Query("J♣ J♠ A♣").up_card("♣").count("3").do("order"),
                    Query("J♠ J♣ A♠").up_card("♠").count("3").do("order"),
                    Query("J♥ J♦ A♥").up_card("♥").lead("02").count("2").do("order"),
                    Query("J♦ J♥ A♦").up_card("♦").lead("02").count("2").do("order"),
                    Query("J♣ J♠ A♣").up_card("♣").lead("02").count("2").do("order"),
                    Query("J♠ J♣ A♠").up_card("♠").lead("02").count("2").do("order"),
                ],
                "state_2": [
                    Query("910JQK♥").count("1").worst().do("up"),
                    Query("910JQK♦").count("1").worst().do("up"),
                    Query("910JQK♣").count("1").worst().do("up"),
                    Query("910JQK♠").count("1").worst().do("up"),
                    Query("~♠ 910JQK").count("12345").worst().do("up"),
                ],
                "state_3": [
                    Query("♣").down_card("~♣").count("345").do("make", "♣"),
                    Query("♦").down_card("~♦").count("345").do("make", "♦"),
                    Query("♥").down_card("~♥").count("345").do("make", "♥"),
                    Query("♠").down_card("~♠").count("345").do("make", "♠"),
                    Query("J♣ J♠ A♣").down_card("~♣").count("23").do("make", "♣"),
                    Query("J♦ J♥ A♦").down_card("~♦").count("23").do("make", "♦"),
                    Query("J♥ J♦ A♥").down_card("~♥").count("23").do("make", "♥"),
                    Query("J♠ J♣ A♠").down_card("~♠").count("23").do("make", "♠"),
                ],
                "state_4": [
                    Query("♣").down_card("~♣").count("345").do("make", "♣"),
                    Query("♦").down_card("~♦").count("345").do("make", "♦"),
                    Query("♥").down_card("~♥").count("345").do("make", "♥"),
                    Query("♠").down_card("~♠").count("345").do("make", "♠"),
                    Query("J♣ J♠ A♣").down_card("~♣").count("23").do("make", "♣"),
                    Query("J♦ J♥ A♦").down_card("~♦").count("23").do("make", "♦"),
                    Query("J♥ J♦ A♥").down_card("~♥").count("23").do("make", "♥"),
                    Query("J♠ J♣ A♠").down_card("~♠").count("23").do("make", "♠"),
                ],
                "state_5": [
                    Query("~", "beats").lead("123").wins().worst().do("play"),
                    Query("~", "loses").lead("123").loses().worst().do("play"),
                    Query("♥", name="play ♥").lead("0").best().do("play"),
                    Query("♦", name="play ♦").lead("0").best().do("play"),
                    Query("♣", name="play ♣").lead("0").best().do("play"),
                    Query("♠", name="play ♠").lead("0").best().do("play"),
                ],
            }
        )
