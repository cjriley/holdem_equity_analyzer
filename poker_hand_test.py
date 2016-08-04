import unittest

import card
import poker_hand

class HoldemHandTest(unittest.TestCase):
    def test_hand_eq(self):
        lhs_short = ['as','ad']
        lhs_cards = [card.create_card_from_short_name(sn) for sn in lhs_short]

        rhs_cards = [card.create_card_from_short_name(sn) for sn in lhs_short]

        lhs_he_hand = poker_hand.HoldemHand(cards=lhs_cards)
        rhs_he_hand = poker_hand.HoldemHand(cards=rhs_cards)

        self.assertEqual(lhs_he_hand, rhs_he_hand)

    def test_hand_eq_ne(self):
        lhs_short = ['as','ad']
        lhs_cards = [card.create_card_from_short_name(sn) for sn in lhs_short]
        lhs_he_hand = poker_hand.HoldemHand(cards=lhs_cards)

        rhs_short = ['ks', 'kd']
        rhs_cards = [card.create_card_from_short_name(sn) for sn in rhs_short]
        rhs_he_hand = poker_hand.HoldemHand(cards=rhs_cards)
        self.assertNotEqual(lhs_he_hand, rhs_he_hand)


class PokerHandParsingTest(unittest.TestCase):
    def test_parse_hands_valid_one_hand(self):
        hand_input = 'ahad'
        hands = poker_hand.parse_hands_into_holdem_hands(hand_input)

        self.assertEqual(1, len(hands))
        self.assertIn(card.create_card_from_short_name('ah'), hands[0].cards)
        self.assertIn(card.create_card_from_short_name('ad'), hands[0].cards)

    def test_parse_hands_valid_two_hands(self):
        hand_input = 'ahad,ksqc'
        hands = poker_hand.parse_hands_into_holdem_hands(hand_input)

        self.assertEqual(2, len(hands))
        self.assertIn(card.create_card_from_short_name('ah'), hands[0].cards)
        self.assertIn(card.create_card_from_short_name('ad'), hands[0].cards)
        self.assertIn(card.create_card_from_short_name('ks'), hands[1].cards)
        self.assertIn(card.create_card_from_short_name('qc'), hands[1].cards)

    def test_parse_hands_with_space(self):
        hand_input = 'Ah Ad'
        hands = poker_hand.parse_hands_into_holdem_hands(hand_input)

        self.assertEqual(1, len(hands))
        self.assertIn(card.create_card_from_short_name('ah'), hands[0].cards)
        self.assertIn(card.create_card_from_short_name('ad'), hands[0].cards)

    def test_parse_string_into_cards_space_sep(self):
        card_input = 'ah ad qs qc'

        cards = poker_hand.parse_string_into_cards(card_input)
        self.assertEqual(4, len(cards))
        self.assertIn(card.create_card_from_short_name('ah'), cards)
        self.assertIn(card.create_card_from_short_name('ad'), cards)
        self.assertIn(card.create_card_from_short_name('qs'), cards)
        self.assertIn(card.create_card_from_short_name('qc'), cards)

    def test_parse_string_into_cards_empty_string(self):
        self.assertEqual([], poker_hand.parse_string_into_cards(''))


    def test_parse_hands_one_hand_invalid(self):
        hand_input = 'asqc,jjjc'
        with self.assertRaisesRegexp(ValueError, 'Invalid suit'):
            poker_hand.parse_hands_into_holdem_hands(hand_input)


class PokerHandTest(unittest.TestCase):

    def _create_poker_hand_from_short_name_list(self, short_name_list):
        return poker_hand.PokerHand(
            cards=[card.create_card_from_short_name(sn)
                   for sn in short_name_list])

    def test_get_base_hand_from_cards(self):
        short_names = ['2h', '2c', '2s', '9s', 'qh', '4d', '2d']
        cards = [card.create_card_from_short_name(s) for s in short_names]

        expected_short_names = ['2h', '2c', '2s', '2d', 'qh']
        expected_cards = [
            card.create_card_from_short_name(s) for s in expected_short_names]
        self.assertItemsEqual(
            expected_cards, poker_hand.get_best_hand_from_cards(cards).cards)

    def test_contains_straight_no_straight(self):
        short_names = ['2h', '5d', '6s', '7s', '9s']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertFalse(poker_hand.contains_straight(hand))

    def test_contains_straight_normal_straight(self):
        short_names = ['2h', '3s', '4d', '5h', '6c']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertTrue(poker_hand.contains_straight(hand))

    def test_contains_straight_ace_to_five(self):
        short_names = ['2h', '3s', '4d', '5h', 'ac']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertTrue(poker_hand.contains_straight(hand))

    def test_contains_straight_invalid_wrap(self):
        short_names = ['qh', 'kh', 'as', '2d', '3c']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertFalse(poker_hand.contains_straight(hand))

    def test_contains_flush_with_flush(self):
        short_names = ['2h', '3h', '4h', '5h', 'qh']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertTrue(poker_hand.contains_flush(hand))

    def test_contains_flush_no_flush(self):
        short_names = ['2h', '3h', '4c', '5h', 'qh']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertFalse(poker_hand.contains_flush(hand))

    def test_contains_straight_flush_no_straight_flush(self):
        short_names = ['2h', '3h', '4h', '5h', 'qh']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertFalse(poker_hand.contains_straight_flush(hand))

    def test_contains_straight_flush_straight_flush(self):
        short_names = ['2h', '3h', '4h', '5h', '6h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertTrue(poker_hand.contains_straight_flush(hand))

    def test_contains_four_of_a_kind_with_four_of_a_kind(self):
        short_names = ['2h', '2c', '2d', '2s', '6h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertTrue(poker_hand.contains_four_of_a_kind(hand))

    def test_contains_four_of_a_kind_no_four_of_a_kind(self):
        short_names = ['2h', '2c', '2d', '3s', '6h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertFalse(poker_hand.contains_four_of_a_kind(hand))

    def test_contains_three_of_a_kind_with_three_of_a_kind(self):
        short_names = ['2h', '2c', '2d', '3s', '6h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertTrue(poker_hand.contains_three_of_a_kind(hand))

    def test_contains_three_of_a_kind_with_four_of_a_kind(self):
        """Note that this should return false since we want exact counts"""
        short_names = ['2h', '2c', '2d', '2s', '6h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertFalse(poker_hand.contains_three_of_a_kind(hand))

    def test_contains_three_of_a_kind_no_three_of_a_kind(self):
        short_names = ['ah', 'jc', '2d', '2s', '6h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertFalse(poker_hand.contains_three_of_a_kind(hand))

    def test_contains_full_house_with_full_house(self):
        short_names = ['ah', 'ac', '2d', '2s', '2h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertTrue(poker_hand.contains_full_house(hand))

    def test_contains_full_house_with_three_of_a_kind_only(self):
        short_names = ['ah', 'jc', '2d', '2s', '2h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertFalse(poker_hand.contains_full_house(hand))

    def test_contains_full_house_with_two_pair_only(self):
        short_names = ['ah', 'jc', '2d', '2s', '8h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertFalse(poker_hand.contains_full_house(hand))

    def test_contains_two_pair_with_two_pair(self):
        short_names = ['ah', '8c', '2d', '2s', '8h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertTrue(poker_hand.contains_two_pair(hand))

    def test_contains_two_pair_with_one_pair(self):
        short_names = ['ah', '8c', '2d', '2s', '9h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertFalse(poker_hand.contains_two_pair(hand))

    def test_contains_two_pair_with_no_pair(self):
        short_names = ['ah', '8c', 'qd', '2s', '9h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertFalse(poker_hand.contains_two_pair(hand))

    def test_contains_one_pair_with_one_pair(self):
        short_names = ['ah', '8c', 'qd', '8s', '9h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertTrue(poker_hand.contains_one_pair(hand))

    def test_contains_one_pair_with_two_pair(self):
        short_names = ['9d', '8c', 'qd', '8s', '9h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertFalse(poker_hand.contains_one_pair(hand))

    def test_get_hand_rank_straight_flush(self):
        short_names = ['2h', '3h', '4h', '5h', '6h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertEqual(
            poker_hand.STRAIGHT_FLUSH, poker_hand.get_hand_rank(hand))

    def test_get_hand_rank_four_of_a_kind(self):
        short_names = ['2h', '2s', '2d', '2c', '6h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertEqual(
            poker_hand.FOUR_OF_A_KIND, poker_hand.get_hand_rank(hand))

    def test_get_hand_rank_full_house(self):
        short_names = ['2h', '2s', '2d', '6c', '6h']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertEqual(
            poker_hand.FULL_HOUSE, poker_hand.get_hand_rank(hand))

    def test_get_hand_rank_flush(self):
        short_names = ['2d', '3d', '8d', 'ad', 'qd']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertEqual(
            poker_hand.FLUSH, poker_hand.get_hand_rank(hand))

    def test_get_hand_rank_straight(self):
        short_names = ['2d', '3d', '4c', '5s', 'ad']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertEqual(
            poker_hand.STRAIGHT, poker_hand.get_hand_rank(hand))

    def test_get_hand_rank_three_of_a_kind(self):
        short_names = ['2d', '3d', '2c', '2s', 'ad']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertEqual(
            poker_hand.THREE_OF_A_KIND, poker_hand.get_hand_rank(hand))

    def test_get_hand_rank_two_pair(self):
        short_names = ['2d', '3d', '2c', '3s', 'ad']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertEqual(
            poker_hand.TWO_PAIR, poker_hand.get_hand_rank(hand))

    def test_get_hand_rank_one_pair(self):
        short_names = ['2d', '8d', '2c', '3s', 'ad']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertEqual(
            poker_hand.ONE_PAIR, poker_hand.get_hand_rank(hand))

    def test_get_hand_rank_high_card(self):
        short_names = ['2d', '8d', 'ac', '3s', 'qd']
        hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertEqual(
            poker_hand.HIGH_CARD, poker_hand.get_hand_rank(hand))

    def test_hand_comparison_different_ranks_lhs_better(self):
        lhs_short_names = ['2c', '3c', '4c', '5c', '6c']
        lhs_hand = self._create_poker_hand_from_short_name_list(lhs_short_names)

        rhs_short_names = ['qd', 'qs', 'qc', 'qh', '5d']
        rhs_hand = self._create_poker_hand_from_short_name_list(rhs_short_names)

        self.assertGreater(lhs_hand, rhs_hand)

    def test_hand_comparison_different_ranks_rhs_better(self):
        lhs_short_names = ['qd', 'qs', 'ac', '5h', '5d']
        lhs_hand = self._create_poker_hand_from_short_name_list(lhs_short_names)

        rhs_short_names = ['2c', '2s', '2h', '5c', '6c']
        rhs_hand = self._create_poker_hand_from_short_name_list(rhs_short_names)

        self.assertLess(lhs_hand, rhs_hand)

    def test_hand_comparison_same_rank(self):
        lhs_short_names = ['qd', 'qs', 'ac', '5h', '5d']
        lhs_hand = self._create_poker_hand_from_short_name_list(lhs_short_names)

        rhs_short_names = ['2c', '2s', '5h', '5c', '6c']
        rhs_hand = self._create_poker_hand_from_short_name_list(rhs_short_names)

        self.assertGreater(lhs_hand, rhs_hand)

    def test_compare_secondary_ranks_rhs_first(self):
        lhs_short_names = ['ah', 'ad', 'as', 'qd', 'qc']
        lhs_hand = self._create_poker_hand_from_short_name_list(lhs_short_names)

        rhs_short_names = ['qd', 'qc', '2s', '2d', '2c']
        rhs_hand = self._create_poker_hand_from_short_name_list(rhs_short_names)

        self.assertGreater(
            poker_hand.compare_secondary_ranks(lhs_hand, rhs_hand), 0)

    def test_compare_secondary_ranks_lhs_first(self):
        lhs_short_names = ['3h', '3d', '3s', 'qd', 'qc']
        lhs_hand = self._create_poker_hand_from_short_name_list(lhs_short_names)

        rhs_short_names = ['qd', 'qc', 'qs', '2d', '2c']
        rhs_hand = self._create_poker_hand_from_short_name_list(rhs_short_names)

        self.assertLess(
            poker_hand.compare_secondary_ranks(lhs_hand, rhs_hand), 0)

    def test_compare_secondary_ranks_equal_hands(self):
        short_names = ['as', '2d', 'qs', 'ks', 'td']
        lhs_hand = self._create_poker_hand_from_short_name_list(short_names)
        rhs_hand = self._create_poker_hand_from_short_name_list(short_names)
        self.assertEqual(
            0, poker_hand.compare_secondary_ranks(lhs_hand, rhs_hand))

    def test_compare_secondary_ranks_ace_to_five(self):
        lhs_short_names = ['as', '2d', '3c', '4h', '5d']
        lhs_hand = self._create_poker_hand_from_short_name_list(lhs_short_names)

        rhs_short_names = ['8s', '9d', 'tc', 'jd', 'qd']
        rhs_hand = self._create_poker_hand_from_short_name_list(rhs_short_names)
        self.assertLess(
            poker_hand.compare_secondary_ranks(lhs_hand, rhs_hand), 0)

        # Try the reverse order.
        self.assertGreater(
            poker_hand.compare_secondary_ranks(rhs_hand, lhs_hand), 0)

    def test_poker_hand_object_comparison_lt(self):
        lhs_short_names = ['as', 'qs', 'js', '5s', '2s']
        lhs_hand = self._create_poker_hand_from_short_name_list(lhs_short_names)

        rhs_short_names = ['2c', '5d', '8h', 'ts', 'ad']
        rhs_hand = self._create_poker_hand_from_short_name_list(rhs_short_names)

        self.assertTrue(rhs_hand < lhs_hand)
        self.assertTrue(rhs_hand <= lhs_hand)
        self.assertTrue(lhs_hand > rhs_hand)
        self.assertTrue(lhs_hand >= rhs_hand)

    def test_poker_hand_object_comparison_equality(self):
        lhs_short_names = ['6d', '7h', '8s', '9c', 'td']
        lhs_hand = self._create_poker_hand_from_short_name_list(lhs_short_names)

        rhs_short_names = ['6h', '7d', '8s', '9c', 'td']
        rhs_hand = self._create_poker_hand_from_short_name_list(rhs_short_names)

        self.assertTrue(lhs_hand == rhs_hand)
        self.assertFalse(lhs_hand > rhs_hand)


if __name__ == '__main__':
    unittest.main()
