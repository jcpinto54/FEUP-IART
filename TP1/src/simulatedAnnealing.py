import blueprint as bp
from utils import *
import math
import time


def simulatedAnnealing(blueprint, solution):
    """
    Simulated annealing algorithm implementation.
    Configuration:  - initial temperature of 10000
                    - end temperature of 10
                    - linear cooling schedule with a factor of 0.99
                    - 10 iterations per temperature
    """
    # Configuration
    initialTemp = 10000
    finalTemp = 10
    alpha = 0.99
    currentIter = 1

    currentTemp = initialTemp
    currentSolution = solution.copy()
    currentSolutionValue = value(blueprint, currentSolution)

    print("Initial solution value:", currentSolutionValue)

    while currentTemp > finalTemp:
        print("Temperature:", currentTemp)
        # 10 iterations per temperature
        for _ in range(10):
            # Accept only a valid neighbour
            while True:
                neighbour, neighbourValue = randomNeighbour(blueprint, solution)
                if (neighbour, neighbourValue) == (None, None):
                    continue
                break

            delta = neighbourValue - currentSolutionValue

            # Neighbour is better that current solution
            if delta > 0:
                currentSolution, currentSolutionValue = neighbour, neighbourValue
                print("Upgrade! Value:", currentSolutionValue)
            elif delta == 0:
                pass
            # If Neighbour is worse, accept it with a probability of e^(delta/temperature)
            else:
                print("Probability: " + str(math.exp(delta / currentTemp)) +
                      "; delta: " + str(delta))
                if random.uniform(0, 1) < math.exp(delta / currentTemp):
                    currentSolution, currentSolutionValue = neighbour, neighbourValue
                    print("Upgrade! Value: " + str(currentSolutionValue))
        # decrement the temperature
        currentTemp = initialTemp * alpha ** currentIter
        currentIter += 1

    print("Solution value: " + str(currentSolutionValue))
    return currentSolution
