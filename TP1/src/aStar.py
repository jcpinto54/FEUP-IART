from utils import *
import heapq
import math


class Node:
    """
    Auxiliary structure to help to the A* algorithm
    """
    def __init__(self, pos, parent, h=0, cost=0):
        self.position = pos
        self.parent = parent
        self.cost = cost
        self.heurisitic = h

    def __eq__(self, other):
        return self.position == other.position

    # Sort nodes
    def __lt__(self, other):
        # The processed cost is reduced, in order to increase the A* algorithm's efficiency.
        # Since this algorithm is running in a grid, the optimal solution is guaranteed.
        processedCost = 0.8
        return (processedCost * self.cost + self.heurisitic) < (processedCost * other.cost + other.heurisitic)

    def __repr__(self):
        return '({0},{1})'.format(self.position, self.cost + self.heurisitic)


def aStar(blueprint, startCoord, endCoord):
    """ Calculates the shortest paths between 2 points.
        Params: startCoord - tuple
            endCoord - tuple
            blueprint - class Blueprint
    """
    startCoord = tuple(startCoord)
    # Check if start and end positions are valid
    if (not blueprint.atGrid(startCoord)) or (not blueprint.atGrid(endCoord)):
        return None

    startNode = Node(startCoord, None, distance(startCoord, endCoord))
    endNode = Node(endCoord, None, 0)

    # 'open' is a priority queue with nodes to be expanded and is ordered by each node's cost
    open = [startNode]
    heapq.heapify(open)

    # 'closed' is a list which contains the already visited nodes
    closed = []

    # while open has at least one node
    while open:
        currentNode = heapq.heappop(open)

        # Mark node as visited
        closed.append(currentNode)

        # If finished
        if currentNode == endNode:
            path = []
            # Create path
            while currentNode != startNode:
                path.append(currentNode.position)
                currentNode = currentNode.parent
            path.append(currentNode.position)
            return path[::-1]

        # Get each neighbour cell
        neighbours = blueprint.getCellNeighbours(currentNode.position)
        for n in neighbours:
            # Check move cost
            if isDiagonal(n, currentNode.position):
                moveCost = math.sqrt(2)
            else:
                moveCost = 1

            neighbourNode = Node(n, currentNode, distance(n, endCoord), currentNode.cost + moveCost)

            # Node already visited
            if neighbourNode in closed: continue

            addToOpen = True
            # Check if the neighbour already exists and, if it exists, check whether it's worth an update
            for node in open:
                if neighbourNode == node and neighbourNode.cost + neighbourNode.heurisitic >= node.cost + node.heurisitic:
                    addToOpen = False

            if addToOpen:
                heapq.heappush(open, neighbourNode)
    return None


def isDiagonal(pos1, pos2):
    """
    Checks if 2 positions are in the same diagonal.
    """
    return abs(pos1[1] - pos2[1]) != 0 and abs(pos1[0] - pos2[0]) != 0
