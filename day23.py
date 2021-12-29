import sys
from re import findall
from itertools import combinations
from heapq import heappush, heappop
from copy import copy

costOfStepPerKind = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

allLocations = (
    "lefthallfar",
    "lefthallnear",
    "room1",
    "column1",
    "room2",
    "column2",
    "room3",
    "column3",
    "room4",
    "righthallnear",
    "righthallfar"
)

allRooms = (
    "room1", "room2", "room3", "room4"
)

# Distances from outside of rooms, and each of possible other places to be
stepsBetweenLocations = {
    ("room1", "lefthallnear"): 1,
    ("room1", "lefthallfar"): 2,
    ("room1", "column1"): 1,
    ("room1", "column2"): 3,
    ("room1", "column3"): 5,
    ("room1", "righthallnear"): 7,
    ("room1", "righthallfar"): 8,

    ("room2", "lefthallnear"): 3,
    ("room2", "lefthallfar"): 4,
    ("room2", "column1"): 1,
    ("room2", "column2"): 1,
    ("room2", "column3"): 3,
    ("room2", "righthallnear"): 5,
    ("room2", "righthallfar"): 6,

    ("room3", "lefthallnear"): 5,
    ("room3", "lefthallfar"): 6,
    ("room3", "column1"): 3,
    ("room3", "column2"): 1,
    ("room3", "column3"): 1,
    ("room3", "righthallnear"): 3,
    ("room3", "righthallfar"): 4,

    ("room4", "lefthallnear"): 7,
    ("room4", "lefthallfar"): 8,
    ("room4", "column1"): 5,
    ("room4", "column2"): 3,
    ("room4", "column3"): 1,
    ("room4", "righthallnear"): 1,
    ("room4", "righthallfar"): 2,

    ("room1", "room2"): 2,
    ("room1", "room3"): 4,
    ("room1", "room4"): 6,
    ("room2", "room3"): 2,
    ("room2", "room4"): 4,
    ("room3", "room4"): 2,
}

def isRoom(location):
    return location in allRooms

def costOfMove(kind, source, destination, extraSteps=0):
    try:
        steps = stepsBetweenLocations[source, destination] + extraSteps
    except KeyError:
        steps = stepsBetweenLocations[destination, source] + extraSteps
    return costOfStepPerKind[kind] * steps

# Returns a new state where a single amphipod moves from the source to a destination, and the cost of the move.
# Rules say that either the source or the destination (or both) must be a room.
def move(state, source, destination):
    next = copy(state)
    amphipod = next[source][0]

    # Extra steps are the steps through a room, to fully leave or enter it.
    extraSteps = 0
    if isRoom(source):
        extraSteps += ROOM_SIZE - len(next[source]) + 1
    if isRoom(destination):
        extraSteps += ROOM_SIZE - len(next[destination])

    next[source] = next[source][1:] if len(next[source]) > 1 else ""
    next[destination] = amphipod + next[destination]
    return stateToString(next), costOfMove(amphipod, source, destination, extraSteps)

def canMove(state, source, destination):
    if not state[source]:
        return False
    if (not isRoom(destination) and state[destination]) or (isRoom(destination) and len(state[destination]) == ROOM_SIZE):
        return False

    # If moving into a room...
    if isRoom(destination):
        amphipod = state[source][0]
        # ...it needs to be the correct destination for the amphipod
        if " ABCD".index(amphipod) != int(destination[-1]):
            return False
        # ...and all amphipods inside - if any - are of the same kind
        if state[destination] and state[destination].replace(amphipod, ""):
            return False
    
    # Ensure the path is not blocked
    isource = allLocations.index(source)
    idestination = allLocations.index(destination)
    left = min(isource, idestination)
    right = max(isource, idestination)
    if any([ state[nonroom] for nonroom in allLocations[left+1:right] if not isRoom(nonroom) ]):
        return False
    return True

# Amphipods are either leaving a room, entering a room, or doing both with a single move.
def possibleNextStates(state):
    state = stringToState(state)
    # Leaving a room to any free non-room location, of vice versa
    for room in allRooms:
        for nonroom in [ location for location in allLocations if not isRoom(location) ]:
            if canMove(state, room, nonroom): yield move(state, room, nonroom)
            if canMove(state, nonroom, room): yield move(state, nonroom, room)

    # Room to room moves
    for a, b in combinations(allRooms, 2):
        if canMove(state, a, b): yield move(state, a, b)
        if canMove(state, b, a): yield move(state, b, a)

def locationString(state, location):
    if not isRoom(location):
        return state[location] or "_"
    empty = ROOM_SIZE - len(state[location])
    return ((empty * "_") or "") + (state[location] or "")

def stateToString(state):
    return ' '.join([ locationString(state, location) for location in allLocations ])

def stringToState(stateString):
    fields = stateString.split()
    return { location: fields[i].replace("_", "") for i, location in enumerate(allLocations) }

def printTraceBack(goal, cost, previousStates):
    print("----- Traceback -----")
    traceback = [ (goal, None) ]
    node, cost = previousStates[goal]
    while True:
        traceback.insert(0, (node, cost))
        node, cost = previousStates[node]
        if node is None:
            break
    
    for i, (step, cost) in enumerate(traceback):
        print(step)
        if cost is not None:
            print(f" move costing {cost}")

# Maybe later...
# def heuristic(next, goal):
#    pass

def solve(start, goal):
    frontier = [ (0, start) ]
    cameFrom = { start: (None, 0) }
    costSoFar = { start: 0 }

    while frontier:
        cost, current = heappop(frontier)
        if current == goal:
            printTraceBack(goal, cost, cameFrom)
            return cost

        for next, costOfMove in possibleNextStates(current):
            newCost = costSoFar[current] + costOfMove
            if next not in costSoFar or newCost < costSoFar[next]:
                costSoFar[next] = newCost
                priority = newCost # + heuristic(next, goal)
                heappush(frontier, (priority, next))
                cameFrom[next] = current, costOfMove

def main(args = ()):
    fileName = "day23.txt" if len(args) < 1 else args[0]

    initial = ["", "", "", ""]
    with open(fileName) as lines:
        for line in lines:
            amphiphods = findall(r"[ABCD]", line)
            if amphiphods:
                for i, amphipod in enumerate(amphiphods):
                    initial[i] += amphipod

    state = {}
    goal = {}

    for nonroom in [ location for location in allLocations if not isRoom(location) ]:
        state[nonroom] = goal[nonroom] = ""

    # Ugly, but part 2 surprised me with changing input data
    global ROOM_SIZE
    ROOM_SIZE = 2
    for i, room in enumerate(allRooms):
        state[room] = initial[i]
        goal[room] = ROOM_SIZE * "ABCD"[i]
    print("Part 1:", solve(stateToString(state), stateToString(goal)))

    ROOM_SIZE = 4
    extras = ( "DD", "CB", "BA", "AC" )
    for i, room in enumerate(allRooms):
        state[room] = state[room][0] + extras[i] + state[room][1]
        goal[room] = ROOM_SIZE * "ABCD"[i]
    print("Part 2:", solve(stateToString(state), stateToString(goal)))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))