from mpi4py import MPI
from euchre_bots import bots
from play import play
from util.split_list import split_list

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
mpi_process_cnt = comm.Get_size()

def eval(solution, args):
    bot_list = {
        "bot_1": bots.Bot_1A2(),
        "bot_2": bots.Bot_3(solution.features),
        "bot_3": bots.Bot_1A2(),
        "bot_4": bots.Bot_3(solution.features)
    }

    stats = play(bot_list, {"count": args["count"], "mirror": args["mirror"]})
    score = stats.eval(bots.Bot_3)
    solution.update_score(score, args["count"])
    print(rank, solution)

    return solution

def evaluator(solutions, args):
    for solution in solutions: eval(solution, args)
    return solutions

def mpi_evaluator(solutions, args):
    split = split_list(solutions, mpi_process_cnt) if rank == 0 else None

    my_solutions = comm.scatter(split, root=0)
    my_results = evaluator(my_solutions, args)
    all_results = comm.gather(my_results, root=0)

    return all_results