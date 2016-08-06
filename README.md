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

    Please input the board cards, separated by spaces.  For example, "Ah As"

    Please input any dead cards, separated by spaces.  For example, "Ah As"

    Please input comma separated hold em hands.  For example, ahad,kskd
    AsAd,QsQc,7h6h

    Ran 1000 iterations in 1.725 seconds

    Overall Equity
    P0)  AsAd            0.618
    P1)  QsQc            0.152
    P2)  7h6h            0.230


    Hand distribution for each player
    ==================== AsAd ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind         10       0.010   1.000   0.000   0.000
    Two pair              408       0.408   0.588   0.000   0.412
    Three-of-a-kind       124       0.124   0.790   0.000   0.210
    Straight               10       0.010   0.200   0.000   0.800
    Flush                  23       0.023   0.739   0.000   0.261
    Straight Flush          0       0.000   0.000   0.000   0.000
    High Card               0       0.000   0.000   0.000   0.000
    One pair              313       0.313   0.466   0.000   0.534
    Full House            112       0.112   0.938   0.000   0.062
    ==================== QsQc ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind         13       0.013   0.923   0.000   0.077
    Two pair              420       0.420   0.000   0.000   1.000
    Three-of-a-kind       107       0.107   0.551   0.000   0.449
    Straight               11       0.011   0.727   0.000   0.273
    Flush                  25       0.025   0.360   0.000   0.640
    Straight Flush          1       0.001   1.000   0.000   0.000
    High Card               0       0.000   0.000   0.000   0.000
    One pair              325       0.325   0.000   0.000   1.000
    Full House             98       0.098   0.643   0.000   0.357
    ==================== 7h6h ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind          4       0.004   0.750   0.000   0.250
    Two pair              206       0.206   0.107   0.000   0.893
    Three-of-a-kind        51       0.051   0.471   0.000   0.529
    Straight              106       0.106   0.934   0.000   0.066
    Flush                  82       0.082   0.720   0.000   0.280
    Straight Flush          3       0.003   1.000   0.000   0.000
    High Card             118       0.118   0.000   0.000   1.000
    One pair              395       0.395   0.000   0.000   1.000
    Full House             35       0.035   0.571   0.000   0.429

    Run a non-interactive version.

    python ./main_holdem_odds.py --hands=2c3c,TsTd --nointeraction

    Ran 1000 iterations in 1.126 seconds

    Overall Equity
    P0)  2c3c            0.196
    P1)  TsTd            0.804


    Hand distribution for each player
    ==================== 2c3c ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind          2       0.002   1.000   0.000   0.000
    Two pair              235       0.235   0.140   0.000   0.860
    Three-of-a-kind        49       0.049   0.469   0.000   0.531
    Straight               55       0.055   0.927   0.055   0.018
    Flush                  79       0.079   0.810   0.038   0.152
    Straight Flush          0       0.000   0.000   0.000   0.000
    High Card             153       0.153   0.000   0.000   1.000
    One pair              401       0.401   0.000   0.000   1.000
    Full House             26       0.026   0.769   0.000   0.231
    ==================== TsTd ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind         15       0.015   1.000   0.000   0.000
    Two pair              405       0.405   0.800   0.000   0.200
    Three-of-a-kind       125       0.125   0.832   0.000   0.168
    Straight               31       0.031   0.806   0.097   0.097
    Flush                  16       0.016   0.750   0.188   0.062
    Straight Flush          0       0.000   0.000   0.000   0.000
    High Card               0       0.000   0.000   0.000   0.000
    One pair              310       0.310   0.726   0.000   0.274
    Full House             98       0.098   0.980   0.000   0.020


    Specify a board:

    python ./main_holdem_odds.py --hands=2c3c,TsTd --board_cards=4c5cTh --nointeraction

    Ran 1000 iterations in 1.044 seconds

    Overall Equity
    P0)  2c3c            0.422
    P1)  TsTd            0.578


    Hand distribution for each player
    ==================== 2c3c ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind          0       0.000   0.000   0.000   0.000
    Two pair               53       0.053   0.000   0.000   1.000
    Three-of-a-kind         8       0.008   0.000   0.000   1.000
    Straight              205       0.205   0.780   0.000   0.220
    Flush                 300       0.300   0.607   0.000   0.393
    Straight Flush         80       0.080   1.000   0.000   0.000
    High Card             113       0.113   0.000   0.000   1.000
    One pair              241       0.241   0.000   0.000   1.000
    Full House              0       0.000   0.000   0.000   0.000
    ==================== TsTd ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind         55       0.055   1.000   0.000   0.000
    Two pair                0       0.000   0.000   0.000   0.000
    Three-of-a-kind       630       0.630   0.368   0.000   0.632
    Straight                0       0.000   0.000   0.000   0.000
    Flush                   0       0.000   0.000   0.000   0.000
    Straight Flush          0       0.000   0.000   0.000   0.000
    High Card               0       0.000   0.000   0.000   0.000
    One pair                0       0.000   0.000   0.000   0.000
    Full House            315       0.315   0.924   0.000   0.076

    
    Use general hands:

    python ./main_holdem_odds.py --hands=88,KQs --nointeraction

    Ran 1000 iterations in 1.116 seconds

    Overall Equity
    P0)  88              0.497
    P1)  KQs             0.502


    Hand distribution for each player
    ==================== 88 ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind          4       0.004   1.000   0.000   0.000
    Two pair              426       0.426   0.444   0.000   0.556
    Three-of-a-kind       111       0.111   0.901   0.000   0.099
    Straight               26       0.026   0.500   0.077   0.423
    Flush                  30       0.030   0.767   0.033   0.200
    Straight Flush          0       0.000   0.000   0.000   0.000
    High Card               0       0.000   0.000   0.000   0.000
    One pair              321       0.321   0.296   0.000   0.704
    Full House             82       0.082   0.878   0.000   0.122
    ==================== KQs ====================
    Hand================    #       Frac       W     Tie       L
    Four-of-a-kind          1       0.001   1.000   0.000   0.000
    Two pair              226       0.226   0.765   0.000   0.235
    Three-of-a-kind        41       0.041   0.659   0.000   0.341
    Straight               70       0.070   0.929   0.029   0.043
    Flush                  59       0.059   0.932   0.017   0.051
    Straight Flush          1       0.001   1.000   0.000   0.000
    High Card             163       0.163   0.000   0.000   1.000
    One pair              410       0.410   0.366   0.000   0.634
    Full House             29       0.029   1.000   0.000   0.000
