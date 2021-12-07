import sys
from collections import deque

SIZE = 5

def is_winning(board):
    for offset in range(0, SIZE):
        row = board[offset*SIZE:(offset+1)*SIZE]
        if all([ n < 0 for n in row ]):
            return row
        col = board[offset::SIZE]
        if all([ n < 0 for n in col ]):
            return col

def bingo(numbers, boards, winFirst):
    won = []
    for number in numbers:
        for boardNum, board in enumerate(boards):
            if number in board:
                board[board.index(number)] -= 100; # Cheeky way of indicating the number was drawn

            if is_winning(board):
                if boardNum not in won:
                    won.append(boardNum)
                    if winFirst or len(won) == len(boards):
                        score = sum([ number for number in board if number > 0 ])
                        return number * score

def main(args = ()):
    arg = "day4.txt" if len(args) < 1 else args[0]

    with open(arg, "r") as puzzle:
        numbers = [ int(number) for number in puzzle.readline().strip().split(",") ]
        boards = []
        for line in puzzle:
            if not line.strip():
                boards.append([])
                continue
            for number in line.split():
                boards[-1].append(int(number))
    if len(boards[-1]) == 0:
        boards.pop()

    print("Part 1 Final score:", bingo(numbers, boards, True))
    print("Part 2 Final score:", bingo(numbers, boards, False))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))