from lists_of_algorithms import *
from mapstate import *
from interactive import *
from algo_sample import *
from algo_dpll import *
from algo_nerd import *
from algo_bc_fc import *
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


# This is the main program for the project to navigate between map and algorithm
# DO NOT MODIFY THIS FILE
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
        self.timeCount = round(self.timeCount, 4)
        self.memoryCount = round(self.memoryCount, 4)
        # add color to time and memory
        print('\t\t+ Time:\t\t' + '\033[93m' + str(self.timeCount) + '\033[0m' + ' s')
        print('\t\t+ Memory:\t' + '\033[93m' + str(self.memoryCount) + '\033[0m' + ' MB')
        return self.timeCount, self.memoryCount

    def readAllFolderMap(self, folderPath):
        MAP_PATH = os.path.join(CUR_PATH, folderPath)
        for mapName in os.listdir(MAP_PATH):
            self.mapLists[mapName[:-4]] = loadMap(folderPath, mapName)
    
    def writeSolution(self, mapName, algorithm, solution):
        with open(os.path.join(CUR_PATH, 'Solutions', '[result]_' + mapName + '_' + algorithm + '.txt'), 'w') as f:
            f.write(str(len(solution)) + '\n')
            for step in solution:
                f.write(str(step)[1: -1] + '\n')

        # add color to result_ + mapName + '_' + algorithm + '.txt
        print('\t\t+ Result file: ' + '\033[93m' + '[result]_' + mapName + '_' + algorithm + '.txt' + '\033[0m')
    
    def writeKBsolution(self, mapName, algorithm, solution):
        with open(os.path.join(CUR_PATH, 'Solutions', '[KB]_' + mapName + '_' + algorithm + '.txt'), 'w') as f:
            f.write(str(len(solution)) + '\n')
            for step in solution:
                f.write(str(step) + '\n')

        # add color to result_ + mapName + '_' + algorithm + '.txt
        print('\t\t+ Result file: ' + '\033[93m' + '[KB]_' + mapName + '_' + algorithm + '.txt' + '\033[0m')

    def writeJson(self, mapName, algorithm, solution):
        solution["0"]['time'] = self.timeCount
        solution["0"]['memory'] = self.memoryCount
        with open(os.path.join(CUR_PATH, 'Solutions', '[visualize]_' + mapName + '_' + algorithm + '.json'), 'w') as f:
            json_str = json.dumps(solution, indent=4)
            json_str = re.sub(r"(?<=\[)[^\[\]]+(?=])", repl_func, json_str)
            f.write(json_str)
            # json.dump(solution, f)

        # add color to result_ + mapName + '_' + algorithm + '.json
        print('\t\t+ Result file: ' + '\033[93m' + '[visualize]_' + mapName + '_' + algorithm + '.json' + '\033[0m')
    
    def printMap(self, mapName):
        self.mapLists[mapName].printMap()

    def printMapList(self):
        for mapName in self.mapLists:
            print('-' * 50)
            self.printMap(mapName)

    def solvingAllMap(self):
        for mapName in self.mapLists:
            algo_lists = ['bc_fc', 'nerd']
            for algo in algo_lists:
                self.solving(mapName, algo)

    def solving(self, mapName, algorithm):
        print('-' * 50)
        print('\t+ Solving ' + mapName + ' with ' + algorithm + ' algorithm...')
        self.measureStart()
        solution = None
        model = None
        if algorithm == 'sample':
            print("\t\t+ Sample algorithm")
            model = AlgoSample(self.mapLists[mapName])
        elif algorithm == 'dpll':
            print("\t\t+ DPLL algorithm")
            model = DPLLAlgo(self.mapLists[mapName])
            #solution = [(1, 2, 1, 100), (1, 3, 1, 200), (2, 3, 1, 300)]
        elif algorithm == 'fol':
            print("\t\t+ FOL algorithm is not implemented yet!")
            #solution = [(1, 2, 1, 100), (2, 2, 1, 0), (3, 2, 1, 50)]
        elif algorithm == 'nerd':
            print("\t\t+ Nerd algorithm!")
            # solution = nerve(self.mapLists[mapName], 0)
            model = Nerd(self.mapLists[mapName])
        elif algorithm == 'bc_fc':
            print("\t\t+ Backward chaining + Forward chaining algorithm!")
            model = BackAndForwardChaining(self.mapLists[mapName])
        else:
            print("\t\t+ Algorithm is not exist!")
            return None
        if model is not None:
            solution = model.solve()

        self.measureEnd()
        
        if solution is None:
            print('\t+ No solution found!')
            return None

        self.writeSolution(mapName, algorithm, solution[0])
        self.writeJson(mapName, algorithm, solution[1])
        self.writeKBsolution(mapName, algorithm, solution[2])
        # add color to mapname and algorith name
        mapName = '\033[94m' + mapName + '\033[0m'
        algorithm = '\033[92m' + algorithm + '\033[0m'
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
        
        # mapName = 'map1'
        # algorithm = 'bc_fc'
        # algorithm = 'nerd'
        # system.solving(mapName, algorithm)
    elif sys.argv[2] == 'custom':
        print('Please choose the map you want to solve, for example: map1')
        mapName = input('Enter the map name: ')
        if mapName not in system.mapLists:
            print('Map name is not exist!')
            exit()
        print('Please choose the algorithm you want to solve, for example: sample')
        for i, algo in enumerate(algo_lists):
            print(f'{i + 1}. {algo}')
        algorithm = input('Enter the algorithm name: ')
        print(algo_lists)
        if algorithm not in algo_lists:
            print('Algorithm is not exist!')
            exit()
        system.solving(mapName, algorithm)
        print('Solving ' + mapName + ' with ' + algorithm + ' algorithm is done!')
    tracemalloc.stop()
    # done and visualize the solution
    print('-' * 50)
    print('Program is done!')
    print('To visualize the solution, please run the main.py file')
    print('\t python3 main.py')
    print('Thank you for using our program!')