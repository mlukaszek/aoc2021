import sys
from collections import defaultdict

def day(fish):
    expired = fish[0]
    for i in range(8):
        fish[i] = fish[i+1]
    fish[6] += expired
    fish[8] = expired

def main(args = ()):
    arg = "day6.txt" if len(args) < 1 else args[0]
    fish = defaultdict(int)
    with open(arg, "r") as initial:
        for counter in [ int(num) for num in initial.readline().strip().split(",") ]:
            fish[counter] += 1
    
    for days in (80, 256):
        for i in range(days):
            day(fish)
        print(f"{i+1}:", sum(fish.values()))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))