import unittest

import card
import monte_carlo_runner
import poker_hand

class MonteCarloRunnerTest(unittest.TestCase):
    def test_reset_deck(self):
        he_hands = poker_hand.parse_hands_into_holdem_hands('asad,qsjh')
        board_cards = poker_hand.parse_string_into_cards('2c2d')

        dead_cards = poker_hand.parse_string_into_cards('8h')

        mcr = monte_carlo_runner.MonteCarloRunner(
            he_hands, board_cards=board_cards, dead_cards=dead_cards)
        
        mcr._reset_deck()
        self.assertEqual(52 - 7, len(mcr.current_deck.cards))
        removed_cards = (
            he_hands[0].cards + he_hands[1].cards + board_cards + dead_cards)
        for rc in removed_cards:
            self.assertNotIn(rc, mcr.current_deck.cards)

