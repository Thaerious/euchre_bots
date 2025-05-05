# do_deap.py
import random
from deap import base, creator, tools, algorithms
from euchre_bots import bots
from play import play
from types import SimpleNamespace

# --- STEP 1: Define fitness and individual types ---
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# --- STEP 2: Toolbox setup ---
toolbox = base.Toolbox()

# Integer gene in range [0, 5]
toolbox.register("attr_int", random.randint, 0, 5)

# Individual of 10 integer genes
toolbox.register("individual", 
                 tools.initRepeat, 
                 creator.Individual,
                 toolbox.attr_int, 
                 n=4)

# Population
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# --- STEP 3: Fitness function ---
def evaluate(ind):
    bot_list = {
        "bot_1": bots.Bot_1A2(),
        "bot_2": bots.Bot_3(ind),
        "bot_3": bots.Bot_1A2(),
        "bot_4": bots.Bot_3(ind),
    }
    
    stats = play(bot_list, {"count": 10})
    return stats.eval(bots.Bot_3),

# --- STEP 4: Genetic operators ---
toolbox.register("mate", tools.cxTwoPoint)

def mut_int(individual, low=0, high=5, indpb=0.2):
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] += random.choice([-1, 1])
            individual[i] = max(low, min(high, individual[i]))  # clip to bounds
    return individual,

toolbox.register("mutate", mut_int)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

# --- STEP 5: Run the algorithm ---
def main():
    pop = toolbox.population(n=30)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", lambda f: sum(x[0] for x in f) / len(f))
    stats.register("max", lambda f: max(x[0] for x in f))

    pop, _ = algorithms.eaSimple(
        pop, toolbox,
        cxpb=0.5, mutpb=0.2,
        ngen=30, stats=stats,
        halloffame=hof,
        verbose=True
    )

    print("\nBest solution:", hof[0])
    print("Fitness:", hof[0].fitness.values[0])

if __name__ == "__main__":
    main()