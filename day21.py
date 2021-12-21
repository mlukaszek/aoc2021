import sys
from functools import lru_cache

PLAYER_COUNT = 2

def roll_deterministic(turn):
    low = 3 * turn + 1
    mid =  low + 1
    high = mid + 1
    return low + mid + high

def part1(positions):
    scores = [0] * PLAYER_COUNT
    turn = -1
    winner = None

    while winner is None:
        for player in range(PLAYER_COUNT):
            turn += 1
            rolls = roll_deterministic(turn)
            positions[player] = (positions[player] + rolls) % 10
            scores[player] += (positions[player] + 1)
            # print(f"Player {player+1} rolls {rolls} and moves to position {positions[player] + 1} for a total score {scores[player]}")
            if scores[player] >= 1000:
                winner = player
                break

    print(f"After {turn+1} turns = {3*(turn+1)} rolls")
    for player in range(PLAYER_COUNT):
        print(f"Player {player+1} is on position {positions[player] + 1} with score {scores[player]}")

    return scores[winner+1 % 2] * 3 * (turn+1)

# Map of equal sums of 3 rolls - sums and number of cases where they can be the same
dirac_rolls = {
    3: len(set([ 111 ])),
    4: len(set([ 112, 121, 211 ])),
    5: len(set([ 113, 131, 311, 122, 212, 221 ])),
    6: len(set([ 123, 132, 312, 321, 213, 231, 222 ])),
    7: len(set([ 223, 232, 322, 133, 313, 331 ])),
    8: len(set([ 233, 323, 332 ])),
    9: len(set([ 333 ]))
}

@lru_cache(maxsize=None)
def roll_dirac(playerPosition, opponentPosition, playerScore, opponentScore):
    if playerScore >= 21:
        return 1, 0

    if opponentScore >= 21:
        return 0, 1

    scores = [ 0, 0 ]

    for rolls, count in dirac_rolls.items():
        newPlayerPosition = (playerPosition + rolls) % 10
        newPlayerScore = playerScore + newPlayerPosition + 1
        
        wins_now = [ count * win for win in reversed(roll_dirac(opponentPosition, newPlayerPosition, opponentScore, newPlayerScore)) ]
        
        for player in range(2):
            scores[player] += wins_now[player]
    return scores

def part2(positions):
    scores = [0] * PLAYER_COUNT
    results = roll_dirac(*positions, *scores)
    return max(results)

def main(args = ()):
    fileName = "day21.txt" if len(args) < 1 else args[0]

    positions = []
    with open(fileName) as lines:
        for line in lines:
            positions.append(int(line.split(":")[-1]) - 1)

    print("Part 1:", part1(positions[:]))
    print("Part 2:", part2(positions))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))