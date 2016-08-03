import collections
import unittest

import card
import deck

class DeckTest(unittest.TestCase):
    def test_basic_deck(self):
        d = deck.Deck()
        self.assertEqual(52, len(d.cards))

        card_str_set = set(str(c) for c in d.cards)
        self.assertEqual(52, len(card_str_set))

    def test_reset_and_shuffle_cards_restored(self):
        d = deck.Deck()
        for _ in xrange(15):
            d.cards.pop()

        d.reset_and_shuffle()
        self.assertEqual(52, len(d.cards))

    def test_remove_cards_from_deck(self):
        d = deck.Deck()
        d.reset_and_shuffle()

        cards_to_remove = [card.create_card_from_short_name('ah'),
                           card.create_card_from_short_name('5d')]
        d.remove_cards_from_deck(cards_to_remove)

        self.assertEqual(50, len(d.cards))
        for c in cards_to_remove:
            self.assertNotIn(c, d.cards)

    def test_shuffle_randomness(self):
        shuffle_iterations = 1500
        card_keyed = collections.defaultdict(
            lambda: collections.defaultdict(int))
        
        d = deck.Deck()
        for _ in xrange(shuffle_iterations):
            d.reset_and_shuffle()
            for idx, card in enumerate(d.cards):
                card_keyed[str(card)][idx] += 1

        for card_key, pos_dict in card_keyed.iteritems():
            for position, count in pos_dict.iteritems():
                self.assertAlmostEqual(
                    1.0/52, float(count)/shuffle_iterations, 1)
    



if __name__ == '__main__':
    unittest.main()

