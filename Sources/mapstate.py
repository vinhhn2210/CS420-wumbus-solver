import os
from colorama import Fore
import copy
CUR_PATH = os.path.dirname(os.path.abspath(__file__))

class MapState:
    def __init__(self, name, nSize, mazer = []):
        self.name = name
        self.nSize = nSize
        self.mazer = copy.deepcopy(mazer)
    
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
    return MapState(mapName, nSize, mazer)


'''
S is stench, W is wumpus, G is gold, P is pit, B is breeze, - is nothing, . is separator
4
S.-.B.P
W.BGS.P.B
S.-.B.-
-.B.P.B
Example of map file
    '''