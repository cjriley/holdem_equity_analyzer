import collections
import itertools

import card
import deck
import poker_hand

DEFAULT_ITERATIONS = 1000

class MonteCarloRunner(object):
    def __init__(self, holdem_hands, board_cards=None, dead_cards=None,
            iterations=DEFAULT_ITERATIONS):
        self.holdem_hands = holdem_hands
        self.board_cards = board_cards
        self.dead_cards = dead_cards
        self.iterations = iterations

        self.current_deck = None

        # Hand index to number of wins.
        self.win_stats = collections.defaultdict(int)

    def _reset_deck(self):
        if not self.current_deck:
            self.current_deck = deck.Deck()
        self.current_deck.reset_and_shuffle()

        cards_to_remove = self.board_cards + self.dead_cards
        for h in self.holdem_hands:
            cards_to_remove.extend(h.cards)

        self.current_deck.remove_cards_from_deck(cards_to_remove)

    def print_statistics(self):
        for index, wins in self.win_stats.iteritems():
            print '%s ==> %s' % (index, wins)
        for index in range(len(self.holdem_hands)):
            hand_short_form = ' '.join(c.short_form() for c in self.holdem_hands[index].cards)
            print 'P%s)%-15s %0.3f' % (
                index,
                hand_short_form,
                float(self.win_stats.get(index, 0))/self.iterations)

    def run_all_iterations(self):
        for idx in xrange(self.iterations):
            self.run_iteration()

        self.print_statistics()


    def run_iteration(self):
        self._reset_deck()
        
        # Finish the board
        iteration_board_cards = self.board_cards[:]
        while len(iteration_board_cards) < 5:
            iteration_board_cards.append(self.current_deck.pop())

        index_to_best_hands = {}
        for idx, holdem_hand in enumerate(self.holdem_hands):
            index_to_best_hands[idx] = poker_hand.get_best_hand_from_cards(
                holdem_hand.cards + iteration_board_cards)

        # Now update the statistics.
        winning_indices = []
        winning_hand = None
        for idx, best_hand in index_to_best_hands.iteritems():
            if not winning_indices:
                winning_indices.append(idx)
                winning_hand = best_hand
                continue
            comparison_result = poker_hand.compare_poker_hands(
                best_hand, winning_hand)
            if comparison_result == 0:
                winning_indices.append(idx)
                continue
            if comparison_result < 0:
                winning_indices = [idx]
                winning_hand = best_hand

        for idx in winning_indices:
            self.win_stats[idx] += 1
        # TODO update hand stats as well.

