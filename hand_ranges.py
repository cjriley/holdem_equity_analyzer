import itertools

import card
import poker_hand

class Error(Exception):
    pass


class HandDescriptionParseError(Error):
    """Raised if we are unable to parse a description of a hand."""


def single_hand_description_to_hands(description, dead_cards=None):
    description = description.lower()

    # Pairs are the same character twice.
    if len(description) == 2 and description[0] == description[1]:
        short_rank = description[0]
        if short_rank not in card.SHORT_RANKS_TO_FULL_RANKS:
            raise HandDescriptionParseError('Rank %s is invalid' % short_rank)
        full_rank = card.SHORT_RANKS_TO_FULL_RANKS[short_rank]
        return generate_pair_hands(full_rank, dead_cards=dead_cards)

    if len(description) == 3 and description[2] in ('o', 's'):
        short_rank1 = description[0]
        short_rank2 = description[1]
        if (short_rank1 not in card.SHORT_RANKS_TO_FULL_RANKS or
            short_rank2 not in card.SHORT_RANKS_TO_FULL_RANKS):
            raise HandDescriptionParseError(
                'Rank %s or %s is invalid' % (short_rank1, short_rank2))
        full_rank1 = card.SHORT_RANKS_TO_FULL_RANKS[short_rank1]
        full_rank2 = card.SHORT_RANKS_TO_FULL_RANKS[short_rank2]
        if description[2] == 'o':
            return generate_unsuited_hands(
                full_rank1, full_rank2, dead_cards=dead_cards)
        elif description[2] == 's':
            return generate_suited_hands(
                full_rank1, full_rank2, dead_cards=dead_cards)
    raise HandDescriptionParseError('Invalid hand description: %s' % description)

def generate_pair_hands(rank, dead_cards=None):
    """Generates all possible pair hands for the given rank."""
    if rank not in card.RANKS:
        raise ValueError('Invalid rank: %s' % rank)

    cards = [card.Card(s, rank) for s in card.SUITS]
    filtered_cards = cards
    if dead_cards:
        filtered_cards = [c for c in cards if c not in dead_cards]

    return [poker_hand.HoldemHand(cards=c)
            for c in itertools.combinations(filtered_cards, 2)] 

def generate_suited_hands(rank1, rank2, dead_cards=None):
    hands = []
    for suit in card.SUITS:
        c1 = card.Card(suit, rank1)
        c2 = card.Card(suit, rank2)
        if dead_cards and (c1 in dead_cards or c2 in dead_cards):
            continue
        hands.append(poker_hand.HoldemHand(cards=[c1, c2]))
    return hands

def generate_unsuited_hands(rank1, rank2, dead_cards=None):
    c1_possibilities = [card.Card(s, rank1) for s in card.SUITS]
    c2_possibilities = [card.Card(s, rank2) for s in card.SUITS]

    hands = []
    for c1 in c1_possibilities:
        if dead_cards and c1 in dead_cards:
            continue
        for c2 in c2_possibilities:
            if dead_cards and c2 in dead_cards:
                continue
            if c1.suit == c2.suit:
                continue
            hands.append(poker_hand.HoldemHand(cards=[c1, c2]))
    return hands





