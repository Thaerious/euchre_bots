# compete.py
from euchre_bots import bots
from euchre import Game
from play import play
import argparse
import pathlib
import random

# handle cli arguments
def print_help():
    """Print available methods for the script."""

    print("USAGE")
    print("    python ./examples/compete.py <bot_class> <bot_class> [args...]\n")
    print("OPTIONS")
    print("    --count ## : the number of iterations to run\n")   

args = argparse.ArgumentParser()
args.add_argument("-c", "--count", type=int, default=1, help="Number of iterations")
args.add_argument("-l", "--list", action="store_true", help="List available bots")
args.add_argument("-s", "--seed", type=int, help="Set starting seed")
args.add_argument("bots", nargs="*") 
args = args.parse_args()

# list available bots when --list
if args.list:
    path = pathlib.Path(bots.__file__).parent
    files = [p.name for p in path.iterdir() if not p.name.startswith("_")]
    print(files)

if len(args.bots) == 0:
    print("Must provide at least one bot")
    exit()

# use random when no seed provided
seed = args.seed
if not seed: seed = random.randint(0, 100000)

# generate bots
bot_list = {}
bot_names = ["bot0", "bot1", "bot2", "bot3"]

for i in range(4):
    # get the bot class name from the cli
    idx = i % len(args.bots)
    class_name = args.bots[idx]

    # retrieve the bot class from the bots modules
    bot_type = getattr(bots, class_name)

    # create ans store an instance of the bot
    bot_list[bot_names[i]] = bot_type()

stats = play(bot_list, seed, args.count)
stats.print()
