import card
import random

def reverse_enumerator(input_list):
   for index in reversed(xrange(len(input_list))):
      yield index, input_list[index]

class Deck(object):
    def __init__(self):
        self.cards = self._generate_deck()

    def _generate_deck(self):
        return [card.Card(s, r) for s in card.SUITS for r in card.RANKS]

    def reset_and_shuffle(self):
        self.cards = self._generate_deck()
        random.shuffle(self.cards)

    def remove_cards_from_deck(self, cards):
        for idx, item in reverse_enumerator(self.cards):
            if item in cards:
                self.cards.pop(idx)
    def pop(self):
        return self.cards.pop(0)

