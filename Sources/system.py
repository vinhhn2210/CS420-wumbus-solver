from lists_of_algorithms import *
from mapstate import *
import os 
import json
import re
import sys
import time
import psutil
import tracemalloc
from matplotlib import pyplot as plt
# back to the parent folder
CUR_PATH = os.path.dirname(os.path.abspath(__file__))

def repl_func(match: re.Match):
    return " ".join(match.group().split())


# This is the main program for the project to navigate between frontend, backend and other class
class SystemController:
    def __init__(self):
        self.mapLists = {}
        self.timeCount = 0
        self.memoryCount = 0

    def measureStart(self):
        tracemalloc.clear_traces()
        self.timeCount = time.time()
        self.memoryCount = psutil.Process()

    def measureEnd(self):
        self.timeCount = time.time() - self.timeCount
        self.memoryCount = tracemalloc.get_traced_memory()[1] / (1024 ** 2)
        #self.memoryCount = self.memoryCount.memory_info().rss / (1024 ** 2)
        # print time, mem with 4 digits after comma
        self.timeCount = round(self.timeCount * 1000, 4)
        self.memoryCount = round(self.memoryCount, 4)
        print('\t\t+ Time: \t{} ms'.format(self.timeCount))
        print('\t\t+ Memory:\t{} Mib'.format(self.memoryCount))
        return self.timeCount, self.memoryCount

    def readAllFolderMap(self, folderPath):
        MAP_PATH = os.path.join(CUR_PATH, folderPath)
        for mapName in os.listdir(MAP_PATH):
            self.mapLists[mapName] = loadMap(folderPath, mapName)
    
    def writeSolution(self, mapName, algorithm, solution):
        with open(os.path.join(CUR_PATH, 'Solutions', 'result_' + mapName[:-4] + '_' + algorithm + '.txt'), 'w') as f:
            f.write(str(len(solution)) + '\n')
            for step in solution:
                f.write(str(step)[1: -1] + '\n')
        print('\t\t+ Solution is written to file result_' + mapName[:-4] + '_' + algorithm + '.txt')
    def printMap(self, mapName):
        self.mapLists[mapName].printMap()

    def printMapList(self):
        for mapName in self.mapLists:
            print('-' * 50)
            self.printMap(mapName)

    def solvingAllMap(self):
        for mapName in self.mapLists:
            for algo in algo_lists:
                self.solving(mapName, algo)

    def solving(self, mapName, algorithm):
        print('-' * 50)
        print('\t+ Solving ' + mapName + ' with ' + algorithm + ' algorithm...')
        self.measureStart()
        solution = None
        if algorithm == 'dpll':
            print("\t\t+ DPLL algorithm is not implemented yet!")
            solution = [(1, 2, 100), (1, 3, 200), (2, 3, 300)]
        elif algorithm == 'fol':
            print("\t\t+ FOL algorithm is not implemented yet!")
            solution = [(1, 2, 100), (2, 2, 0), (3, 2, 50)]
        else:
            print("\t\t+ Algorithm is not exist!")
            return None
        
        self.measureEnd()
        
        if solution is None:
            print('\t+ No solution found!')
            return None
        print('\t\t+ Solution found!')
        self.writeSolution(mapName, algorithm, solution)
        print('\t+ Solving ' + mapName + ' with ' + algorithm + ' algorithm is done!')

if __name__ == '__main__':
    if len(sys.argv) != 3 or (sys.argv[2] != 'auto' and sys.argv[2] != 'custom'):
        print('Please enter the correct command')
        print('1. To automaticly solving all map with all current algorithms:\n\t python3 Sources/system.py Map auto')
        print('2. to solve with specify map-algorithm:\n\t python3 Sources/system.py Map custom')
        exit()
     
    system = SystemController()
    # Reading map from folder
    print('Folder ' + sys.argv[1] + ' is being processed...')
    system.readAllFolderMap(sys.argv[1])
    print('Load folder: ' + sys.argv[1] + ' is done!')
    print("List of map: ")
    system.printMapList()
    # solving map
    print('-' * 50)
    tracemalloc.start()
    if sys.argv[2] == 'auto':
        print('Solving all map with all current algorithms...')
        system.solvingAllMap()
    elif sys.argv[2] == 'custom':
        print('Please choose the map you want to solve, for example: input1-level1')
        mapName = input('Enter the map name: ')
        if mapName not in system.mapLists:
            print('Map name is not exist!')
            exit()
        print('Please choose the algorithm you want to solve, for example: dfs ')
        for i, algo in enumerate(algo_lists):
            print(f'{i + 1}. {algo}')
        algorithm = input('Enter the algorithm name: ')
        if algorithm == 'dpll':
            system.solving(mapName, 'dpll')
        elif algorithm == 'fol':
            system.solving(mapName, 'fol')
        else:
            print('Algorithm is not exist!')
            exit()
        print('Solving ' + mapName + ' with ' + algorithm + ' algorithm is done!')
    tracemalloc.stop()
    # done and visualize the solution
    print('-' * 50)
    print('Program is done!')
    print('To visualize the solution, please run the main.py file')
    print('\t python3 main.py')
    print('Thank you for using our program!')
