import sys
from collections import deque

def count_larger(scan):
    previous = None
    larger = 0
    for line in scan:
        current = int(line)
        if previous and current > previous:
            larger += 1
        previous = current
    return larger

def count_windowed(scan):
    sums = []
    window = deque()
    for line in scan:
        window.append(int(line))
        if len(window) > 3:
            window.popleft()
        if len(window) == 3:
            sums.append(sum(window))
    return count_larger(sums)

def main(args = ()):
    arg = "day1.txt" if len(args) < 1 else args[0]
    with open(arg, "r") as scan:
        print("Part 1:", count_larger(scan))
        scan.seek(0)
        print("Part 2:", count_windowed(scan))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))