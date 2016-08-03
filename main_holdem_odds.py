import argparse

import monte_carlo_runner
import poker_hand

def get_player_hands():
    print 'Please input comma separated hold em hands.  For example, ahad,kskd'
    hands = raw_input()
    return poker_hand.parse_hands_into_holdem_hands(hands)

def get_board_cards():
    print 'Please input the board cards, separated by spaces.  For example, "Ah As"'
    board_cards = raw_input()
    return poker_hand.parse_string_into_cards(board_cards)

def get_dead_cards():
    print 'Please input any dead cards, separated by spaces.  For example, "Ah As"'
    board_cards = raw_input()
    return poker_hand.parse_string_into_cards(board_cards)

def main(args):
    player_he_hands = get_player_hands()
    board_cards = get_board_cards()
    dead_cards = get_dead_cards()

    mc_runner = monte_carlo_runner.MonteCarloRunner(
        player_he_hands, board_cards=board_cards, dead_cards=dead_cards)
    mc_runner.run_all_iterations()

def _build_argparse():
    return None

if __name__ == '__main__':
    args = _build_argparse()
    main(args)
