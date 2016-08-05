"""Main entry point for Hold 'em odds evaluator.

Sample invocations:
Full interactive run: $ python main_holdem_odds.py
Specific hands: $ python main_holdem_odds.py --hands=AsAd,KsKd
Specific hands without any interaction for dead cards and board cards:
    $ python main_holdem_odds.py --hands=AsAd,KsKd,2c3c --nointeraction
"""
import argparse

import monte_carlo_runner
import poker_hand


def get_player_hands(hands='', used_cards=None):
    """Determine which hands to simulate.

    Note that if we have an empty input, we can't proceed, so we forcibly
    interact with the user in that case.

    Args:
        hands: str, representation of which hands to simulate.  In the form:
            "AsAh,KsKd".
        used_cards: list of Card, cards that are not available.

    Returns:
        list of HoldemHand, the hands to simulate.
    """
    if not hands:
        print ('Please input comma separated hold em hands.  '
               'For example, ahad,kskd')
        hands = raw_input()
    return poker_hand.parse_hands_into_holdem_hands(
        hands, used_cards=used_cards)


def get_board_cards(board_cards='', interaction=True):
    """Determine which cards to place on the board initially.

    Args:
        board_cards: str, which cards should be placed on the board in every
            iteration.  For example, "As,Ah,Ad,Ac".
        interaction: bool, whether or not we should prompt the user for a value
            if the input is empty.

    Returns:
        list of Card, cards to place on the board each iteration.
    """
    if not board_cards and interaction:
        print ('Please input the board cards, separated by spaces.  '
               'For example, "Ah As"')
        board_cards = raw_input()
    return poker_hand.parse_string_into_cards(board_cards)


def get_dead_cards(dead_cards='', interaction=True):
    """Find which cards should be excluded from being selected in the sim.

    Args:
        dead_cards: str, which cards should be excluded from consideration in
            this simulation.
        interaction: bool, whether or not we should prompt the user for a value
            if the input is empty.

    Returns:
        list of Card, cards that should be excluded.
    """
    if not dead_cards and interaction:
        print ('Please input any dead cards, separated by spaces.  '
               'For example, "Ah As"')
        dead_cards = raw_input()
    return poker_hand.parse_string_into_cards(dead_cards)


def main(parsed_args):
    """Run the main program."""
    board_cards = get_board_cards(
        board_cards=parsed_args.board_cards,
        interaction=parsed_args.interaction)
    dead_cards = get_dead_cards(
        dead_cards=parsed_args.dead_cards, interaction=parsed_args.interaction)
    used_cards = board_cards + dead_cards
    player_he_hands = get_player_hands(
        hands=parsed_args.hands, used_cards=used_cards)

    mc_runner = monte_carlo_runner.MonteCarloRunner(
        player_he_hands, board_cards=board_cards, dead_cards=dead_cards,
        iterations=parsed_args.num_iterations)
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
              'AhAs,KsKd .  You may also specify generic hands, like TT, '
              'AKo, or KQs'),
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
    parser.add_argument(
        '--nointeraction',
        help='Disable interactively asking for cards.',
        action='store_false',
        dest='interaction')
    parser.set_defaults(interaction=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = _build_argparse()
    main(args)
