# compete.py
# compete.py
from euchre_bots import bots
from euchre import Game, Snapshot
import argparse
import pathlib
import random

def play(game: Game, bot_list):
    game.input(None, "start")
    while game.current_state != 8:
        if game.current_state in [6, 7]:
            game.input(None, "continue", None)
        else:
            index = game.current_player.index
            bot = bot_list[index]
            snapshot = Snapshot(game, game.current_player.name)
            action = bot.decide(snapshot)
            game.input(game.current_player.name, action[0], action[1])

def print_help():
    """Print available methods for the script."""

    print("USAGE")
    print("    python ./examples/compete.py <bot_class> <bot_class> [args...]\n")
    print("OPTIONS")
    print("    --count ## : the number of iterations to run\n")   

args = argparse.ArgumentParser()
args.add_argument("--count", type=int, default=1, help="Number of iterations")
args.add_argument("--list", action="store_true", help="List available bots")
args.add_argument("--seed", type=int, help="Set starting seed")
args.add_argument("bots", nargs="*") 
args = args.parse_args()

if args.list:
    path = pathlib.Path(bots.__file__).parent
    files = [p.name for p in path.iterdir() if not p.name.startswith("_")]
    print(files)

if len(args.bots) == 0:
    print("Must provide at least one bot")
    exit()

bot_list = []
bot_names = ["bot0", "bot1", "bot2", "bot3"]

for i in range(4):
    bot_name = args.bots[i % len(args.bots)]
    bot_type = getattr(bots, bot_name)
    bot_list.append(bot_type())

seed = args.seed
if not seed: seed = random.randint(0, 100000)

for i in range(args.count):
    game = Game(bot_names, seed=seed)
    play(game, bot_list)
    seed = seed + 1
