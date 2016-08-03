import argparse

import monte_carlo_runner
import poker_hand


def get_player_hands(hands=None):
    if not hands:
        print 'Please input comma separated hold em hands.  For example, ahad,kskd'
        hands = raw_input()
    return poker_hand.parse_hands_into_holdem_hands(hands)


def get_board_cards(board_cards=None):
    if not board_cards:
        print 'Please input the board cards, separated by spaces.  For example, "Ah As"'
        board_cards = raw_input()
    return poker_hand.parse_string_into_cards(board_cards)


def get_dead_cards(dead_cards=None):
    if not dead_cards:
        print 'Please input any dead cards, separated by spaces.  For example, "Ah As"'
        dead_cards = raw_input()
    return poker_hand.parse_string_into_cards(dead_cards)


def main(args):
    player_he_hands = get_player_hands(hands=args.hands)
    board_cards = get_board_cards(board_cards=args.board_cards)
    dead_cards = get_dead_cards(dead_cards=args.dead_cards)

    mc_runner = monte_carlo_runner.MonteCarloRunner(
        player_he_hands, board_cards=board_cards, dead_cards=dead_cards,
        iterations=args.num_iterations)
    mc_runner.run_all_iterations()


def _build_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--num_iterations', help='Number of iterations to run.',
        type=int, default=1000)
    parser.add_argument(
        '--hands',
        help=('Hands to test.  If not specified, these will be provided '
              'interactively. Format should be comma separated, e.g. '
              'AhAs,KsKd .'),
        type=str, default='')
    parser.add_argument(
        '--board_cards',
        help=('Cards on the board.  If not specified, these will be provided '
              'interactively.'),
        type=str, default='')
    parser.add_argument(
        '--dead_cards',
        help=('Dead cards.  These will be excluded from consideration in '
              'the hands.'),
        type=str, default='')

    return parser.parse_args()


if __name__ == '__main__':
    args = _build_argparse()
    main(args)
