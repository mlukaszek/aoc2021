import sys
from collections import defaultdict
from heapq import heappush, heappop

def in_bounds(location, bounds):
    i, j = location
    return i >= 0 and j >= 0 and i <= bounds[0] and j <= bounds[1]

def adjacent(location, bounds):
    i, j = location
    return (
        (i+di, j+dj) for (di,dj) in ((1,0),(-1,0),(0,1),(0,-1))
        if in_bounds((i+di, j+dj), bounds)
    )

# Heuristic for A* - using Manhattan distance
def heuristic(node, goal):
    return sum(abs(goal[i] - node[i]) for i in (0,1))

def a_star(graph, start, goal):
    frontier = [ (0, start) ]
    cameFrom = { start: None }
    costSoFar = { start: 0 }

    while frontier:
        cost, current = heappop(frontier)
        if current == goal:
            return cost

        for next in adjacent(current, goal):
            newCost = costSoFar[current] + graph.getCost(next)
            if next not in costSoFar or newCost < costSoFar[next]:
                costSoFar[next] = newCost
                priority = newCost + heuristic(next, goal)
                heappush(frontier, (priority, next))
                cameFrom[next] = current

class Graph(object):
    def __init__(self) -> None:
        self.risks = defaultdict(int)

    def setSize(self, i, j):
        self.size = (i, j)

    def setCost(self, i, j, value):
        self.risks[(i,j)] = value

    def getCost(self, node):
        if node in self.risks:
            return self.risks[node]

        # Cost for part 2:
        # Get the value from the original tile
        i, j = node
        risk = self.risks[(i % self.size[0], j % self.size[1])]

        # Add Manhattan distance between the tiles
        distance = i // self.size[0] + j // self.size[1]
        return 1 + ((risk + distance - 1) % 9)

def main(args = ()):
    fileName = "day15.txt" if len(args) < 1 else args[0]

    graph = Graph()
    with open(fileName) as lines:
        for j, row in enumerate(lines):
            for i, value in enumerate(row.strip()):
                graph.setCost(i, j, int(value))
    graph.setSize(i+1, j+1)

    start = (0, 0)
    part1 = (i, j)
    part2 = (5 * (i+1) - 1, 5 * (j+1) - 1)
    for part, goal in enumerate((part1, part2)):
        cost = a_star(graph, start, goal)
        print(f"Part {part+1}:", cost)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))