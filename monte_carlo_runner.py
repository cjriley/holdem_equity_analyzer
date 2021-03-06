"""Probabilistic runner for Hold em equity and hand statistics."""
import collections
import random
import time

import deck
import poker_hand

DEFAULT_ITERATIONS = 1000
WIN_RESULT = 'w'
LOSS_RESULT = 'l'
TIE_RESULT = 't'
VALID_RESULTS = frozenset([WIN_RESULT, LOSS_RESULT, TIE_RESULT])


class Error(Exception):
    pass


class HandDistribution(object):
    """Track basic statistics about a single player's hands."""
    def __init__(self, player_label='Label'):
        self.label = player_label
        self.total_items = 0
        self.counts = {}
        for rank in poker_hand.HAND_RANKS.iterkeys():
            self.counts[rank] = {}
            for result in VALID_RESULTS:
                self.counts[rank][result] = 0

    def increment_rank(self, rank, result):
        """Increment the proper counter for the rank.

        Args:
            rank: str, the rank of the hand to record.
            result: str, one of the above results.
        """
        if result not in VALID_RESULTS:
            raise ValueError('Invalid result: %s' % result)
        self.counts[rank][result] += 1
        self.total_items += 1

    def print_report(self):
        """Prints out stats about the hand distribution."""
        print '=' * 20 + ' %s ' % self.label + '=' * 20
        print '%-20s%5s\t%4s\t%4s\t%4s\t%4s' % (
            'Hand' + '=' * 16, '#', 'Frac', 'W', 'Tie', 'L')
        for hand, result_dict in self.counts.iteritems():
            total_for_hand = sum(result_dict.itervalues())
            if total_for_hand == 0:
                win_frac = 0.0
                tie_frac = 0.0
                loss_frac = 0.0
            else:
                win_frac = float(result_dict[WIN_RESULT])/total_for_hand
                tie_frac = float(result_dict[TIE_RESULT])/total_for_hand
                loss_frac = float(
                    result_dict[LOSS_RESULT])/total_for_hand
            print '%-20s%5d\t%0.3f\t%0.3f\t%0.3f\t%0.3f' % (
                hand, total_for_hand, float(total_for_hand)/self.total_items,
                win_frac, tie_frac, loss_frac)


class MonteCarloRunner(object):
    """Runs a Monte Carlo simulation of Hold em and outputs equity stats."""
    def __init__(self, holdem_ranges, board_cards=None, dead_cards=None,
                 iterations=DEFAULT_ITERATIONS):
        self._validate_input_specification(
            holdem_ranges, board_cards or [], dead_cards or [])
        self.holdem_ranges = holdem_ranges
        self.board_cards = board_cards
        self.dead_cards = dead_cards
        self.iterations = iterations

        self.current_deck = None
        self.start_time = 0
        self.elapsed_time = 0

        # Hand index to number of wins.
        self.win_stats = collections.defaultdict(float)
        self.player_stats = []
        for hand in self.holdem_ranges:
            self.player_stats.append(
                HandDistribution(player_label=str(hand)))

    def _validate_input_specification(
            self, holdem_ranges, board_cards, dead_cards):
        """Sanity check for the input.

        Ensures that cards aren't specified multiple times.
        """
        explicit_card_count = collections.defaultdict(int)
        for c in (board_cards + dead_cards) or ():
            explicit_card_count[c] += 1

        for her in holdem_ranges:
            if len(her.possible_hands) == 1:
                for c in her.possible_hands[0].cards:
                    explicit_card_count[c] += 1

        multiple_specified_cards = []
        for card, count in explicit_card_count.iteritems():
            if count > 1:
                multiple_specified_cards.append(card)
        if multiple_specified_cards:
            raise Error('Cards specified multiple times: %s' % (
                ','.join('%s' % c for c in multiple_specified_cards)))

    def _reset_deck(self, player_starting_hands):
        if not self.current_deck:
            self.current_deck = deck.Deck()
        self.current_deck.reset_and_shuffle()

        cards_to_remove = self.board_cards + self.dead_cards
        for h in player_starting_hands:
            cards_to_remove.extend(h.cards)

        self.current_deck.remove_cards_from_deck(cards_to_remove)

    def print_statistics(self):
        """Print out statistics about equity along with final hand counts."""
        print 'Ran %s iterations in %0.3f seconds\n' % (
            self.iterations, self.elapsed_time)

        print 'Overall Equity'
        for index in range(len(self.holdem_ranges)):
            range_short_form = '%r' % self.holdem_ranges[index]
            print 'P%s)  %-15s %0.3f' % (
                index,
                range_short_form,
                float(self.win_stats.get(index, 0))/self.iterations)
        print '\n'
        print 'Hand distribution for each player'
        for stats in self.player_stats:
            stats.print_report()

    def run_all_iterations(self):
        """Run the specified number of iterations and print out stats."""
        self.start_time = time.time()
        for _ in xrange(self.iterations):
            self.run_iteration()
        self.elapsed_time = time.time() - self.start_time

        self.print_statistics()

    def _get_best_hands_for_each_player(
            self, player_hands, iteration_board_cards):
        """Find the best hand for each player, given the board.

        Args:
            iteration_board_cards: list of Card, the cards that are present on
                the board for this hand.
            player_hands: list of HoldemHand, each player's starting hand.

        Returns:
            dict, mapping player indices to their best hand for this hand.
        """
        index_to_best_hands = {}
        for idx, player_hand in enumerate(player_hands):
            best_hand_for_player = poker_hand.get_best_hand_from_cards(
                list(player_hand.cards) + iteration_board_cards)
            index_to_best_hands[idx] = best_hand_for_player
        return index_to_best_hands

    def _get_winning_indices(self, index_to_best_hands):
        """Determine which player or players won the hand.

        Args:
            index_to_best_hands: dict, mapping player_index to their best
                poker hand for this iteration.

        Returns:
            list of int, the player indices that won or tied for the winning
                hand.
        """
        winning_indices = []
        winning_hand = None
        for idx, best_hand in index_to_best_hands.iteritems():
            if not winning_indices:
                winning_indices.append(idx)
                winning_hand = best_hand
                continue
            if best_hand > winning_hand:
                winning_indices = [idx]
                winning_hand = best_hand
            elif best_hand == winning_hand:
                winning_indices.append(idx)
        return winning_indices

    def select_hands_for_players(self):
        """Randomly selects hands for each player.

        Returns:
            list of HoldemHand, which specific hand to use for each player.
        """
        return [random.choice(h.possible_hands) for h in self.holdem_ranges]

    def run_iteration(self):
        """Run a single iteration of the simulation."""
        # Choose the player's starting hands and remove from deck.
        starting_hands_for_players = self.select_hands_for_players()
        self._reset_deck(starting_hands_for_players)

        # Finish the board
        iteration_board_cards = self.board_cards[:]
        while len(iteration_board_cards) < 5:
            iteration_board_cards.append(self.current_deck.pop())

        index_to_best_hands = self._get_best_hands_for_each_player(
            starting_hands_for_players, iteration_board_cards)
        winning_indices = self._get_winning_indices(index_to_best_hands)

        # Now update the statistics.
        for idx in winning_indices:
            self.win_stats[idx] += 1.0 / len(winning_indices)
        for idx, best_hand in index_to_best_hands.iteritems():
            if idx in winning_indices:
                if len(winning_indices) > 1:
                    self.player_stats[idx].increment_rank(
                        best_hand.hand_rank, TIE_RESULT)
                else:
                    self.player_stats[idx].increment_rank(
                        best_hand.hand_rank, WIN_RESULT)
            else:
                self.player_stats[idx].increment_rank(
                    best_hand.hand_rank, LOSS_RESULT)

