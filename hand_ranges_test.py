import itertools
import mock
import unittest

import card
import hand_ranges
import poker_hand


class HandRangesTest(unittest.TestCase):

    def test_single_hand_description_bad_suffix(self):
        with self.assertRaises(hand_ranges.HandDescriptionParseError):
            hand_ranges.single_hand_description_to_hands('akz')

    def test_single_hand_description_bad_rank(self):
        with self.assertRaises(hand_ranges.HandDescriptionParseError):
            hand_ranges.single_hand_description_to_hands('ZZ')

    def test_single_hand_description_to_hands_suited(self):
        desc = '76s'
        hands = hand_ranges.single_hand_description_to_hands(desc)
        self.assertEqual(4, len(hands))

    def test_single_hand_description_to_hands_offsuit(self):
        desc = 'AKo'
        hands = hand_ranges.single_hand_description_to_hands(desc)
        self.assertEqual(12, len(hands))

    def test_single_hand_description_to_hands_pair(self):
        desc = '88'

        hands = hand_ranges.single_hand_description_to_hands(desc)
        self.assertEqual(6, len(hands))

    def test_generate_unsuited_hands(self):
        rank1 = 'King'
        rank2 = 'Queen'

        all_hands = hand_ranges.generate_unsuited_hands(rank1, rank2)

        self.assertEqual(12, len(all_hands))
        sample_expected_hand = poker_hand.HoldemHand(
            cards=[card.Card('Clubs', 'King'), card.Card('Spades', 'Queen')])
        self.assertIn(sample_expected_hand, all_hands)
        for h in all_hands:
            self.assertNotEqual(h.cards[0].suit, h.cards[1].suit)

    def test_generate_unsuited_cards(self):
        rank1 = 'Seven'
        rank2 = 'Eight'
        dead_cards = [
            card.Card('Clubs', 'Seven'), card.Card('Diamonds', 'Eight')]

        all_hands = hand_ranges.generate_unsuited_hands(
            rank1, rank2, dead_cards=dead_cards)

        self.assertEqual(7, len(all_hands))
        flattened_cards = []
        for h in all_hands:
            flattened_cards.extend(h.cards)
        for dc in dead_cards:
            self.assertNotIn(dc, flattened_cards)

    def test_generate_suited_hands(self):
        rank1 = 'Two'
        rank2 = 'Jack'

        all_hands = hand_ranges.generate_suited_hands(rank1, rank2)

        self.assertEqual(4, len(all_hands))
        expected_hand = poker_hand.HoldemHand(
            cards=[card.Card('Hearts', 'Two'),
                   card.Card('Hearts', 'Jack')])
        self.assertIn(expected_hand, all_hands)
        for h in all_hands:
            self.assertEqual(h.cards[0].suit, h.cards[1].suit)
    def test_generate_suited_hands_dead_cards(self):
        rank1 = 'Three'
        rank2 = 'King'

        dead_cards = [card.Card('Hearts', 'Three'),
                      card.Card('Spades', 'King')]
        all_hands = hand_ranges.generate_suited_hands(
            rank1, rank2, dead_cards=dead_cards)

        self.assertEqual(2, len(all_hands))
        expected_hands = [
            poker_hand.HoldemHand(cards=[card.Card('Diamonds', 'Three'),
                                         card.Card('Diamonds', 'King')]),
            poker_hand.HoldemHand(cards=[card.Card('Clubs', 'Three'),
                                         card.Card('Clubs', 'King')]),
        ]
        for h in expected_hands:
            self.assertIn(h, all_hands)

    def test_generate_pair_hands(self):
        rank = 'Two'
        all_pairs = hand_ranges.generate_pair_hands(rank)
        print all_pairs

        self.assertEqual(6, len(all_pairs))
        expected_hand = poker_hand.HoldemHand(
            cards=[card.Card('Hearts', 'Two'), card.Card('Spades', 'Two')])
        self.assertIn(expected_hand, all_pairs)

    def test_generate_pair_hands_dead_cards(self):
        rank = 'Five'
        dead_cards = [card.Card('Hearts', rank)]

        all_pairs = hand_ranges.generate_pair_hands(rank, dead_cards=dead_cards)
        self.assertEqual(3, len(all_pairs))
        flattened_cards = []
        for hand in all_pairs:
            flattened_cards.extend(hand.cards)
        for dc in dead_cards:
            self.assertNotIn(dc, flattened_cards)

if __name__ == '__main__':
    unittest.main()
