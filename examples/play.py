from euchre import Game, Snapshot
from euchre.utility import rotate
from tabulate import tabulate
import random

class Stats:
    def __init__(self, bot_list:list, seed):
        self.seed = seed
        self.bot_list = bot_list
        self.names = bot_list.keys()
        self.tricks_won = {key: 0 for key in self.names}
        self.hands_won = {key: 0 for key in self.names}
        self.games_won = {key: 0 for key in self.names}
        self.tricks_played = 0
        self.hands_played = 0
        self.games_played = 0
    
    def print(self):
        headers = ["Name", "Tricks", "Hands", "Games"]
        data = [
            [f"{name}:{type(self.bot_list[name]).__name__}", self.tricks_won[name], self.hands_won[name], self.games_won[name]]
            for name in self.names
        ]
        data.append(["", self.tricks_played, self.hands_played, self.games_played])
        print(tabulate(data, headers=headers, tablefmt="grid"))

class PlayManager:
    def __init__(self, bot_list:list, seed):
        self.stats = Stats(bot_list, seed)
        self.bot_list = bot_list

    def run(self, count):
        names = list(self.bot_list.keys())

        for i in range(count):
            rotate(names)            
            game = Game(names, seed=self.stats.seed + i)
            self.step(game)

    def step(self, game: Game):
        game.input(None, "start")
        while game.state != 8:
            if game.state == 6:
                winning_index = game.tricks[-1].winner
                winning_name = game.get_player(winning_index).name
                self.stats.tricks_won[winning_name] += 1
                self.stats.tricks_played += 1
                game.input(None, "continue", None)
            elif game.state == 7:
                for player in game.won_last_hand.players:
                    self.stats.hands_won[player.name] += 1

                self.stats.hands_played += 1                    
                game.input(None, "continue", None)
            else:
                name = game.current_player.name
                bot = self.bot_list[name]
                snapshot = Snapshot(game, game.current_player.name)
                action = bot.decide(snapshot)

                try:
                    game.input(game.current_player.name, action[0], action[1])
                except:
                    print("Action generated from:")
                    for frame in bot.trace:
                         print(f" - {frame.filename.split("/")[-1]}:{frame.lineno} in {frame.function}")
                    print("")                         
                    raise

        self.stats.games_played += 1
        if game.teams[0].score > game.teams[1].score:
            for player in game.teams[0].players:
                self.stats.games_won[player.name] += 1
        else:                
            for player in game.teams[1].players:
                self.stats.games_won[player.name] += 1            

def play(bot_list:list, seed, count):
    pm = PlayManager(bot_list, seed)
    pm.run(count)
    return pm.stats