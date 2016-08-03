import card
import collections
import itertools

PokerHand = collections.namedtuple('PokerHand', ['cards'])
# Should consist of exactly two cards.
HoldemHand = collections.namedtuple('HoldemHand', ['cards'])

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
    # Strip it down to characters only.
    card_input = card_input.lower().replace(' ', '').replace(',', '')
    cards = []
    for short_name_tuple in zip(card_input[::2], card_input[1::2]):
        cards.append(card.create_card_from_short_name(''.join(short_name_tuple)))
    return cards


def compare_poker_hands(lhs, rhs):
    """Compares the two hands.

    Args:
        lhs: PokerHand.
        rhs: PokerHand.

    Returns:
        int, a positive number if the lhs hand ranks higher, a negative number
            if the rhs hand ranks higher, and zero if they are equal.
    """
    lhs_rank = get_hand_rank(lhs)
    rhs_rank = get_hand_rank(rhs)
    if HAND_RANKS[lhs_rank] > HAND_RANKS[rhs_rank]:
        return -1
    elif HAND_RANKS[lhs_rank] < HAND_RANKS[rhs_rank]:
        return 1
    return compare_secondary_ranks(lhs, rhs, lhs_rank)

def compare_secondary_ranks(lhs, rhs, rank):
    # Special case for ace_to_five straights
    if _is_ace_to_five_straight(lhs):
        if _is_ace_to_five_straight(rhs):
            return 0
        return 1
    elif _is_ace_to_five_straight(rhs):
        return -1

    lhs_buckets = _build_rank_buckets_from_hand(lhs)
    lhs_relevant_ranks = [k for k in sorted(
        lhs_buckets, key=lambda k: -lhs_buckets[k])]
    rhs_buckets = _build_rank_buckets_from_hand(rhs)
    rhs_relevant_ranks = [k for k in sorted(
        rhs_buckets, key=lambda k: -rhs_buckets[k])]
    for lhs_rank, rhs_rank in zip(lhs_relevant_ranks, rhs_relevant_ranks):
        if lhs_rank != rhs_rank:
            return rhs_rank - lhs_rank
    return 0


def get_hand_rank(hand):
    """Gets the rank of the poker hand."""
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
    rank_buckets = collections.defaultdict(int)
    for card in hand.cards:
        rank_buckets[card.rank_index] += 1
    return rank_buckets

def _contains_exactly_x_of_a_kind(hand, num):
    rank_buckets = _build_rank_buckets_from_hand(hand)
    for count in rank_buckets.itervalues():
        if count == num:
            return True
    return False

# TODO:  This will return false for two pair hands right now.  Is that the 
#        behavior we want?
def contains_one_pair(hand):
    return (_contains_exactly_x_of_a_kind(hand, 2) and
            not contains_two_pair(hand))

def contains_two_pair(hand):
    rank_buckets = _build_rank_buckets_from_hand(hand)
    has_pair = False
    for count in rank_buckets.itervalues():
        if count == 2:
            if has_pair:
                return True
            has_pair = True
    return False
            



def contains_full_house(hand):
    return (_contains_exactly_x_of_a_kind(hand, 3) and 
            _contains_exactly_x_of_a_kind(hand, 2))

def contains_four_of_a_kind(hand):
    return _contains_exactly_x_of_a_kind(hand, 4)

def contains_three_of_a_kind(hand):
    return _contains_exactly_x_of_a_kind(hand, 3)

def contains_straight_flush(hand):
    return contains_flush(hand) and contains_straight(hand)

def contains_flush(hand):
    """Determine if the given hand contains a flush (all cards same suit)."""
    suit_set = set(c.suit for c in hand.cards)
    return len(suit_set) == 1

def _is_ace_to_five_straight(sorted_ranks):
    return sorted_ranks == [2, 3, 4, 5, 14]

def contains_straight(hand):
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
    best_hand = None
    for five_cards in itertools.combinations(cards, 5):
        if not best_hand:
            best_hand = PokerHand(cards=five_cards)
            continue
        five_card_hand = PokerHand(cards=five_cards)
        compare_result = compare_poker_hands(five_card_hand, best_hand)
        if compare_result >= 0:
            continue
        best_hand = five_card_hand
    return best_hand

