from euchre import Game, Snapshot
from euchre_bots.bots import Bot_X4A1
from euchre_bots.query import played
from euchre_bots.query import CardSelectionSet as CSS
import copy
import random

seed = random.randint(0, 10000)
print(seed)

game = Game(["Adam", "Eve", "Cain", "Able"], seed=7106)
game1 = copy.deepcopy(game)
game.input(None, "start", None)
snap = Snapshot(game, "Adam")

bot = Bot_X4A1()
while game.state != 5:
    snap = Snapshot(game, game.current_player.name)
    action = bot.decide(snap)
    game.input(game.current_player.name, action[0], action[1])    

for __ in range(3):
    for _ in range(5):
        # before = game.state
        snap = Snapshot(game, game.current_player.name)
        action = bot.decide(snap)
        game.input(game.current_player.name, action[0], action[1])    
        # print(f"{before} -> {game.state}")

snap = Snapshot(game, game.current_player.name)

hand = CSS(snap.hand, trump=snap.trump)
not_played = played(snap).complement()
print(f"trump = {snap.trump}")
print(hand)
print(not_played, not_played.best(), not_played.trump)
print(not_played.best() in hand)
