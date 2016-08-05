"""Implementation of a deck of cards."""
import card
import random

def reverse_enumerator(input_list):
    """Enumerate a sequence in reverse."""
    for index in reversed(xrange(len(input_list))):
        yield index, input_list[index]


def generate_deck():
    """Generates a standard 52 card deck.

    Returns:
        List of cards, one of each suit/rank.
    """
    return [card.Card(s, r) for s in card.SUITS for r in card.RANKS]


class Deck(object):
    def __init__(self):
        self.cards = generate_deck()

    def reset_and_shuffle(self):
        """Generates a new deck of cards and randomly shuffles it."""
        self.cards = generate_deck()
        random.shuffle(self.cards)

    def remove_cards_from_deck(self, cards):
        """Removes the specified cards from the deck.

        Args:
            iterable of Card.
        """
        for idx, item in reverse_enumerator(self.cards):
            if item in cards:
                self.cards.pop(idx)

    def pop(self):
        """Remove a card from the deck and return it."""
        return self.cards.pop(0)

