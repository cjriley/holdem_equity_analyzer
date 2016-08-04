# Texas Hold 'em Equity and Hand Distribution

## Introduction

This is a command line utility that allows you to specify various game states
in Texas Hold 'em and outputs each hand's equity, along with the hand
distribution each hand will end up with.

### Usage

    usage: main_holdem_odds.py [-h] [--num_iterations NUM_ITERATIONS]
                               [--hands HANDS] [--board_cards BOARD_CARDS]
                               [--dead_cards DEAD_CARDS] [--nointeraction]

    optional arguments:
      -h, --help            show this help message and exit
      --num_iterations NUM_ITERATIONS
                            Number of iterations to run.
      --hands HANDS         Hands to test. If not specified, these will be
                            provided interactively. Format should be comma
                            separated, e.g. AhAs,KsKd . You may also specify
                            generic hands, like TT, AKo, or KQs
      --board_cards BOARD_CARDS
                            Cards on the board. If not specified, these will be
                            provided interactively.
      --dead_cards DEAD_CARDS
                            Dead cards. These will be excluded from consideration
                            in the hands.
      --nointeraction       Disable interactively asking for cards.

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

    Overall Equity
    P0)  AsAd            0.575
    P1)  QsQc            0.200
    P2)  7h6h            0.226


    Hand distribution for each player
    ==================== AsAd ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind         15       0.015   1.000   0.000   0.000
    Two pair              383       0.383   0.556   0.000   0.444
    Three-of-a-kind       123       0.123   0.732   0.000   0.268
    Straight               18       0.018   0.278   0.111   0.611
    Flush                  17       0.017   0.471   0.000   0.529
    Straight Flush          0       0.000   0.000   0.000   0.000
    High Card               0       0.000   0.000   0.000   0.000
    One pair              351       0.351   0.436   0.000   0.564
    Full House             93       0.093   0.968   0.000   0.032
    ==================== QsQc ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind          9       0.009   1.000   0.000   0.000
    Two pair              392       0.392   0.069   0.000   0.931
    Three-of-a-kind       125       0.125   0.560   0.000   0.440
    Straight               25       0.025   0.720   0.080   0.200
    Flush                  19       0.019   0.737   0.000   0.263
    Straight Flush          0       0.000   0.000   0.000   0.000
    High Card               0       0.000   0.000   0.000   0.000
    One pair              340       0.340   0.000   0.000   1.000
    Full House             90       0.090   0.678   0.000   0.322
    ==================== 7h6h ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind          1       0.001   1.000   0.000   0.000
    Two pair              254       0.254   0.161   0.000   0.839
    Three-of-a-kind        44       0.044   0.545   0.000   0.455
    Straight               88       0.088   0.795   0.023   0.182
    Flush                  99       0.099   0.747   0.000   0.253
    Straight Flush          4       0.004   1.000   0.000   0.000
    High Card             142       0.142   0.000   0.000   1.000
    One pair              340       0.340   0.000   0.000   1.000
    Full House             28       0.028   0.393   0.000   0.607


Run a non-interactive version.

    python ./main_holdem_odds.py --hands=2c3c,TsTd --nointeraction

    Ran 1000 iterations in 1.038 seconds

    Overall Equity
    P0)  2c3c            0.185
    P1)  TsTd            0.815


    Hand distribution for each player
    ==================== 2c3c ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind          3       0.003   1.000   0.000   0.000
    Two pair              226       0.226   0.204   0.009   0.788
    Three-of-a-kind        50       0.050   0.520   0.000   0.480
    Straight               43       0.043   0.837   0.070   0.093
    Flush                  59       0.059   0.831   0.017   0.153
    Straight Flush          1       0.001   1.000   0.000   0.000
    High Card             174       0.174   0.000   0.000   1.000
    One pair              411       0.411   0.000   0.000   1.000
    Full House             33       0.033   0.606   0.091   0.303
    ==================== TsTd ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind          9       0.009   1.000   0.000   0.000
    Two pair              373       0.373   0.791   0.005   0.204
    Three-of-a-kind       141       0.141   0.879   0.000   0.121
    Straight               30       0.030   0.800   0.100   0.100
    Flush                  20       0.020   0.950   0.050   0.000
    Straight Flush          0       0.000   0.000   0.000   0.000
    High Card               0       0.000   0.000   0.000   0.000
    One pair              342       0.342   0.760   0.000   0.240
    Full House             85       0.085   0.929   0.035   0.035

Specify a board:

    python ./main_holdem_odds.py --hands=2c3c,TsTd --board_cards=4c5cTh --nointeraction

    Ran 1000 iterations in 0.989 seconds

    Overall Equity
    P0)  2c3c            0.423
    P1)  TsTd            0.577


    Hand distribution for each player
    ==================== 2c3c ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind          0       0.000   0.000   0.000   0.000
    Two pair               51       0.051   0.000   0.000   1.000
    Three-of-a-kind        14       0.014   0.000   0.000   1.000
    Straight              195       0.195   0.769   0.000   0.231
    Flush                 256       0.256   0.707   0.000   0.293
    Straight Flush         92       0.092   1.000   0.000   0.000
    High Card             137       0.137   0.000   0.000   1.000
    One pair              255       0.255   0.000   0.000   1.000
    Full House              0       0.000   0.000   0.000   0.000
    ==================== TsTd ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind         33       0.033   0.970   0.000   0.030
    Two pair                0       0.000   0.000   0.000   0.000
    Three-of-a-kind       668       0.668   0.394   0.000   0.606
    Straight                0       0.000   0.000   0.000   0.000
    Flush                   0       0.000   0.000   0.000   0.000
    Straight Flush          0       0.000   0.000   0.000   0.000
    High Card               0       0.000   0.000   0.000   0.000
    One pair                0       0.000   0.000   0.000   0.000
    Full House            299       0.299   0.943   0.000   0.057

