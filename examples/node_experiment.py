# node_experiment.py
from euchre.card import Deck, Card
from euchre import Game, Euchre
from euchre_bots.utility import enumerate_actions
import copy

class NodeCollection(list):
    def add_layer(self):
        result = NodeCollection()
        for node in self:
            result.extend(node.add_layer())

        return result

class Node:
    def __init__(self, game:Game, parent = None, action_tuple = None):
        self.game = game
        self.parent = parent
        self.children = NodeCollection()
        self.action_tuple = action_tuple
        self.depth = 0
        self._score = None

    @property
    def score(self):
        if len(self.children) == 0:
            return 0

        if self._score is not None:
            return self._score
        
        return sum(child.score for child in self.children) / len(self.children)

    @property
    def size(self):
        return sum(child.size for child in self.children) + len(self.children)

    def add_layer(self):
        if self.game.teams[0].tricks >= 3:
            return self.freeze_node()

        if self.game.teams[1].tricks >= 3:
            return self.freeze_node()

        if self.game.state >= 7:
            return NodeCollection()       

        while self.game.state >= 6:
            self.game.input(None, "continue", None)

        enumerated_actions = enumerate_actions(self.game)

        for action_tuple in enumerated_actions:
            game = copy.deepcopy(self.game)
            game.input(*action_tuple)
            child = Node(game, self, action_tuple)
            self.children.append(child) 
            child.depth = self.depth + 1

        return self.children       

    def freeze_node(self):
        self._score = 1
        return []

    def print(self, max_depth = 100, indent = 0):           
        print("  " * indent, self.game.state, self.action_tuple, self.score, self.game.teams[0].tricks, self.game.teams[1].tricks)
        if (max_depth <= indent): return

        for child in self.children:
            child.print(max_depth, indent + 1)

game = Game(["Adam", "Eve", "Cain", "Able"])
game.enter_state_1()
game.trump = "♠"
game.enter_state_5()

root = Node(game)
layer = root.add_layer()

i = 0
while len(layer) > 0 and i < 11:
    layer = layer.add_layer()
    print(i, root.size, len(layer))
    i += 1

root.print()    