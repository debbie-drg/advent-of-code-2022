"""
We codify the outcomes as follows:
- 0 for Rock
- 1 for Paper
- 2 for Scissors
Then Draw if equal, Win if index for player 2 is one more than for player 1, Lose otherwise.
Using this we can easily compute the game result.
"""


def game_result(player_1: int, player_2: int) -> int:  # 0 if lost, 1 if draw, 2 if won
    return (1 + player_2 - player_1) % 3


def player_2_move_round_2(player_1: int, player_2: int) -> int:
    return (player_1 + player_2 - 1) % 3


player_1_key = {"A": 0, "B": 1, "C": 2}
player_2_key = {"X": 0, "Y": 1, "Z": 2}

# We compute the score tables for both players
results_round_1, results_round_2 = dict(), dict()
for player_1 in player_1_key:
    player_1_value = player_1_key[player_1]
    for player_2 in player_2_key:
        player_2_value = player_2_key[player_2]
        results_round_1[f"{player_1} {player_2}"] = (
            player_2_value + 1
        ) + 3 * game_result(player_1_value, player_2_value)
        player_2_value = player_2_move_round_2(player_1_value, player_2_value)
        results_round_2[f"{player_1} {player_2}"] = (
            player_2_value + 1
        ) + 3 * game_result(player_1_value, player_2_value)


def func_from_dict(dictionary: dict, input: str):
    return dictionary[input]


with open("input.txt") as f:
    input_games = f.read().split(sep="\n")
    input_games.remove("")
    score_round_1 = sum(map(lambda x : func_from_dict(results_round_1, x), input_games))
    score_round_2 = sum(map(lambda x : func_from_dict(results_round_2, x), input_games))


print(f"The final score for Round 1 is {score_round_1}")
print(f"The final score for Round 2 is {score_round_2}")
