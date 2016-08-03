"""Constants and class related to Card representations."""
SUITS = {
    'Clubs': 0,
    'Diamonds': 1,
    'Hearts': 2,
    'Spades': 3,
}
RANKS = {
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 11,
    'Queen': 12,
    'King': 13,
    'Ace': 14,
}

SHORT_RANKS_TO_FULL_RANKS = {
    '2': 'Two',
    '3': 'Three',
    '4': 'Four',
    '5': 'Five',
    '6': 'Six',
    '7': 'Seven',
    '8': 'Eight',
    '9': 'Nine',
    't': 'Ten',
    'j': 'Jack',
    'q': 'Queen',
    'k': 'King',
    'a': 'Ace',
}
SHORT_SUITS_TO_FULL_SUITS = {
    'c': 'Clubs',
    'd': 'Diamonds',
    'h': 'Hearts',
    's': 'Spades'
}


def create_card_from_short_name(short_name):
    """Creates a card object from the short name of a card.

    e.g. Th is the ten of hearts.

    Args:
        short_name: str, describes the card in a short form.

    Returns:
        Card, new object with the specified suit and rank.
    """
    if len(short_name) != 2:
        raise ValueError('Invalid short name for card: %s' % short_name)

    short_name = short_name.lower()
    rank_char = short_name[0]
    suit_char = short_name[1]

    if rank_char not in SHORT_RANKS_TO_FULL_RANKS:
        raise ValueError('Invalid rank character: %s' % rank_char)
    if suit_char not in SHORT_SUITS_TO_FULL_SUITS:
        raise ValueError('Invalid suit character: %s' % suit_char)

    return Card(SHORT_SUITS_TO_FULL_SUITS[suit_char],
                SHORT_RANKS_TO_FULL_RANKS[rank_char])


class Card(object):
    """Suit and rank representation for a card."""
    def __init__(self, suit, rank):
        if suit not in SUITS:
            raise ValueError('Invalid suit: %s' % suit)
        if rank not in RANKS:
            raise ValueError('Invalid rank: %s' % rank)

        self.suit = suit
        self.rank = rank
        self.rank_index = RANKS[rank]

    # TODO: Needs testing and needs to be more efficient.
    def short_form(self):
        """Get the short form string for the card."""
        result = ''
        for short_name, full_name in SHORT_RANKS_TO_FULL_RANKS.iteritems():
            if full_name == self.rank:
                result += short_name.upper()
        for short_name, full_name in SHORT_SUITS_TO_FULL_SUITS.iteritems():
            if full_name == self.suit:
                result += short_name
        return result

    def __repr__(self):
        return '%s of %s' % (self.rank, self.suit)

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def __hash__(self):
        return self.__repr__().__hash__()

