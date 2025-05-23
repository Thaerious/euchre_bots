from mpi4py import MPI
import argparse
import random
from itertools import product
from mpi_evaluator import mpi_evaluator
from Solution import Solution
from util.flatten import flatten

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
mpi_process_cnt = comm.Get_size()

args = argparse.ArgumentParser()
args.add_argument("-p", "--pop_size", type=int, default=1, help="Population size")
args.add_argument("-c", "--count", type=int, default=1, help="Number of eval iterations")
args.add_argument("-s", "--seed", type=int, help="Set starting seed")
args.add_argument("-m", "--mirror", action="store_true", help="Repeat each seed with rotated seating")
args.add_argument("bots", nargs="*") 
args = args.parse_args()
args = vars(args) # convert args to dict

def generate_solutions(count):
    features_list = list(product(range(6), repeat=4))
    solutions = []

    while len(solutions) < count:
        features = features_list.pop(random.randrange(len(features_list)))
        solutions.append(Solution(features))

    return solutions

if __name__ == "__main__":
    solutions = generate_solutions(args["pop_size"])
    results = mpi_evaluator(solutions, args)
    
    if rank == 0:
        flat = flatten(results)
        print(f"number of processes = {mpi_process_cnt}")

        with open('output.txt', 'w') as f:
                for item in flat:
                    f.write(f"{item}\n")