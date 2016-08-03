# Texas Hold 'em Equity and Hand Distribution

### Basic invocations

Run an interactive version of the script:
    python ./main_holdem_odds.py

    Please input comma separated hold em hands.  For example, ahad,kskd
    AsAd,QsQc,7h6h
    Please input the board cards, separated by spaces.  For example, "Ah As"

    Please input any dead cards, separated by spaces.  For example, "Ah As"

    Ran 1000 iterations in 1.417 seconds
    P0)  As Ad           0.535
    P1)  Qs Qc           0.200
    P2)  7h 6h           0.267
    ==================== P0 AsAd ====================
    Four-of-a-kind           6      0.006
    Two pair               415      0.415
    Three-of-a-kind        110      0.110
    Straight                16      0.016
    Flush                   18      0.018
    Straight Flush           0      0.000
    High Card                0      0.000
    One pair               349      0.349
    Full House              86      0.086
    ==================== P1 QsQc ====================
    Four-of-a-kind          10      0.010
    Two pair               405      0.405
    Three-of-a-kind        116      0.116
    Straight                17      0.017
    Flush                   20      0.020
    Straight Flush           0      0.000
    High Card                0      0.000
    One pair               342      0.342
    Full House              90      0.090
    ==================== P2 7h6h ====================
    Four-of-a-kind           2      0.002
    Two pair               237      0.237
    Three-of-a-kind         48      0.048
    Straight               107      0.107
    Flush                   90      0.090
    Straight Flush           2      0.002
    High Card              106      0.106
    One pair               374      0.374
    Full House              34      0.034

Run a non-interactive version.

    python ./main_holdem_odds.py --hands=2c3c,TsTd --nointeraction

    Ran 1000 iterations in 1.002 seconds
    P0)  2c 3c           0.213
    P1)  Ts Td           0.793
    ==================== P0 2c3c ====================
    Four-of-a-kind           3      0.003
    Two pair               235      0.235
    Three-of-a-kind         43      0.043
    Straight                51      0.051
    Flush                   76      0.076
    Straight Flush           0      0.000
    High Card              146      0.146
    One pair               413      0.413
    Full House              33      0.033
    ==================== P1 TsTd ====================
    Four-of-a-kind          11      0.011
    Two pair               414      0.414
    Three-of-a-kind        106      0.106
    Straight                23      0.023
    Flush                   21      0.021
    Straight Flush           3      0.003
    High Card                0      0.000
    One pair               328      0.328
    Full House              94      0.094

Specify a board:
    python ./main_holdem_odds.py --hands=2c3c,TsTd --board_cards=4c5cTh --nointeraction

    Ran 1000 iterations in 0.966 seconds
    P0)  2c 3c           0.421
    P1)  Ts Td           0.579
    ==================== P0 2c3c ====================
    Four-of-a-kind           0      0.000
    Two pair                46      0.046
    Three-of-a-kind         15      0.015
    Straight               221      0.221
    Flush                  273      0.273
    Straight Flush          77      0.077
    High Card              118      0.118
    One pair               250      0.250
    Full House               0      0.000
    ==================== P1 TsTd ====================
    Four-of-a-kind          39      0.039
    Two pair                 0      0.000
    Three-of-a-kind        654      0.654
    Straight                 0      0.000
    Flush                    0      0.000
    Straight Flush           0      0.000
    High Card                0      0.000
    One pair                 0      0.000
    Full House             307      0.307

