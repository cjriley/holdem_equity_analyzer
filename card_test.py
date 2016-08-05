"""Tests for card.py"""
import unittest

import card

class CardTest(unittest.TestCase):

    def test_create_card_invalid_suit(self):
        with self.assertRaisesRegexp(ValueError, 'Invalid suit'):
            card.Card('Notasuit', 'Jack')

    def test_create_card_invalid_rank(self):
        with self.assertRaisesRegexp(ValueError, 'Invalid rank'):
            card.Card('Clubs', 'Fourteen')

    def test_create_card_from_short_name_too_short(self):
        with self.assertRaisesRegexp(ValueError, 'Invalid short name'):
            card.create_card_from_short_name('x')

    def test_create_card_from_short_name_too_long(self):
        with self.assertRaisesRegexp(ValueError, 'Invalid short name'):
            card.create_card_from_short_name('xyz')

    def test_create_card_from_short_name_invalid_rank(self):
        with self.assertRaisesRegexp(ValueError, 'Invalid rank character'):
            card.create_card_from_short_name('zh')

    def test_create_card_from_short_name_invalid_suit(self):
        with self.assertRaisesRegexp(ValueError, 'Invalid suit character'):
            card.create_card_from_short_name('tq')

    def test_create_card_from_short_name_valid(self):
        c = card.create_card_from_short_name('th')
        self.assertEqual('Ten', c.rank)
        self.assertEqual('Hearts', c.suit)

    def test_create_card_from_short_name_valid_uppercase(self):
        c = card.create_card_from_short_name('As')
        self.assertEqual('Ace', c.rank)
        self.assertEqual('Spades', c.suit)

    def test_short_form(self):
        c = card.create_card_from_short_name('as')
        self.assertEqual('As', c.short_form())
        c = card.create_card_from_short_name('9s')
        self.assertEqual('9s', c.short_form())


if __name__ == '__main__':
    unittest.main()
