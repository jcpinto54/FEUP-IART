import random
import time
import blueprint as bp
from utils import *


def crossover(sol1, sol2):
    """
    Makes a Single-Point Crossover with 2 possible solutions to routers positions.
    :return: A child of the 2 solutions given (using crossover).
    """
    r1, r2 = routersPlaced(sol1), routersPlaced(sol2)
    minRouters = min(r1, r2)
    rand = random.randint(1, max(1, minRouters - 1))

    child = []

    for i in range(len(sol1)):
        if i < rand:
            child.append(sol1[i])
        else:
            child.append(sol2[i])

    return child


def mutation(blueprint, sol):
    """
    Chooses a number of routers to mutate and replace them with random neighbours.
    """
    r = routersPlaced(sol)

    routersToMutate = max(1, blueprint.getMaxRouters() // 10)
    for i in range(routersToMutate):
        if r == 0:
            break
        sol = randomNeighbour(blueprint, sol, True)[0]
        r -= 1

    return sol


def generateInitialPopulation(blueprint):
    """
    Generates the first generation of solutions randomly.
    :return: list with population of first generation.
    """
    population = []
    positionsAdded = {}
    iteration = 0
    lastIteration = 10

    while iteration < lastIteration:
        print("Generating initial population: " + str(iteration) + "/" + str(lastIteration))
        individualSol = []

        # Generating each solution
        for j in range(blueprint.getMaxRouters()):
            rand = random.randint(0, len(blueprint.validPositions) - 1)
            while True:
                try:
                    positionsAdded[rand]
                except KeyError:
                    break
                rand = random.randint(0, len(blueprint.validPositions) - 1)
                continue

            individualSol.append(blueprint.validPositions[rand])
            positionsAdded[rand] = True

            # Check if last router added covered any cell (if it doesn't, it's not needed)
            while len(blueprint.accessCoverageDict(individualSol[-1])) == 0:
                individualSol.pop()
                rand = random.randint(0, len(blueprint.validPositions) - 1)
                while True:
                    try:
                        positionsAdded[rand]
                    except KeyError:
                        break
                    rand = random.randint(0, len(blueprint.validPositions) - 1)
                    continue

                individualSol.append(blueprint.validPositions[rand])

            # Check if the actual routers cover all target covered cells
            # If so, fill the remaining solution list with (-1, -1)
            if blueprint.targetCoveredCells == len(blueprint.getSolutionCoveredCells(individualSol)):
                while len(individualSol) < blueprint.getMaxRouters():
                    individualSol.append((-1, -1))
                break

            # Check if the solution value exceeds the budget.
            # If so, it means we can't have the last router added and we can fill the solution list with (-1, -1)
            if value(blueprint, individualSol) is None:
                individualSol.pop()
                while len(individualSol) < blueprint.getMaxRouters():
                    individualSol.append((-1, -1))
                break

        iteration += 1
        population.append(individualSol)

    population.sort(reverse=True, key=lambda elem: value(blueprint, elem))

    print("Generating initial population: Done!")
    return population


def geneticAlgorithm(blueprint):
    """
    Genetic Algorithm: For 20 "generations", all population reproduces randomly, between the best half of solutions.
    :return: The best solution of the last generation.
    """
    population = generateInitialPopulation(blueprint)
    iteration = 0
    lastIteration = 20

    while iteration < lastIteration:
        print("Generation... " + str(iteration) + "/" + str(lastIteration))

        nextGeneration = []

        for i in range(int(len(population))):
            # for each generation, it generates the at most the number of children as the actual population
            x = population[random.randint(0, int(len(population) / 2))]  # randomizing in the best half of population
            y = population[random.randint(0, int(len(population) / 2))]  # randomizing in the best half of population
            child = crossover(x, y)

            if random.randint(0, 100) < 10:  # 10% chance of a child to be mutated
                child = mutation(blueprint, child)

            if value(blueprint, child) is not None:
                nextGeneration.append(child)

        population = nextGeneration
        population.sort(reverse=True, key=lambda elem: value(blueprint, elem))
        iteration += 1

    print("Generation... Done!")
    print("Solution value: " + str(value(blueprint, population[0])))

    # The population is ordered by value, so the first solution is the best one
    return population[0]
