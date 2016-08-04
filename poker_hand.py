"""Representations and evaluations of Poker hands."""
import card
import collections
import itertools

HIGH_CARD = 'High Card'
ONE_PAIR = 'One pair'
TWO_PAIR = 'Two pair'
THREE_OF_A_KIND = 'Three-of-a-kind'
STRAIGHT = 'Straight'
FLUSH = 'Flush'
FULL_HOUSE = 'Full House'
FOUR_OF_A_KIND = 'Four-of-a-kind'
STRAIGHT_FLUSH = 'Straight Flush'

HAND_RANKS = {
    HIGH_CARD: 0,
    ONE_PAIR: 1,
    TWO_PAIR: 2,
    THREE_OF_A_KIND: 3,
    STRAIGHT: 4,
    FLUSH: 5,
    FULL_HOUSE: 6,
    FOUR_OF_A_KIND: 7,
    STRAIGHT_FLUSH: 8,
}


class PokerHand(object):
    """Represents a five card poker hand."""
    def __init__(self, cards=None):
        self.cards = cards
        self.hand_rank = get_hand_rank(self)
        self.hand_rank_index = HAND_RANKS[self.hand_rank]
        self.sorted_ranks = sorted(c.rank_index for c in cards)

    def __eq__(self, other):
        return (self.hand_rank_index == other.hand_rank_index and
                compare_secondary_ranks(self, other) == 0)

    def __lt__(self, rhs):
        if self.hand_rank_index < rhs.hand_rank_index:
            return True
        elif self.hand_rank_index > rhs.hand_rank_index:
            return False

        # Compare secondary ranks returns < 0 if RHS is a "better" hand.
        return compare_secondary_ranks(self, rhs) < 0

    def __gt__(self, other):
        return (not self.__lt__(other) and
                not self == other)

    def __le__(self, other):
        return self.__lt__(other) or self == other


class HoldemHand(object):
    """Representation of a holdem hand."""
    def __init__(self, cards=None):
        self.cards = cards
        self.as_set = set(cards)

    def __eq__(self, other):
        return self.as_set == other.as_set

    def __hash__(self, other):
        return str(self.as_set).__hash__()


class HoldemHandRange(object):
    def __init__(self, possible_hands):
        self.possible_hands = possible_hands


def parse_hands_into_holdem_hands(hand_input):
    """Split the string into holdem hands.

    Args:
        hand_input: str, comma separated string of concatenated short card
            names.  For example: "ahad,kskc,qdqc".  Space is ignored.

    Returns:
        list of HoldemHand.
    """
    holdem_hands = []
    hands = hand_input.replace(' ', '').lower().split(',')
    for hand in hands:
        he_hand = HoldemHand(cards=parse_string_into_cards(hand))
        holdem_hands.append(he_hand)
    return holdem_hands


def parse_string_into_cards(card_input):
    """Parses a string of characters into Card objects.

    Args:
        card_input: str, representing cards.  May be space or comma separated.

    Returns:
        list of Cards.
    """
    # Strip it down to characters only.
    card_input = card_input.lower().replace(' ', '').replace(',', '')
    cards = []
    for short_name_tuple in zip(card_input[::2], card_input[1::2]):
        cards.append(
            card.create_card_from_short_name(''.join(short_name_tuple)))
    return cards


def compare_secondary_ranks(lhs, rhs):
    """Determine which of the two hands is ranked higher.

    This assumes that the hands are of the same rank.

    Args:
        lhs: PokerHand.
        rhs: PokerHand.

    Returns:
        int, -1 if the lhs hand ranks LOWER.  1 if the rhs hand ranks LOWER. 0
            if they rank equally.

    Raises:
        ValueError if the hands are not of the same rank.
    """
    if lhs.hand_rank != rhs.hand_rank:
        raise ValueError(
            'Hands must be of the same rank to use secondary ranks')

    # Special case for ace_to_five straights
    if _is_ace_to_five_straight(lhs.sorted_ranks):
        if _is_ace_to_five_straight(rhs.sorted_ranks):
            return 0
        return -1
    elif _is_ace_to_five_straight(rhs.sorted_ranks):
        return 1

    lhs_buckets = _build_rank_buckets_from_hand(lhs)
    lhs_relevant_ranks = [k for k in sorted(
        lhs_buckets, key=lambda k: -lhs_buckets[k])]
    rhs_buckets = _build_rank_buckets_from_hand(rhs)
    rhs_relevant_ranks = [k for k in sorted(
        rhs_buckets, key=lambda k: -rhs_buckets[k])]
    for lhs_rank, rhs_rank in zip(lhs_relevant_ranks, rhs_relevant_ranks):
        if lhs_rank != rhs_rank:
            return lhs_rank - rhs_rank
    return 0


def get_hand_rank(hand):
    """Gets the rank of the poker hand.

    Args:
        hand: PokerHand.

    Returns:
        str, key of RANKS.
    """
    if contains_straight_flush(hand):
        return STRAIGHT_FLUSH
    if contains_four_of_a_kind(hand):
        return FOUR_OF_A_KIND
    if contains_full_house(hand):
        return FULL_HOUSE
    if contains_flush(hand):
        return FLUSH
    if contains_straight(hand):
        return STRAIGHT
    if contains_three_of_a_kind(hand):
        return THREE_OF_A_KIND
    if contains_two_pair(hand):
        return TWO_PAIR
    if contains_one_pair(hand):
        return ONE_PAIR
    return HIGH_CARD


def _build_rank_buckets_from_hand(hand):
    """Builds up a dict mapping rank to counts within the hand."""
    rank_buckets = collections.defaultdict(int)
    for c in hand.cards:
        rank_buckets[c.rank_index] += 1
    return rank_buckets


def _contains_exactly_x_of_a_kind(hand, num):
    rank_buckets = _build_rank_buckets_from_hand(hand)
    for count in rank_buckets.itervalues():
        if count == num:
            return True
    return False


def contains_one_pair(hand):
    """Determine if a hand contains exactly one pair.

    Args:
        hand: PokerHand.

    Returns:
        bool, indicating whether or not the hand contains exactly one pair.
    """
    return (_contains_exactly_x_of_a_kind(hand, 2) and
            not contains_two_pair(hand))


def contains_two_pair(hand):
    """Determine if a hand contains two pair.

    Args:
        hand: PokerHand.

    Returns:
        bool, indicating whether or not the hand contains two pair.
    """
    rank_buckets = _build_rank_buckets_from_hand(hand)
    has_pair = False
    for count in rank_buckets.itervalues():
        if count == 2:
            if has_pair:
                return True
            has_pair = True
    return False


def contains_full_house(hand):
    """Determine if a hand contains a full house.

    Args:
        hand: PokerHand.

    Returns:
        bool, indicating whether or not the hand contains a full house.
    """

    return (_contains_exactly_x_of_a_kind(hand, 3) and
            _contains_exactly_x_of_a_kind(hand, 2))


def contains_four_of_a_kind(hand):
    """Determine if a hand contains four of a kind.

    Args:
        hand: PokerHand.

    Returns:
        bool, indicating whether or not the hand contains four of a kind.
    """
    return _contains_exactly_x_of_a_kind(hand, 4)


def contains_three_of_a_kind(hand):
    """Determine if a hand contains three of a kind.

    Args:
        hand: PokerHand.

    Returns:
        bool, indicating whether or not the hand contains three of a kind.
    """
    return _contains_exactly_x_of_a_kind(hand, 3)

def contains_straight_flush(hand):
    """Determine if a hand contains a straight flush.

    Args:
        hand: PokerHand.

    Returns:
        bool, indicating whether or not the hand contains a straight flush.
    """
    return contains_flush(hand) and contains_straight(hand)


def contains_flush(hand):
    """Determine if the given hand contains a flush.

    Args:
        hand: PokerHand.

    Returns:
        bool, whether or not the hand contains a flush.
    """
    suit_set = set(c.suit for c in hand.cards)
    return len(suit_set) == 1


def _is_ace_to_five_straight(sorted_ranks):
    """Special case for the ace-to-five straight."""
    return sorted_ranks == [2, 3, 4, 5, 14]


def contains_straight(hand):
    """Determine if the hand contains a straight.

    Args:
        hand: PokerHand.

    Returns:
        bool, whether or not the hand contains a straight.
    """
    sorted_rank_index = sorted(c.rank_index for c in hand.cards)

    # Special case of the ace to five straight.
    if _is_ace_to_five_straight(sorted_rank_index):
        return True

    expected_rank = sorted_rank_index[0] + 1
    for rank_index in sorted_rank_index[1:]:
        if rank_index != expected_rank:
            return False
        expected_rank += 1
    return True


def get_best_hand_from_cards(cards):
    """Finds the highest ranked five-card hand from all combinations of cards.

    Args:
        cards: list of Cards.

    Returns:
        PokerHand, the highest ranking poker hand possible, given the
            collection of cards input.
    """
    best_hand = None
    for five_cards in itertools.combinations(cards, 5):
        if not best_hand:
            best_hand = PokerHand(cards=five_cards)
            continue
        five_card_hand = PokerHand(cards=five_cards)
        best_hand = max(best_hand, five_card_hand)
    return best_hand

