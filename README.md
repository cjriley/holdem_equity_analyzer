# Texas Hold 'em Equity and Hand Distribution

## Introduction

This is a command line utility that allows you to specify various game states
in Texas Hold 'em and outputs each hand's equity, along with the hand
distribution each hand will end up with.

### Stats explanation

##### Equity
The fraction output here indicates what portion of the current pot the player
would expect to win.  For example, when we run two hands, both of which are the
same pocket pair, the equity of each player is around .5.  The hand will
always end in a tie except when there are 4 to a suit on board and one of the
players has a flush (and this will be equally distributed on each side under
normal circumstances).

##### Hand Distribution
This just counts up the number of times each starting hand ends up with a
specific hand.


### Basic invocations

Run an interactive version of the script:

    python ./main_holdem_odds.py

    Please input comma separated hold em hands.  For example, ahad,kskd
    AsAd,QsQc,7h6h
    Please input the board cards, separated by spaces.  For example, "Ah As"

    Please input any dead cards, separated by spaces.  For example, "Ah As"

    Ran 1000 iterations in 1.445 seconds

    Overall Equity
    P0)  As Ad           0.575
    P1)  Qs Qc           0.210
    P2)  7h 6h           0.214


    Hand distribution for each player
    ==================== P0 AsAd ====================
    Four-of-a-kind          11      0.011
    Two pair               371      0.371
    Three-of-a-kind        122      0.122
    Straight                18      0.018
    Flush                   34      0.034
    Straight Flush           0      0.000
    High Card                0      0.000
    One pair               346      0.346
    Full House              98      0.098
    ==================== P1 QsQc ====================
    Four-of-a-kind          10      0.010
    Two pair               376      0.376
    Three-of-a-kind        123      0.123
    Straight                16      0.016
    Flush                   30      0.030
    Straight Flush           0      0.000
    High Card                0      0.000
    One pair               354      0.354
    Full House              91      0.091
    ==================== P2 7h6h ====================
    Four-of-a-kind           2      0.002
    Two pair               229      0.229
    Three-of-a-kind         48      0.048
    Straight               117      0.117
    Flush                   67      0.067
    Straight Flush           4      0.004
    High Card              130      0.130
    One pair               385      0.385
    Full House              18      0.018
    python ./main_holdem_odds.py


Run a non-interactive version.

    python ./main_holdem_odds.py --hands=2c3c,TsTd --nointeraction

    Ran 1000 iterations in 1.097 seconds

    Overall Equity
    P0)  2c 3c           0.213
    P1)  Ts Td           0.787


    Hand distribution for each player
    ==================== P0 2c3c ====================
    Four-of-a-kind           3      0.003
    Two pair               222      0.222
    Three-of-a-kind         55      0.055
    Straight                50      0.050
    Flush                   74      0.074
    Straight Flush           1      0.001
    High Card              149      0.149
    One pair               431      0.431
    Full House              15      0.015
    ==================== P1 TsTd ====================
    Four-of-a-kind          10      0.010
    Two pair               380      0.380
    Three-of-a-kind        113      0.113
    Straight                30      0.030
    Flush                   13      0.013
    Straight Flush           0      0.000
    High Card                0      0.000
    One pair               358      0.358
    Full House              96      0.096

Specify a board:

    python ./main_holdem_odds.py --hands=2c3c,TsTd --board_cards=4c5cTh --nointeraction

    Ran 1000 iterations in 1.038 seconds

    Overall Equity
    P0)  2c 3c           0.441
    P1)  Ts Td           0.559


    Hand distribution for each player
    ==================== P0 2c3c ====================
    Four-of-a-kind           0      0.000
    Two pair                52      0.052
    Three-of-a-kind          6      0.006
    Straight               195      0.195
    Flush                  276      0.276
    Straight Flush         111      0.111
    High Card              132      0.132
    One pair               228      0.228
    Full House               0      0.000
    ==================== P1 TsTd ====================
    Four-of-a-kind          44      0.044
    Two pair                 0      0.000
    Three-of-a-kind        662      0.662
    Straight                 0      0.000
    Flush                    0      0.000
    Straight Flush           0      0.000
    High Card                0      0.000
    One pair                 0      0.000
    Full House             294      0.294 
