import logging
from mapstate import *
from interactive import *
'''
1. If you want to get the current position of agent, call
    + self.interactive.getPlayerPosition() 
    -> return (x, y, direction), direction = 0: up, 1: right, 2: down, 3: left

2. if you want to move agent to left, right, up, down, call 
    + self.interactive.move('UP'),
    + self.interactive.move('DOWN'),
    + self.interactive.move('LEFT'),
    + self.interactive.move('RIGHT'),
    + if same direction, agent will move forward else agent will turn to new direction

3. If you want to shoot arrow, call
    + self.interactive.shootArrow() -> Shoot in current direction, return True if shoot wumbus successfully, False otherwise

4. If you want to get the current score of agent, call
    + self.interactive.getScore() -> return int

5. + self.interactive.isStench() -> return True if agent is in stench, False otherwise
    + self.interactive.isBreeze() -> return True if agent is in breeze, False otherwise
    + self.interactive.isGold() -> return True if agent get a goal, False otherwise
'''

CONVERT = {'B': 1, 'S': 2, 'BS': 3}


class Nerve:
    def __init__(self, mapState):
        self.interactive = InteractiveGame()
        self.interactive.loadMap(mapState)
        self.view = {}
        self.estimate = {} # self.estimate[(i, j)] = 1: B, 2: S, 3: BS
        self.door = (self.interactive.size - 1, 0)
        self.safe = []
        self.parent = {}
        

    def possibleMove(self, playerPos):
        ''' return a list of possible move from the current position'''
        # print(Fore.YELLOW + "Player position: ", playerPos)
        available = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        nSize = self.interactive.size
        if playerPos[0] == 0:
            available.remove((-1, 0, 'UP'))
        if playerPos[0] == nSize - 1:
            available.remove((1, 0, 'DOWN'))
        if playerPos[1] == 0:
            available.remove((0, -1, 'LEFT'))
        if playerPos[1] == nSize - 1:
            available.remove((0, 1, 'RIGHT'))
        move = []
        for i in available:
            move.append((playerPos[0] + i[0], playerPos[1] + i[1], i[2]))
        return move
    
    def newMove(self, playerPos):
        '''return a list of new move from the current position'''
        return [i for i in self.possibleMove(playerPos) if (i[0], i[1]) not in self.view]

    
    def agentMap(self):
        nSize = self.interactive.size
        temp = [[[] for i in range(nSize)] for j in range(nSize)]
        for i in range(nSize):
            for j in range(nSize):
                if (i, j) not in self.view:
                    # view[i, j] = ['x']
                    temp[i][j] = ['x']
                else:
                    temp[i][j] = self.view[(i, j)]
                    # temp[i][j] = view[(i, j)]
                    # temp[i][j] = ']
        print(Fore.YELLOW + "Agent map: ")
        MapState('agentMap', nSize, temp).printMap()
        
        
    def escape(self):
        player = self.interactive.getPlayerPosition()
        self.safe = [self.door]
        if self.travelNextMove(player):
            # nextDoor = self.interactive.getPlayerPosition()
            # self.interactive.move('DOWN')
            # player = self.interactive.getPlayerPosition()
            # if (player[0], player[1]) == (nextDoor[0], nextDoor[1]):
                # self.interactive.move('DOWN')
            pass
        else:
            print(Fore.RED + "Cannot escape" + Fore.WHITE)
    
    def findNextMove(self, previous):
        '''find the optimal safe position'''
        visit = [(previous[0], previous[1], None, self.interactive.getScore())]
        self.parent = {}
        self.parent[(previous[0], previous[1])] = None
        while (visit):
            current = visit.pop(0)
            # print("\nConsider", Fore.CYAN + f'{current}')
            if (current[0], current[1]) in self.safe:
                break
            for i in self.possibleMove((current[0], current[1])):
                # print(Fore.WHITE + "Check", i, "is in", self.safe)
                if (i[0], i[1]) in self.view and (i[0], i[1]) not in self.parent:
                    # print("Repeat this step", Fore.RED + f'{i}')
                    self.parent[(i[0], i[1])] = current
                    visit.append((i[0], i[1], i[2], current[3] - 10))
                if (i[0], i[1]) in self.safe:
                    self.parent[(i[0], i[1])] = current
                    current = i
                    destination = current
                    flag = True
                    # print("Found safe position", Fore.YELLOW + f'{destination}')
                    return current
        if (current[0], current[1]) not in self.safe:
            return None
        
    def travelNextMove(self, previous):
        path = []
        current = self.findNextMove(previous)
        if (current == None):
            return False
        # print(Fore.CYAN + "Destination: ", destination)
        while (current):
            path.append(current)
            current = self.parent[(current[0], current[1])]
        path = path[::-1]
        path.pop(0)
        # print(Fore.WHITE + "    Path: ", path)
        for i in path:
            # print(Fore.WHITE + "    Move to", i[2])
            cur = self.interactive.getPlayerPosition()
            self.interactive.move(i[2])
            new = self.interactive.getPlayerPosition()
            if (cur[0], cur[1]) == (new[0], new[1]):
                self.interactive.move(i[2])
            # print(self.interactive.getPlayerPosition())
        return True
    
    # def updateBS(self, player):
    #     for i in self.newMove((player[0], player[1])):
    #                 if self.interactive.isBreeze() and self.interactive.isStench():
    #                     key = CONVERT['BS']
    #                 elif self.interactive.isBreeze():
    #                     key = CONVERT['B']
    #                 else:
    #                     key = CONVERT['S']
    #         # TODO: change estimate to count the number of B, S, BS
    #                 position = (i[0], i[1])
    #                 if position in self.estimate:
    #                     compare = key ^ self.estimate[position]
    #                     # print(Fore.RED + "Compare", compare)
    #                     if compare == 0 or key == 3:
    #                         continue
    #                     else:
    #                         if self.estimate[position] == 3:
    #                             self.estimate[position] = key
    #                             continue
    #                         else:
    #                             self.safe.append(position)
    #                             self.view[position] = []
    #                             self.estimate[position] = 0
    #                 else:
    #                     self.estimate[position] = key
    
    def findWumpus(self, previous):
        '''find the optimal possible wumpus'''
        visit = [(previous[0], previous[1], None, self.interactive.getScore())]
        self.parent = {}
        self.parent[(previous[0], previous[1])] = None
        while (visit):
            current = visit.pop(0)
            # print("\nConsider", Fore.CYAN + f'{current}')
            if (current[0], current[1]) in self.wumpus:
                break
            for i in self.possibleMove((current[0], current[1])):
                # print(Fore.WHITE + "Check", i, "is in", self.wumpus)
                if (i[0], i[1]) in self.view and (i[0], i[1]) not in self.parent:
                    # print("Repeat this step", Fore.RED + f'{i}')
                    self.parent[(i[0], i[1])] = current
                    visit.append((i[0], i[1], i[2], current[3] - 10))
                if (i[0], i[1]) in self.wumpus:
                    self.parent[(i[0], i[1])] = current
                    current = i
                    self.wumpus.remove((current[0], current[1]))
                    destination = current
                    flag = True
                    # print("Found safe position", Fore.YELLOW + f'{destination}')
                    return current
        if (current[0], current[1]) not in self.wumpus:
            return None
    
    def travelWumpus(self, previous):
        path = []
        current = self.findWumpus(previous)
        if (current == None):
            return False
        # print(Fore.CYAN + "Destination: ", destination)
        while (current):
            path.append(current)
            current = self.parent[(current[0], current[1])]
        wumpus = path.pop(0)
        path = path[::-1]
        path.pop(0)
        # print(Fore.WHITE + "    Path: ", path)
        for i in path:
            # print(Fore.WHITE + "    Move to", i[2])
            cur = self.interactive.getPlayerPosition()
            self.interactive.move(i[2])
            new = self.interactive.getPlayerPosition()
            if (cur[0], cur[1]) == (new[0], new[1]):
                self.interactive.move(i[2])
            # print(self.interactive.getPlayerPosition())
        player = self.interactive.getPlayerPosition()
        if player[2] == wumpus[2]:
            self.interactive.shootArrow()
            self.interactive.move(wumpus[2])
        else:
            self.interactive.move(wumpus[2])
            self.interactive.shootArrow()
            self.interactive.move(wumpus[2])
        # print(Fore.BLUE + "May kill Wumpus at" + Fore.WHITE, wumpus)
        # self.safe.append((wumpus[0], wumpus[1]))
        
        self.updateView((wumpus[0], wumpus[1]))
        return True
    
    def updateView(self, wumpus):
        '''update the view of the map'''
        self.estimate[(wumpus[0], wumpus[1])] = [0, 0]
        for i in self.interactive.connectedRooms(wumpus[0], wumpus[1]):
            # print(Fore.YELLOW + "Check" + Fore.WHITE, i, "is in", self.view)
            if (i[0], i[1]) in self.view:
                self.view[(i[0], i[1])] = self.interactive.getCell(i[0], i[1])
                # print(self.view[(i[0], i[1])])
                if 'S' not in self.view[(i[0], i[1])]:
                    for j in self.newMove((i[0], i[1])):
                        self.estimate[(j[0], j[1])][1] = 0
                        if self.estimate[(j[0], j[1])] == [0, 0]:
                            self.safe.append((j[0], j[1]))
                            self.view[(j[0], j[1])] = []
        # print("Estimate after killing" + Fore.CYAN, wumpus, Fore.WHITE + "is ", self.estimate)
        # self.agentMap() 
        
                        
    
    def updateBS(self, player):
        # estimate = [B, S]
        for i in self.newMove((player[0], player[1])):
                    if self.interactive.isBreeze() and self.interactive.isStench():
                        key = [1, 1]
                    elif self.interactive.isBreeze():
                        key = [1, 0]
                    else:
                        key = [0, 1]
                    # print("key", key, "at", player)
                    position = (i[0], i[1])
                    if position in self.estimate:
                        # print("Estimate", self.estimate[position])
                        compare = ((key[0] > 0) * 2 + (key[1] > 0)) ^ ((self.estimate[position][0] > 0) * 2 + (self.estimate[position][1] > 0))
                        # print(Fore.RED + "Compare", compare)
                        if compare == 0:
                            self.estimate[position] = [self.estimate[position][0] + key[0], self.estimate[position][1] + key[1]]
                        elif key == [1,1]:
                                self.estimate[position] = [(self.estimate[position][0] + key[0]) * (self.estimate[position][0] > 0), (self.estimate[position][1] + key[1]) * (self.estimate[position][1] > 0)]
                        else:
                            if self.estimate[position] == [1, 1]:
                                self.estimate[position] = [self.estimate[position][0] * key[0] + key[0], self.estimate[position][1] * key[1] + key[1]]
                            else:
                                # print(Fore.RED + "Found safe position" + Fore.WHITE, position)
                                self.safe.append(position)
                                self.view[position] = []
                                self.estimate[position] = [0, 0]
                    else:
                        self.estimate[position] = key
        # print(Fore.RED + "Estimate" + Fore.WHITE,self.estimate)
    
    def killWumpus(self):
        # search for possible wumpus in estimate: estimate[1] > 1
        self.wumpus = [i for i in self.estimate if self.estimate[i][1] > 1 and self.estimate[i][0] == 0]
        # print(Fore.RED + "Possible wumpus: " + Fore.WHITE, self.wumpus)
        if not self.wumpus:
            return False
        self.travelWumpus(self.interactive.getPlayerPosition())
        return True    
    def solve(self):
        self.interactive.gameStart() # donot modify this line
        player = self.interactive.getPlayerPosition()
        self.safe = [(player[0], player[1])]
        while not self.interactive.isEnd:

            player = self.interactive.getPlayerPosition()
            # print(Fore.GREEN + "Safe position" + Fore.WHITE, self.safe)
            
            # print(Fore.YELLOW + "\nPlayer is at" + Fore.WHITE, player)
            self.view[(player[0], player[1])] = self.interactive.getCellView()
            if self.interactive.isBreeze() or self.interactive.isStench():
                self.updateBS(player)  
            # print("Estimate position", self.estimate)
            if self.interactive.isNone():
                for i in self.newMove((player[0], player[1])):
                    self.safe.append((i[0], i[1]))
            # print(Fore.CYAN + "Estimate: " + Fore.WHITE, self.estimate)                
            # print(Fore.CYAN + "View: " + Fore.WHITE, self.view)                
                    
            previous = player
            # print(previous)
            # print(self.safe)
            self.safe.remove((previous[0], previous[1]))
            if self.travelNextMove(previous):
                continue
            else:
                # TODO shoot the possible wumbus
                if (self.killWumpus()):
                    # print("Let's go")
                    continue
                print(Fore.GREEN + "\nTry to escape" + Fore.WHITE)
                self.escape()
                self.interactive.isEnd = True
        print(Fore.GREEN + "\n\nWhat i have view: ")
        print(self.view)
        self.agentMap() 
        return self.interactive.getLogs() # donot modify this line