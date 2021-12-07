import sys

def part1(scan):
    position, depth = 0, 0
    for command in scan:
        direction, amount = command.strip().split()
        number = int(amount)
        if direction == "forward":
            position += number
        elif direction == "down":
            depth -= number
        elif direction == "up":
            depth += number
    return (position, depth)

def part2(scan):
    position, depth, aim = 0, 0, 0
    for command in scan:
        direction, amount = command.strip().split()
        number = int(amount)
        if direction == "forward":
            position += number
            depth += aim * number
        elif direction == "down":
            aim -= number
        elif direction == "up":
            aim += number
    return (position, depth)

def main(args = ()):
    arg = "day2.txt" if len(args) < 1 else args[0]
    with open(arg, "r") as scan:
        x,  y = part1(scan)
        print("Part 1:", abs(x*y))
        scan.seek(0)
        x,  y = part2(scan)
        print("Part 2:", abs(x*y))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))