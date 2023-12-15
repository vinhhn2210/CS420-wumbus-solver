import copy
import random
class InteractiveGame:
    def __init__(self):
        self.size = 0
        self.mazer = []
        self.playerPosition = (0, 0, 0) # (x, y, direction), direction = 0: up, 1: right, 2: down, 3: left
        self.score = 0
        self.isEnd = False
        self.logs = []
        self.directions = {'UP': 0, 'RIGHT': 1, 'DOWN': 2, 'LEFT': 3}
        self.dx = [-1, 0, 1, 0]
        self.dy = [0, 1, 0, -1]
    
    def flushLog(self):
        self.logs.append(self.playerPosition + (self.score, 0))

    def getLogs(self):
        return self.logs

    def loadMap(self, mapState):
        self.size = mapState.nsize
        self.mazer = copy.deepcopy(mapState.maze)

    def gameStart(self):
        self.score = 0
        self.isEnd = False
        self.logs = []
        # get random position for player which is valid
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.mazer[x][y] == '-':
                self.playerPosition = (x, y, 0)
                break
        self.flushLog()
        return self.playerPosition
    
    
    def getPlayerPosition(self):
        return self.playerPosition
    
    def getScore(self):
        return self.score
    
    def getCellView(self):
        x, y, _ = self.playerPosition
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
    
    def move(self, action):
        if self.isEnd:
            print('Game is already ended, please start a new game!')
            return False
        if action not in self.directions:
            return False
        if self.playerPosition[2] != self.directions[action]:
            self.playerPosition[2] = self.directions[action]
            self.flushLog()
            return True
        else:
            x, y, dir = self.playerPosition
            newX = x + self.dx[dir]
            newY = y + self.dy[dir]
            if newX <= 0 or newX > self.size or newY <= 0 or newY > self.size:
                return False
            self.playerPosition = (newX, newY, self.playerPosition[2])
            self.score -= 10
            if self.isGold():
                self.score += 1000
                self.flushLog()
                return True
            elif self.isWumpus() or self.isPit():
                self.score -= 10000
                self.flushLog()
                self.gameEnd()
                return True
            
    def gameEnd(self):
        self.isEnd = True
        print('Game ended with score: ' + str(self.score))
        
            

'''
S is stench, W is wumpus, G is gold, P is pit, B is breeze, - is nothing, . is separator
4
S.-.B.P
W.BGS.P.B
S.-.B.-
-.B.P.B
Example of map file
    '''