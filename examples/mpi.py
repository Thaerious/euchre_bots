from mpi4py import MPI
from euchre_bots import bots
from play import play
from itertools import product
import argparse

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

args = argparse.ArgumentParser()
args.add_argument("-c", "--count", type=int, default=1, help="Number of iterations")
args.add_argument("-l", "--list", action="store_true", help="List available bots")
args.add_argument("-s", "--seed", type=int, help="Set starting seed")
args.add_argument("-m", "--mirror", action="store_true", help="Repeat each seed with rotated seating")
args.add_argument("bots", nargs="*") 
args = args.parse_args()
args = vars(args) # convert args to dict

def split_list(my_list, count):
    length = len(my_list)
    chunk_size = length // count
    remainder_size = length % count

    chunks = []
    start = 0
    for i in range(count):
        end = start + chunk_size
        if i < remainder_size: end += 1

        chunk = my_list[start:end]
        chunks.append(chunk)
        start = end
    
    return chunks

def eval(feature_list):
    results = []

    for features in feature_list:
        bot_list = {
            "bot_1": bots.Bot_1A2(),
            "bot_2": bots.Bot_3(features),
            "bot_3": bots.Bot_1A2(),
            "bot_4": bots.Bot_3(features),
        }
    
        stats = play(bot_list, {"count": args["count"], "mirror": args["mirror"]})
        score = stats.eval(bots.Bot_3)
        tuple = (features, score)
        results.append(tuple)

    return results

if __name__ == "__main__":
    features = product(range(6), repeat=4)
    features = list(features)
    split_features = split_list(features, size)

    my_features = comm.scatter(split_features, root=0)
    my_results = eval(my_features)
    all_results = comm.gather(my_results, root=0)

    if rank == 0:
        flat = []
        for sub_list in all_results:
            for item in sub_list:
                flat.append(item)

        print(len(flat), len(features))
    