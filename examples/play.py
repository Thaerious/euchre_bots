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
    
    def eval(self, bot_class):
        sum_games = 0
        played_games = 0

        for name, bot in self.bot_list.items():
            if isinstance(bot, bot_class):
                sum_games = sum_games + self.games_won[name]
                played_games = played_games + self.games_played

        if played_games == 0:
            return 0
        else:                
            return sum_games / played_games

    def print(self):
        headers = ["Name", "Tricks", "Hands", "Games", "Eval"]
        data = [
            [f"{name}:{type(self.bot_list[name]).__name__}", self.tricks_won[name], self.hands_won[name], self.games_won[name], self.eval(type(self.bot_list[name]))]
            for name in self.names
        ]
        data.append(["", self.tricks_played, self.hands_played, self.games_played])
        print(tabulate(data, headers=headers, tablefmt="grid"))

class PlayManager:
    def __init__(self, bot_list:list, seed = None):
        """
        Runs a series of Euchre games between bots and records performance data.

        Attributes:
            stats (Stats): Stores win statistics for all bots.
            bot_list (dict): Maps bot names to bot instances.
        """        
        self.stats = Stats(bot_list, seed)
        self.bot_list = bot_list

    def run(self, args):
        """
        Executes a series of games, applying optional mirror mode (rotated seating).
        
        Args:
            args (argparse.Namespace): Parsed CLI arguments with fields:
                - args["count"] (int): number of games (or half, if args["mirror"]ed)
                - args["mirror"] (bool): whether to repeat games with rotated seating
        """        
        self.args = args
        names = list(self.bot_list.keys())
        count = args["count"]
        if args.get("mirror"): count = (int)(count / 2)

        for i in range(count):
            rotate(names)
            seed = None if self.stats.seed is None else self.stats.seed + i
            game = Game(names, seed=seed)
            self.step(game)

            if args.get("mirror"):
                rotate(names)
                game = Game(names, seed=seed)
                self.step(game)

    def step(self, game: Game):
        """
        Executes one complete game, stepping through game states,
        invoking bots, and updating statistics.

        Args:
            game (Game): The Euchre game instance to run.
        """        
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

def play(bot_list:list, args):
    """
    High-level helper to run multiple games and return summary statistics.

    Args:
        bot_list: dict mapping player names ("bot0", ..., "bot3") to bot instances
        seed: starting random seed, or None
        args: CLI args with 'count' and 'args["mirror"]' attributes

    Returns:
        Stats: aggregated game results.
    """    
    pm = PlayManager(bot_list, args.get("seed"))
    pm.run(args)
    return pm.stats