from mpi4py import MPI
from euchre_bots import bots
from play import play
from itertools import product

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

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
    
        stats = play(bot_list, {"count": 10, "mirror": True})
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
    