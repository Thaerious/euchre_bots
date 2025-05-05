# do_deap.py
from euchre_bots import bots
from play import play
from itertools import product

best_score = 0

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

for combo in product(range(6), repeat=4):
    bot_list = {
        "bot_1": bots.Bot_1A2(),
        "bot_2": bots.Bot_3(combo),
        "bot_3": bots.Bot_1A2(),
        "bot_4": bots.Bot_3(combo),
    }
   
    stats = play(bot_list, {"count": 30, "mirror": True})
    score = stats.eval(bots.Bot_3)
    if score > best_score:
        print(score, combo)
        best_score = score

if __name__ == "__main__":
    a = product(range(6), repeat=4)
    print(a)
    b = split_list(list(a), 4)
    print(b)