# this code to generate a map with obstacles and save it in a file
import random
import os

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
class WumpusWorldGenerator:
    def __init__(self, size, name):
        self.size = size
        self.name = name
        self.maze = [['-' for i in range(self.size)] for j in range(self.size)]
        self.generateMap()
        self.saveMap()

    def generateMap(self):
        # generate pit
        for i in range(self.size):
            for j in range(self.size):
                if random.random() < 0.1:
                    self.maze[i][j] = 'P'
        # generate wumpus
        nWumpus = random.randint(1, 10)
        for _ in range(nWumpus):
            while True:
                x = random.randint(0, self.size -1)
                y = random.randint(0, self.size -1)
                if self.maze[x][y] == '-':
                    self.maze[x][y] = 'W'
                    break
        # generate gold
        nGold = random.randint(1, 10)
        for _ in range(nGold):
            while True:
                x = random.randint(0, self.size -1)
                y = random.randint(0, self.size -1)
                if self.maze[x][y] == '-':
                    self.maze[x][y] = 'G'
                    break

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
    for i in range(1, 11):
        WumpusWorldGenerator(10, 'map' + str(i))