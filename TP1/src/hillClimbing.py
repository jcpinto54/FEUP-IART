import time
import blueprint as bp
from utils import *


def hillClimbing(blueprint, solution):
    """
    Regular Hill climbing algorithm implementation.
    """

    maxRouters = getIndexOfLastNonEmptyRouter(solution) + 1
    solutionValue = value(blueprint, solution)
    print("\nStarting solution value:", solutionValue)
    iteration = 0
    upgrade = True
    # Run until 30 upgrades were made, or until a full iteration with no upgrades
    while iteration < 30 and upgrade:
        upgrade = False

        """
        Initially, we tried to use this remove routers from the solutions because we realized, the hill climbing 
        algorithms were not selecting any solutions with less than the max number of routers. 
        Thus, we removed these 2 lines that were slowing down our code. 
        
        for numRouters in range(maxRouters, maxRouters//2, -1):
            for i in range(numRouters):
        """
        for i in range(maxRouters):
            for j in range(0, 2):
                for k in range(0, 2):
                    # Compute a neighbour and its value
                    neighbourSolution, neighbourValue = neighbour(blueprint, solution, i, j, k, maxRouters)

                    # Check if neighbour is valid
                    if neighbourSolution is None and neighbourValue is None:
                        continue

                    # Check if neighbour is the same as the current solution
                    if compareLists(solution, neighbourSolution):
                        continue

                    # If the neighbour is better than the current solution
                    if neighbourValue > solutionValue:
                        solutionValue = neighbourValue
                        solution = neighbourSolution.copy()
                        iteration += 1
                        upgrade = True
                        print("Upgrade!", str(i) + "/" + str(50) + ", Current score:", solutionValue)

                        # Start over
                        break

                # Start over
                if upgrade:
                    break
            # Start over
            if upgrade:
                break
    print("Final solution value:", solutionValue)
    return solution


def hillClimbingSteepestAscent(blueprint, solution):
    """
    Hill climbing steepest ascent implementation.

    In this algorithm, we avoided using the 'value' function, because of its heavy computational load.
    As an alternative, we used the number of covered cells and the number of routers in a solution. We believe
    this method is a good predicition to a solution's value. This prediction works well for maps with an unsignificant
    backbone cost.
    """

    print("\nStarting solution value:", value(blueprint, solution))

    # Initial solution value prediciton
    solutionCoveredCells = len(blueprint.getSolutionCoveredCells(solution))
    solutionRouters = routersPlaced(solution)

    upgrade = True
    # Since the exact value of a solution cannot be computed, we stored the 3 best solutions, to guard ourselves
    # from the situation of generating a solution which exceeds the budget.
    steepest1 = (solution, solutionCoveredCells, solutionRouters)
    steepest2 = (solution, solutionCoveredCells, solutionRouters)
    steepest3 = (solution, solutionCoveredCells, solutionRouters)
    maxRouters = getIndexOfLastNonEmptyRouter(solution) + 1

    # Contains budget exceeding solutions
    impossibleSolutions = {}

    # Run until no upgrade is made
    while upgrade:
        upgrade = False

        """
        Initially, we tried to use this remove routers from the solutions because we realized, the hill climbing 
        algorithms were not selecting any solutions with less than the max number of routers. 
        Thus, we removed these 2 lines that were slowing down our code. 

        for numRouters in range(maxRouters, maxRouters//2, -1):
            for i in range(numRouters):
        """
        for i in range(maxRouters):
            for j in range(0, 2):
                for k in range(0, 2):
                    # Compute a neighbour solution and its value
                    neighbourSolution = neighbour(blueprint, solution, i, j, k, maxRouters, False)

                    # Check if neighbour is valid
                    if neighbourSolution == (None, None):
                        continue

                    skip = True
                    # Check if a solution has been marked as impossible (exceeds the budget)
                    try:
                        impossibleSolutions[tuple(neighbourSolution)]
                    except KeyError:
                        skip = False
                    if skip:
                        continue

                    # Check if neighbour and current solution are the same
                    if compareLists(solution, neighbourSolution):
                        continue

                    # Neighbour value prediction
                    neighbourCoveredCells = len(blueprint.getSolutionCoveredCells(neighbourSolution))
                    neighbourSolutionRouters = routersPlaced(neighbourSolution)

                    # A covered cell is 10x more valuable then a router.
                    # Checks if neighbour is better than the current best solution
                    if neighbourCoveredCells * 10 + blueprint.getMaxRouters() - neighbourSolutionRouters > steepest1[1] * 10 + blueprint.getMaxRouters() - steepest1[2]:
                        # Push back solutions
                        steepest3 = steepest2
                        steepest2 = steepest1
                        steepest1 = (neighbourSolution, neighbourCoveredCells, neighbourSolutionRouters)
                        upgrade = True
        # If there was no upgrade
        if not upgrade:
            break

        steepestValue = value(blueprint, steepest1[0])
        # Check if 'steepest1' does not exceed the budget
        if steepestValue is not None:
            print("Upgrade! Current score:", steepestValue)
            solution, solutionCoveredCells, solutionRouters = steepest1
            steepest2 = steepest1
            steepest3 = steepest1
            continue
        # 'steepest1' exceeded the budget. Mark it as impossible
        impossibleSolutions[tuple(steepest1[0])] = True
        steepestValue = value(blueprint, steepest2[0])
        # Check if 'steepest2' does not exceed the budget
        if steepestValue is not None:
            print("Upgrade! Current score:", steepestValue)
            solution, solutionCoveredCells, solutionRouters = steepest2
            steepest1 = steepest2
            steepest3 = steepest2
            continue
        # 'steepest2' exceeded the budget. Mark it as impossible
        impossibleSolutions[tuple(steepest2[0])] = True
        steepestValue = value(blueprint, steepest3[0])
        # Check if 'steepest3' does not exceed the budget
        if steepestValue is not None:
            print("Upgrade! Current score:", steepestValue)
            solution, solutionCoveredCells, solutionRouters = steepest3
            steepest2 = steepest3
            steepest1 = steepest3
            continue
        # 'steepest3' exceeded the budget. Mark it as impossible
        impossibleSolutions[tuple(steepest3)] = True
        # If all 3 solutions exceed the budget, compute new ones

    print("Final solution value:", value(blueprint, solution))
    return solution

