import copy
import random
from mapstate import *
class InteractiveGame:
    def __init__(self):
        self.size = 0
        self.mazer = []
        self.explored = [] # explored[x][y] = true if cell (x, y) is explored before
        self.playerPosition = (0, 0, 0) # (x, y, direction), direction = 0: up, 1: right, 2: down, 3: left
        self.score = 0
        self.isEnd = False
        self.directions = {'UP': 0, 'RIGHT': 1, 'DOWN': 2, 'LEFT': 3}
        self.dx = [-1, 0, 1, 0]
        self.dy = [0, 1, 0, -1]
        self.logs = []
        self.jsonData = {}
        self.KBlogs = []
    def flipDirection(self, direction):
        return (direction + 2) % 4

    def appendKBLog(self, log):
        self.KBlogs.append(log)

    def flushLog(self):
        self.logs.append((self.playerPosition[0], self.playerPosition[1], self.flipDirection(self.playerPosition[2]), self.score))
        visionMaze = copy.deepcopy(self.mazer)
        for i in range(self.size):
            for j in range(self.size):
                if self.explored[i][j] == False:
                    visionMaze[i][j] = 'X'
        self.jsonData[str(len(self.logs) - 1)] = {
            "mapSize": self.size,
            "map": self.mazer[::-1],
            "vision": visionMaze[::-1],
            "agent": [self.playerPosition[0], self.playerPosition[1], self.flipDirection(self.playerPosition[2]), self.score],
        }

    def debug(self):
        print('player position:', self.playerPosition, 'score:', self.score)
        debugMaze = copy.deepcopy(self.mazer)
        debugMaze[self.playerPosition[0]][self.playerPosition[1]] += 'A'
        for i in range(self.size):
            for j in range(self.size):
                for ch in debugMaze[i][j]:
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
                    elif ch == 'A':
                        print(Fore.BLUE + ch, end = '')
                print(Fore.WHITE + ' ', end = '\t')
            print(end = '\t\t')
            for j in range(self.size):
                if self.explored[i][j] == False:
                    print(Fore.WHITE + 'X', end = '\t')
                    continue
                for ch in debugMaze[i][j]:
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
                    elif ch == 'A':
                        print(Fore.BLUE + ch, end = '')
                print(Fore.WHITE + ' ', end = '\t')
            print()

    def getLogs(self):
        return self.logs, self.jsonData, self.KBlogs

    def getJsonLogs(self):
        return self.jsonData

    def isGoal(self):
        return self.playerPosition[0] == 0 and self.playerPosition[1] == 0

    def loadMap(self, mapState):
        self.size = mapState.nSize
        self.mazer = copy.deepcopy(mapState.mazer)  
        self.explored = [[False for i in range(self.size)] for j in range(self.size)]
        self.playerPosition = mapState.initialPos

    def gameStart(self):
        self.score = 0
        self.isEnd = False
        self.logs = []
        self.explored = [[False for i in range(self.size)] for j in range(self.size)]
        self.explored[self.playerPosition[0]][self.playerPosition[1]] = True
        self.flushLog()
        visionMaze = copy.deepcopy(self.mazer)
        for i in range(self.size):
            for j in range(self.size):
                if self.explored[i][j] == False:
                    visionMaze[i][j] = 'X'
        self.jsonData = {
            "0": {
                "time": 0,
                "memory": 0,
                "mapSize": self.size,
                "map": self.mazer[::-1],
                "vision": visionMaze[::-1],
                "agent": [self.playerPosition[0], self.playerPosition[1], self.playerPosition[2], self.score],
            },
        }
        return self.playerPosition
    
    
    def getPlayerPosition(self):
        return self.playerPosition
    
    def getScore(self):
        return self.score
    
    def getCellView(self):
        x, y, _ = self.playerPosition
        return self.mazer[x][y]
    
    def getCell(self, x, y):
        return self.mazer[x][y]

    def isPit(self):
        for value in self.getCellView():
            if value == 'P':
                return True
        return False
    
    def isWumpus(self):
        for value in self.getCellView():
            if value == 'W':
                return True
        return False
    
    def isGold(self):
        for value in self.getCellView():
            if value == 'G':
                return True
        return False
    
    def isStench(self):
        for value in self.getCellView():
            if value == 'S':
                return True
        return False
    
    def isBreeze(self):
        for value in self.getCellView():
            if value == 'B':
                return True
        return False
    
    def isStenchVisionView(self, x, y):
        if self.explored[x][y] == False:
            return -1
        return self.explored[x][y] == True and 'S' in self.mazer[x][y]
    
    def isBreezeVisionView(self, x, y):
        if self.explored[x][y] == False:
            return -1
        return self.explored[x][y] == True and 'B' in self.mazer[x][y]

    def isNone(self):
        return self.getCellView() == '-'
    
    # def isVisited(self):
    #     return self.explored[self.playerPosition[0]][self.playerPosition[1]]
    
    def moveImmediately(self, action):
        curPos = self.getPlayerPosition()
        self.move(action)
        newPos = self.getPlayerPosition()
        if newPos[0] == curPos[0] and newPos[1] == curPos[1]:
            self.move(action)

    def changeDirection(self, action):
        self.playerPosition = (self.playerPosition[0], self.playerPosition[1], self.directions[action])
        self.flushLog()

    def move(self, action):
        if self.isEnd:
            print('Game is already ended, please start a new game!')
            return False
        if action not in self.directions:
            return False
        if self.playerPosition[2] != self.directions[action]:
            self.playerPosition = (self.playerPosition[0], self.playerPosition[1], self.directions[action])
            self.flushLog()
            return True
        else:
            x, y, dir = self.playerPosition
            newX = x + self.dx[dir]
            newY = y + self.dy[dir]
            if newX < 0 or newX >= self.size or newY < 0 or newY >= self.size:
                self.score -= 10000000
                self.flushLog()
                self.gameEnd()
                return False
            self.playerPosition = (newX, newY, self.playerPosition[2])
            self.score -= 10
            self.explored[newX][newY] = True
            if self.isGold():
                self.score += 1000
                self.mazer[self.playerPosition[0]][self.playerPosition[1]] = self.mazer[self.playerPosition[0]][self.playerPosition[1]].replace('G', '')
                if len(self.mazer[self.playerPosition[0]][self.playerPosition[1]]) == 0:
                    self.mazer[self.playerPosition[0]][self.playerPosition[1]] = '-'
                self.flushLog()
                return True
            elif self.isWumpus() or self.isPit():
                self.score -= 10000
                self.flushLog()
                self.gameEnd()
                return True
            else:
                self.flushLog()
                return True
    
    def connectedRooms(self, x, y):
        connected = []
        for i in range(4):
            newX = x + self.dx[i]
            newY = y + self.dy[i]
            if newX < 0 or newX >= self.size or newY < 0 or newY >= self.size:
                continue
            connected.append((newX, newY))
        return connected
    
    def killWumpus(self, x, y):
        for i in self.connectedRooms(x, y):
            # check if this room connect with wumpus
            noWumpus = True
            for j in self.connectedRooms(i[0], i[1]):
                if 'W' in self.mazer[j[0]][j[1]]:
                    noWumpus = False
                    break
            if noWumpus:
                self.mazer[i[0]][i[1]] = self.mazer[i[0]][i[1]].replace('S', '')
                if len(self.mazer[i[0]][i[1]]) == 0:
                    self.mazer[i[0]][i[1]] = '-'
        
    
    def shootArrow(self):
        if self.isEnd:
            print('Game is already ended, please start a new game!')
            return False
        self.score -= 100
        self.flushLog()
        nextX = self.playerPosition[0] + self.dx[self.playerPosition[2]]
        nextY = self.playerPosition[1] + self.dy[self.playerPosition[2]]
        if 'W' in self.mazer[nextX][nextY]:
            # remove w in maze
            self.mazer[nextX][nextY] = self.mazer[nextX][nextY].replace('W', '')
            if len(self.mazer[nextX][nextY]) == 0:
                self.mazer[nextX][nextY] = '-'
            self.explored[nextX][nextY] = True
            self.killWumpus(nextX, nextY)
            # print(Fore.RED + "You killed the Wumpus!")
            # MapState('agentMap', self.size, self.mazer).printMap()
            #self.score += 100
            #self.flushLog()
            #self.gameEnd()
            return True
        else:
            return False

    def gameEnd(self):
        self.debug()
        self.isEnd = True
        # add color to game score
        print('\t\t+ Score:\t' + '\033[93m' + str(self.score) + '\033[0m')  
        
            

'''
S is stench, W is wumpus, G is gold, P is pit, B is breeze, - is nothing, . is separator
4
S.-.B.P
W.BGS.P.B
S.-.B.-
-.B.P.B
Example of map file
    '''