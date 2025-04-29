# compare_cards.py
from euchre.card import Card


def winning_card(lead_suit: str, card1: Card, card2: Card) -> Card | None:
    """
    Determine which card wins between two cards based on Euchre rules.

    Args:
        lead_suit (str): The suit that was led.
        card1 (Card): First card played.
        card2 (Card): Second card played.

    Returns:
        Card | None: The winning card, or None if no winner.
    """
    if card1.is_right_bower():
        return card1
    if card2.is_right_bower():
        return card2
    if card1.is_left_bower():
        return card1
    if card2.is_left_bower():
        return card2

    if card1.suit_effective() == card1.trump and card2.suit_effective() != card2.trump:
        return card1
    if card1.suit_effective() != card1.trump and card2.suit_effective() == card2.trump:
        return card2

    if card1.suit_effective() == lead_suit and card2.suit_effective() != lead_suit:
        return card1
    if card1.suit_effective() != lead_suit and card2.suit_effective() == lead_suit:
        return card2

    rank1_index = Card.ranks.index(card1.rank)
    rank2_index = Card.ranks.index(card2.rank)

    if rank1_index > rank2_index:
        return card1
    if rank1_index < rank2_index:
        return card2

    return None


def losing_card(lead_suit: str, card1: Card, card2: Card) -> Card | None:
    """
    Determine which card loses between two cards based on Euchre rules.

    Args:
        lead_suit (str): The suit that was led.
        card1 (Card): First card played.
        card2 (Card): Second card played.

    Returns:
        Card | None: The losing card, or None if no loser.
    """
    winner = winning_card(lead_suit, card1, card2)
    if winner == card1:
        return card2
    if winner == card2:
        return card1
    return None
