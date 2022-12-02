"""
We codify the outcomes as follows:
- 0 for Rock
- 1 for Paper
- 2 for Scissors
Then Draw if equal, Win if index for player 2 is one more than for player 1, Lose otherwise.
"""

def game_result(player_1, player_2):
    if player_1 == player_2: # Draw condition
        return 3
    if (player_1 + 1) % 3 == player_2: # Win condition
        return 6
    return 0

def player_2_move_round_2(player_1, player_2):
    if player_2 == 0: # We need to lose
        return (player_1 - 1) % 3
    if player_2 == 1: # We need to draw
        return player_1
    return (player_1 + 1) % 3
    
player_1_key = {
    "A": 0,
    "B": 1,
    "C": 2,
}

player_2_key = {
    "X": 0,
    "Y": 1,
    "Z": 2,
}

score_played = [1, 2, 3]

score_round_1 = 0
score_round_2 = 0

with open("input.txt") as f:
    for line in f:
        line = line.split()
        # For round one
        player_1, player_2 = player_1_key[line[0]], player_2_key[line[1]]
        score_round_1 += score_played[player_2] + game_result(player_1, player_2)

        # For round two
        player_2 = player_2_move_round_2(player_1, player_2)
        score_round_2 += score_played[player_2] + game_result(player_1, player_2)

print(f"The final score for Round 1 is {score_round_1}")
print(f"The final score for Round 2 is {score_round_2}")
