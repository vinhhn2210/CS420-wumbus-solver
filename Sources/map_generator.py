# this code to generate a map with obstacles and save it in a file
import random
import os
import sys
from mapstate import *

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
class WumpusWorldGenerator:
    def __init__(self, size, name, pitCoef = 0.1, wumpusMaximun = 10, goldMaximum = 10):
        self.size = int(size)
        self.name = name
        self.pitCoef = float(pitCoef)
        self.wumpusMaximun = min(int(wumpusMaximun), int(size))
        self.goldMaximum = min(int(goldMaximum), int(size))
        self.maze = [['-' for i in range(self.size)] for j in range(self.size)]
        self.generateMap()
        self.saveMap()

    def generateMap(self):
        # generate pit
        for i in range(self.size):
            for j in range(self.size):
                if random.random() < self.pitCoef and (i != self.size - 1 or j != self.size - 1):
                    self.maze[i][j] = 'P'
        # generate wumpus
        nWumpus = random.randint(1, self.wumpusMaximun)
        for _ in range(nWumpus):
            while True:
                x = random.randint(0, self.size -1)
                y = random.randint(0, self.size -1)
                if self.maze[x][y] == '-':
                    self.maze[x][y] = 'W'
                    break
        # generate gold
        nGold = random.randint(1, self.goldMaximum)
        for _ in range(nGold):
            while True:
                x = random.randint(0, self.size -1)
                y = random.randint(0, self.size -1)
                if self.maze[x][y] == '-':
                    self.maze[x][y] = 'G'
                    break
        mapState = MapState(self.name, self.size, self.maze)
        mapState.printMap()

    def saveMap(self):
        # create file and save map
        with open(os.path.join(CUR_PATH, 'Map', self.name + '.txt'), 'w') as f:
            f.write(str(self.size) + '\n')
            for i in range(self.size):
                for j in range(self.size - 1):
                    f.write(self.maze[i][j] + '.')
                f.write(self.maze[i][self.size - 1])
                f.write('\n')
        print('Map ' + self.name + ' is saved!')

if __name__ == '__main__':

    #for i in range(1, 11):
    #    WumpusWorldGenerator(10, 'map' + str(i))
    if len(sys.argv) > 6:
        print('Please input 5 arguments: size, name, pitCoef, wumpusMaximun, goldMaximum')
        exit()
    if len(sys.argv) < 3:
        for i in range(1, 11):
            WumpusWorldGenerator(10, 'map' + str(i))
    elif len(sys.argv) == 3:
        WumpusWorldGenerator(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        WumpusWorldGenerator(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5:
        WumpusWorldGenerator(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) == 6:
        WumpusWorldGenerator(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])