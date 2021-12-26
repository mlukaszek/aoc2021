import sys
from dataclasses import dataclass

@dataclass
class Cucumber:
    x: int
    y: int
    horizontal: bool

def cucumberLocations(cucumbers):
    return { (c.x, c.y): c.horizontal for c in cucumbers }

def moveCucumbers(cucumbers, horizontal, xmax, ymax):
    moves = 0
    locationsBeforeMove = cucumberLocations(cucumbers)
    for cucumber in cucumbers:
        if (horizontal ^ cucumber.horizontal):
            continue
        dx, dy = (1,0) if horizontal else (0,1)
        x, y = cucumber.x, cucumber.y
        next = ((x+dx) % (xmax+1), (y+dy) % (ymax+1))
        if next not in locationsBeforeMove:
            moves += 1
            cucumber.x, cucumber.y = next
    return moves
    
def moving(cucumbers, xmax, ymax):
    return moveCucumbers(cucumbers, True, xmax, ymax) + moveCucumbers(cucumbers, False, xmax, ymax)

def main(args = ()):
    fileName = "day25.txt" if len(args) < 1 else args[0]

    cucumbers = []
    xmax, ymax = 0, 0
    with open(fileName) as lines:
        for y, line in enumerate(lines):
            for x, cucumber in enumerate(line.strip()):
                if cucumber == ".": continue
                cucumbers.append(Cucumber(x, y, cucumber == ">"))
                xmax = max(xmax, x)
                ymax = max(ymax, y)

    steps = 1
    while moving(cucumbers, xmax, ymax):
        steps += 1

    print(f"Stopping after {steps} steps")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))