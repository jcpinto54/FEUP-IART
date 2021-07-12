import utils
from hillClimbing import *
import aStar


class Node:
    """
    Auxiliary structure to aid in the Kruskal algorithm. A list of nodes and edges composes a graph.
    """
    def __init__(self, coord, kruskalParent = None, kruskalRank = 0):
        self.coord = coord
        self.kruskalParent = kruskalParent
        self.kruskalRank = kruskalRank

    def __eq__(self, o) -> bool:
        if o is None: return False
        return self.coord == o.coord

    def retrieveRoot(self):
        """
        :return: The node's graph root
        """
        if self.kruskalParent is None:
            return self
        current = self.kruskalParent
        previous = self
        while current is not None:
            previous = current
            current = current.kruskalParent
        return previous


class Edge:
    """
    Auxiliary structure to aid in the Kruskal algorithm. A list of nodes and edges composes a graph.
    """
    def __init__(self, nodeFrom : Node, nodeTo : Node, cost):
        self.nodeFrom = nodeFrom
        self.nodeTo = nodeTo
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost


class Graph:
    """
    Auxiliary structure to aid in the Kruskal algorithm. A list of nodes and edges composes a graph.
    """
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.cost = 0

    def kruskal(self):
        """
        Implementation of the Kruskal algorithm.
        :return: The minimum spanning tree of a graph
        """

        # Sort edges by cost
        sortedEdges = sorted(self.edges)
        # Edges to add to the minimum spanning tree
        selectedEdges = []
        i = 0
        # Run until the minimum spanning tree is complete
        while len(selectedEdges) < len(self.nodes) - 1:
            # Choose the cheapest edge
            bestEdge = sortedEdges[i]
            i = i + 1
            # Find both ends' nodes root
            fromRoot = bestEdge.nodeFrom.retrieveRoot()
            toRoot = bestEdge.nodeTo.retrieveRoot()

            # If roots are not the same, then the nodes belong to different graphs
            if fromRoot != toRoot:
                # This edge is a bridge between 2 graphs, so let's add it the 'selectedEdges' list
                selectedEdges.append(bestEdge)
                # Decide who becomes the root of the joined graph
                chooseRoot(bestEdge.nodeFrom, bestEdge.nodeTo)

        # Return MST as a graph
        return Graph(self.nodes, selectedEdges)

    def getPaths(self, blueprint):
        """
        For each edge, this function calculates the path between two nodes, using the A* algorithm.
        :return: List of cells which are part of the paths
        """
        backboneCells = []
        for edge in self.edges:
            path = aStar.aStar(blueprint, edge.nodeFrom.coord, edge.nodeTo.coord)
            backboneCells.extend(path)
        return backboneCells


def chooseRoot(node1: Node, node2: Node):
    """
    Decide who becomes the root of a joined graph. Supports the Kruskal algorithm.
    """
    node1 = node1.retrieveRoot()
    node2 = node2.retrieveRoot()
    if node1.kruskalRank < node2.kruskalRank:
        node1.kruskalParent = node2
    elif node1.kruskalRank > node2.kruskalRank:
        node2.kruskalParent = node1
    else:
        node2.kruskalParent = node1
        node1.kruskalRank += 1


def buildGraphWithSolution(solution, backboneCoord):
    """
    Transforms a solution in a graph. This function is used to make the preparations for the Kruskal algorithm.
    :param solution: List of router coordinates
    :param backboneCoord: Backbone coordinate
    :return: A complete graph
    """
    # Nodes is a dictionary to help efficiency
    nodes = {}
    edges = []
    aux = solution.copy()

    # Treat the backbone position the same way as a router
    aux.append(backboneCoord)
    for coord in aux:
        if coord == (-1, -1):
            continue
        nodes[coord] = Node(coord)

    # Make the graph complete. This means every pair of nodes are connected
    for i in range(len(aux)):
        for j in range(len(aux)):
            if i >= j or (aux[i] == (-1, -1) or aux[j] == (-1, -1)):
                continue
            edges.append(Edge(nodes[aux[i]], nodes[aux[j]], utils.distance(aux[i], aux[j])))

    return Graph(list(nodes.values()), edges)

