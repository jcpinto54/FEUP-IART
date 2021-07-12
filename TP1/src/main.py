import random
import geneticAlgorithm
import hillClimbing
import tabuSearch
import simulatedAnnealing
import utils
import blueprint as bp
import time


def menu():
    print("IART - Router Placement")

    while True:
        print("\nFile input")
        print("[1] example.in (8x22)")
        print("[2] labirinto.in (3x7)")
        print("[3] enunciado.in (7x16)")
        print("[4] another_example.in (8x22)")
        print("[5] charleston_road.in (240x180)")
        print("[6] rue_de_londres.in (559x404)")
        print("[7] opera.in (667x540)")
        print("[8] lets_go_higher.in (872x975)")
        print("[0] Quit")
        file = input("File input: ")

        if file == str(1):
            file = "../inputs/example.in"
        elif file == str(2):
            file = "../inputs/labirinto.in"
        elif file == str(3):
            file = "../inputs/enunciado.in"
        elif file == str(4):
            file = "../inputs/another_example.in"
        elif file == str(5):
            file = "../inputs/charleston_road.in"
        elif file == str(6):
            file = "../inputs/rue_de_londres.in"
        elif file == str(7):
            file = "../inputs/opera.in"
        elif file == str(8):
            file = "../inputs/lets_go_higher.in"
        elif file == str(0):
            break
        else:
            print("File not found\n")
            continue

        blueprint = bp.Blueprint(file)

        print("Choose algorithm to run")
        print("[1] Simulated Annealing")
        print("[2] Hill Climbing: Regular")
        print("[3] Hill Climbing: Steepest Ascent")
        print("[4] Genetic Algorithm")
        print("[5] Tabu Search")
        print("[0] Quit")
        val = input("Option: ")

        algorithmName = ""

        startTime = time.time()
        if val == str(1):
            print("Generating initial solution...")
            solution = utils.generateSolution(blueprint)
            print("Generated initial solution.")
            solution = simulatedAnnealing.simulatedAnnealing(blueprint, solution)
            algorithmName = "annealing"
        elif val == str(2):
            print("Generating initial solution...")
            solution = utils.generateSolution(blueprint)
            print("Generated initial solution.")
            solution = hillClimbing.hillClimbing(blueprint, solution)
            algorithmName = "hill_climbing_regular"
        elif val == str(3):
            print("Generating initial solution...")
            solution = utils.generateSolution(blueprint)
            print("Generated initial solution.")
            solution = hillClimbing.hillClimbingSteepestAscent(blueprint, solution)
            algorithmName = "hill_climbing_steepest"
        elif val == str(4):
            solution = geneticAlgorithm.geneticAlgorithm(blueprint)
            algorithmName = "genetic"
        elif val == str(5):
            print("Generating initial solution...")
            solution = utils.generateSolution(blueprint)
            print("Generated initial solution.")
            solution = tabuSearch.tabuSearch(blueprint, solution)
            algorithmName = "tabu"
        elif val == str(0):
            break
        else:
            print("Algorithm not found\n")
            continue
        endTime = time.time()

        outFileName = file.split("/")
        outFileName = outFileName[-1]
        outFileName = outFileName.split(".")
        outFileName = outFileName[0] + "/" + algorithmName

        blueprint.printSolutionCoverage(solution)
        blueprint.printSolutionPaths(solution)
        print(f"\nTime: {endTime - startTime} seconds\n")
        blueprint.plotSolution(solution, "../out/" + outFileName + ".png")
        utils.printSolToFile(solution, endTime - startTime, blueprint, "../out/" + outFileName + ".txt")

        print("------------------------------------------------------------------------------------------------")
                

if __name__ == "__main__":
    menu()
