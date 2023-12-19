import os
from colorama import Fore
import copy
import random
CUR_PATH = os.path.dirname(os.path.abspath(__file__))

class MapState:
    def __init__(self, name, nSize, mazer = []):
        self.name = name
        self.nSize = nSize
        self.mazer = copy.deepcopy(mazer)
        # self.initialPos = generatePlayer(mazer, nSize)
        # self.initialPos = (3, 0, 'R')
        self.initialPos = (3, 0)
    
    def printMap(self):
        print('Map name: ' + self.name)
        print('Map size: ' + str(self.nSize) + ' x ' + str(self.nSize))
        for i in range(self.nSize):
            for j in range(self.nSize):
                for ch in self.mazer[i][j]:
                    if ch == 'S':
                        print(Fore.RED + ch, end = '')
                    elif ch == 'W':
                        print(Fore.GREEN + ch, end = '')
                    elif ch == 'G':
                        print(Fore.YELLOW + ch, end = '')
                    elif ch == 'P':
                        print(Fore.MAGENTA + ch, end = '')
                    elif ch == 'B':
                        print(Fore.CYAN + ch, end = '')
                    elif ch == '-':
                        print(Fore.WHITE + ch, end = '')
                print(Fore.WHITE + ' ', end = '\t')
            print()
        print('Map end')

def loadMap(folderPath, mapName):
    MAP_PATH = os.path.join(CUR_PATH, folderPath, mapName)
    with open(MAP_PATH, 'r') as f:
        nSize = int(f.readline())
        mazer = []
        for i in range(nSize):
            mazer.append(f.readline().strip().split('.'))
    return MapState(mapName[:-4], nSize, mazer)

def generatePlayer(mazer, nSize):
    '''call this only once'''
    # random a valid position not 'G', 'W', 'P' in map
    valid = []
    for i in range(nSize):
        for j in range(nSize):
            if 'G' not in mazer[i][j] and 'W' not in mazer[i][j] and 'P' not in mazer[i][j]:
                valid.append((i, j))
    # random a position
    pos = random.choice(valid)
    choice = ['U', 'D', 'L', 'R']
    if pos[0] == 0:
        choice.remove('U')
    if pos[0] == nSize - 1:
        choice.remove('D')
    if pos[1] == 0:
        choice.remove('L')
    if pos[1] == nSize - 1:
        choice.remove('R')
    direction = random.choice(choice)
    return pos[0], pos[1], direction

'''
S is stench, W is wumpus, G is gold, P is pit, B is breeze, - is nothing, . is separator
4
S.-.B.P
W.BGS.P.B
S.-.B.-
-.B.P.B
Example of map file
    '''