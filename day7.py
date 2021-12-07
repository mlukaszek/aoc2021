import sys

def min_costs(crabs, constantRate):
    costs = []
    for target in range(max(crabs) + 1):
        costs.append(0)
        for crab in crabs:
            distance =  abs(crab - target)
            costs[-1] += distance if constantRate else int(distance * (1 + distance) / 2)
    return min(costs)

def main(args = ()):
    fileName = "day7.txt" if len(args) < 1 else args[0]

    crabs = []
    with open(fileName) as lines:
        crabs = [ int(i) for i in lines.readline().strip().split(",") ]

    print("Part 1:", min_costs(crabs, True))
    print("Part 2:", min_costs(crabs, False))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))