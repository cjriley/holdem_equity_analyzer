import unittest

import card
import monte_carlo_runner
import poker_hand

class MonteCarloRunnerTest(unittest.TestCase):
    def test_reset_deck(self):
        he_ranges = poker_hand.parse_hands_into_holdem_hands('asad,qsjh')
        board_cards = poker_hand.parse_string_into_cards('2c2d')

        dead_cards = poker_hand.parse_string_into_cards('8h')

        mcr = monte_carlo_runner.MonteCarloRunner(
            he_ranges, board_cards=board_cards, dead_cards=dead_cards)

        mcr._reset_deck(mcr.select_hands_for_players())
        self.assertEqual(52 - 7, len(mcr.current_deck.cards))
        removed_cards = (
            he_ranges[0].possible_hands[0].cards +
            he_ranges[1].possible_hands[0].cards + board_cards + dead_cards)
        for rc in removed_cards:
            self.assertNotIn(rc, mcr.current_deck.cards)

    def test_get_best_hands_for_players(self):
        he_hands = poker_hand.parse_hands_into_holdem_hands('asad,2h2d')
        board_cards = poker_hand.parse_string_into_cards('ac,ah,kd,kc,2c')
        mcr = monte_carlo_runner.MonteCarloRunner(
            he_hands, board_cards=board_cards)

        best_hands_for_each_player = mcr._get_best_hands_for_each_player(
            mcr.select_hands_for_players(), board_cards)

        self.assertEqual(2, len(best_hands_for_each_player))

    def test_get_winning_indices(self):
        h0_short_cards = ['as', 'ad', 'qd', 'qc', 'qs']
        h0_hand = poker_hand.PokerHand(
            cards=[card.create_card_from_short_name(sn)
                   for sn in h0_short_cards])

        h1_short_cards = ['as', '2s', '3s', '4s', '5s']
        h1_hand = poker_hand.PokerHand(
            cards=[card.create_card_from_short_name(sn)
                   for sn in h1_short_cards])
        h2_short_cards = ['qs', '2s', '3s', '4s', '5s']
        h2_hand = poker_hand.PokerHand(
            cards=[card.create_card_from_short_name(sn)
                   for sn in h2_short_cards])

        index_to_hand_dict = {
            0: h0_hand,
            1: h1_hand,
            2: h2_hand,
        }

        mcr = monte_carlo_runner.MonteCarloRunner([])

        self.assertItemsEqual([1], mcr._get_winning_indices(index_to_hand_dict))

    def test_get_winning_indices_multiple_winners(self):
        h0_short_cards = ['as', 'ad', 'qd', 'qc', 'qs']
        h0_hand = poker_hand.PokerHand(
            cards=[card.create_card_from_short_name(sn)
                   for sn in h0_short_cards])
        h1_short_cards = ['as', 'ad', 'qd', 'qc', 'qs']
        h1_hand = poker_hand.PokerHand(
            cards=[card.create_card_from_short_name(sn)
                   for sn in h1_short_cards])

        index_to_hand_dict = {
            0: h0_hand,
            1: h1_hand,
        }

        mcr = monte_carlo_runner.MonteCarloRunner([])
        self.assertItemsEqual(
            [0, 1], mcr._get_winning_indices(index_to_hand_dict))



class HandDistributionTest(unittest.TestCase):
    def test_init(self):
        hd = monte_carlo_runner.HandDistribution(player_label='Xyz')

        self.assertEqual('Xyz', hd.label)
        self.assertEqual(0, hd.total_items)
        self.assertItemsEqual(poker_hand.HAND_RANKS, hd.counts)

    def test_increment_rank(self):
        hd = monte_carlo_runner.HandDistribution()

        rank_counts = {
            poker_hand.HIGH_CARD: 3,
            poker_hand.STRAIGHT: 2,
            poker_hand.FULL_HOUSE: 1,
        }
        for rank, count in rank_counts.iteritems():
            for _ in xrange(count):
                hd.increment_rank(rank, monte_carlo_runner.WIN_RESULT)

        for rank, result_dict in hd.counts.iteritems():
            self.assertEqual(rank_counts.get(rank, 0), sum(result_dict.itervalues()))
        self.assertEqual(6, hd.total_items)


if __name__ == '__main__':
    unittest.main()
