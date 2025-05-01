# enumerate_actions.py
from euchre import Game
from euchre.card import Card, playable

def enumerate_actions(game: Game):
    if game.state == 0:
        return [(None, "start", None)]
    if game.state == 1:
        return _enumerate(
            game.current_player.name, 
            ["pass", "order"], 
            [None]
        )
    if game.state == 2:
        enumerated = _enumerate(
            game.current_player.name, 
            ["up"], 
            game.current_player.hand
        )
        enumerated.append((game.current_player.name, "down", None))
        return enumerated
    if game.state == 3:
        suits = Card.suits.copy()
        suits.remove(game.down_card.suit)

        return _enumerate(
            game.current_player.name, 
            ["pass", "make"], 
            suits
        )    
    if game.state == 4:
        suits = Card.suits.copy()
        suits.remove(game.down_card.suit)

        return _enumerate(
            game.current_player.name, 
            ["make"], 
            suits
        )       
    if game.state == 5:
        suits = Card.suits.copy()

        return _enumerate(
            game.current_player.name, 
            ["play"], 
            playable(game.current_trick, game.current_player.hand)
        )
    
    return [(None, "continue", None)]        

def _enumerate(player, actions, data):
    list = []

    for action in actions:
        for datum in data:
            list.append((player, action, datum))

    return list
