import time
import blueprint as bp
from utils import *
import utils


def getTabuStructure(blueprint,solution):
    """
    Initializes the tabu data structure.
    :param blueprint:
    :param solution:
    :return: Returns a dictionnary with tuples of the format (routerNumber, xOrY, upOrDown, numberOfRouters) as keys
    """

    dict = {}
    index = 0
    for i in solution:
        aux1 = (index, 0, 0, len(solution))
        aux2 = (index, 0, 1, len(solution))
        aux3 = (index, 1, 0, len(solution))
        aux4 = (index, 1, 1, len(solution))
        aux5 = (index, 0, -1, len(solution))
        dict[aux1] = {'tabuTime': 0, 'MoveValue': 0}
        dict[aux2] = {'tabuTime': 0, 'MoveValue': 0}
        dict[aux3] = {'tabuTime': 0, 'MoveValue': 0}
        dict[aux4] = {'tabuTime': 0, 'MoveValue': 0}
        dict[aux5] = {'tabuTime': 0, 'MoveValue': 0}
        index = index + 1

    return dict


def tabuSearch(blueprint, solution):
    """
    Implementation of tabu search algorithm.
    :param blueprint:
    :param solution:
    :return: Returns the best found solution of router coords
    """

    tabuTenure = 10
    tabuStructure = getTabuStructure(blueprint, solution)
    bestSolution = solution
    bestValue = value(blueprint, bestSolution)
    currentSolution = solution
    currentValue = value(blueprint, currentSolution)

    iter = 1
    terminate = 0
    while terminate < 50:
        print('\n\n### Iteration {} ###  Current Value: {}, Best Value: {}'.format(iter, currentValue, bestValue))
        
        number = 0
        
        # searching all the possible neighbours for the current solution
        for i in tabuStructure:
            candidateSolution, candidateValue = utils.neighbour(blueprint, currentSolution, i[0], i[1], i[2], i[3])
            if candidateValue is not None:
                tabuStructure[i]['MoveValue'] = candidateValue
            else: 
                tabuStructure[i]['MoveValue'] = 0

    
        while True:
            # selecting the move with the highest value from all neighbours
            bestMove = max(tabuStructure, key=lambda x: tabuStructure[x]['MoveValue'])
            moveValue = tabuStructure[bestMove]["MoveValue"]
            tabuTime = tabuStructure[bestMove]["tabuTime"]

            # not in the tabu list
            if tabuTime < iter:
                
                # make the move
                currentSolution, currentValue = utils.neighbour(blueprint, currentSolution, bestMove[0], bestMove[1], bestMove[2], bestMove[3])
                if currentValue is None:
                    currentValue = 0
                
                if moveValue > bestValue:
                    bestSolution = currentSolution
                    bestValue = currentValue
                    print("   Best Move: {}, Value: {} => Best Improving => Admissible".format(bestMove, currentValue))
                    terminate = 0
                
                # update tabu time for the move
                else:
                    print("   ## Termination: {} ## Best Move: {}, Value: {} => Least non-improving => " "Admissible".
                          format(terminate, bestMove, currentValue))
                    terminate += 1

                tabuStructure[bestMove]['tabuTime'] = iter + tabuTenure
                iter += 1
                break

            # in tabu
            else:

                    
                if moveValue > bestValue:
                    
                    # make the move
                    currentSolution, currentValue = utils.neighbour(blueprint, currentSolution, bestMove[0], bestMove[1], bestMove[2], bestMove[3])
                    bestSolution = currentSolution
                    bestValue = currentValue
                    print("   Best Move: {}, Value: {} => Aspiration => Admissible".format(bestMove, currentValue))
                    terminate = 0
                    iter += 1
                    break
                else:
                    tabuStructure[bestMove]["MoveValue"] = float('-inf')
                    terminate += 1
                    print("   Best Move: {}, Value: {} => Tabu => Inadmissible".format(bestMove, currentValue))
                    break
                
    print('\n', '#' * 50, "Performed iterations: {}".format(iter), "Best found Solution: {} , Value: {}".
          format(bestSolution, bestValue), sep="\n")
    return bestSolution