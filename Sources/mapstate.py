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
        self.initialPos = (3, 0, 0)
        # flip map vertically
        self.mazer = self.mazer[::-1]
        for i in range(nSize):
            for j in range(nSize):
                if self.mazer[i][j] != 'W' and self.mazer[i][j] != 'P':
                    # check if there is a pit in 4 adjacent cells
                    if i > 0 and self.mazer[i - 1][j] == 'P':
                        self.mazer[i][j] += 'B'
                    elif i < nSize - 1 and self.mazer[i + 1][j] == 'P':
                        self.mazer[i][j] += 'B'
                    elif j > 0 and self.mazer[i][j - 1] == 'P':
                        self.mazer[i][j] += 'B'
                    elif j < nSize - 1 and self.mazer[i][j + 1] == 'P':
                        self.mazer[i][j] += 'B'
                    # check if there is a wumpus in 4 adjacent cells
                    if i > 0 and self.mazer[i - 1][j] == 'W':
                        self.mazer[i][j] += 'S'
                    elif i < nSize - 1 and self.mazer[i + 1][j] == 'W':
                        self.mazer[i][j] += 'S'
                    elif j > 0 and self.mazer[i][j - 1] == 'W':
                        self.mazer[i][j] += 'S'
                    elif j < nSize - 1 and self.mazer[i][j + 1] == 'W':
                        self.mazer[i][j] += 'S'
                if len(self.mazer[i][j]) == 0:
                    self.mazer[i][j] = '-'
                if len(self.mazer[i][j]) > 1 and '-' in self.mazer[i][j]:
                    self.mazer[i][j] = self.mazer[i][j].replace('-', '')
        # get random position for player which is valid
        while True:
            x = random.randint(0, self.nSize -1)
            y = random.randint(0, self.nSize -1)
            if self.mazer[x][y] == '-':
                self.initialPos = (x, y, 0)
                break
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
''''''
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