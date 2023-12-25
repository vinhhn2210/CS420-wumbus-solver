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

B = Fore.BLUE + "B" + Fore.WHITE
S = Fore.RED + "S" + Fore.WHITE
M = Fore.GREEN + "M" + Fore.WHITE
W = Fore.MAGENTA + "~W" + Fore.WHITE
P = Fore.CYAN + "~P" + Fore.WHITE

class Nerd_KB:
    def __init__(self):
        self.knowledgeBase = {}
    def initial(self, facts, position):
        self.knowledgeBase[position] =  f'{facts}({position[0]}, {position[1]})'
    def add_conjunct(self, facts, position, value):
        self.knowledgeBase[position] += f' & {facts}({value[0]}, {value[1]})'
    def add_entail(self, facts, position, value):
        # check if > in the string knowledgeBase[position]
        if '>' in self.knowledgeBase[position]:
            self.knowledgeBase[position] += f' {facts}({value[0]}, {value[1]}) & '
        else:
            self.knowledgeBase[position] += f' => ({facts}({value[0]}, {value[1]}) & '
    def close_entail(self, position):
        if self.knowledgeBase[position][-2:] == "& ":
            self.knowledgeBase[position] = self.knowledgeBase[position][:-3] + ")"
        else:
            self.knowledgeBase[position] += ')'
    
    def add(self, position, other_position):
        if position not in self.knowledgeBase:
            self.knowledgeBase[position] = f'{self.knowledgeBase[other_position]}'
        else:
            self.knowledgeBase[position] += f' & {self.knowledgeBase[other_position]}'
        
    def display(self):
        for i in self.knowledgeBase:
            print(self.knowledgeBase[i])

class Nerd:
    def __init__(self, mapState):
        self.interactive = InteractiveGame()
        self.interactive.loadMap(mapState)
        self.view = {}
        self.estimate = {} # self.estimate[(i, j)] = 1: B, 2: S, 3: BS
        self.door = (0, 0, 'UP')
        # self.door = (mapState.nSize - 1, 0, 'DOWN')
        self.safe = []
        self.parent = {}
        self.knowledgeBase = Nerd_KB()
        

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
        k = [i for i in self.possibleMove(playerPos) if (i[0], i[1]) not in self.view]
        return k

    
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
        # flip vertically
        temp = temp[::-1]
        MapState('agentMap', nSize, temp).printMap()
        
        
    def escape(self):
        player = self.interactive.getPlayerPosition()
        self.safe = [(self.door[0], self.door[1])]
        if self.travelNextMove(player):
            self.interactive.gameEnd()
            # nextDoor = self.interactive.getPlayerPosition()
            # self.interactive.move(self.door[2])
            # player = self.interactive.getPlayerPosition()
            # if (player[0], player[1]) == (nextDoor[0], nextDoor[1]):
            #     self.interactive.move(self.door[2])
            pass
        else:
            print(Fore.RED + "Cannot escape" + Fore.WHITE)
            self.interactive.gameEnd()
    
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
            # print("No more move to go")
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
        # print("Travel to kill wumpus")
        path = []
        current = self.findWumpus(previous)
        if (current == None):
            # print("No more wumpus to kill")
            return False
        while (current):
            path.append(current)
            current = self.parent[(current[0], current[1])]
        wumpus = path.pop(0)
        path = path[::-1]
        path.pop(0)
        # print(Fore.WHITE + "    Path: ", path)
        for i in path:
            self.interactive.moveImmediately(i[2])
        player = self.interactive.getPlayerPosition()
        if player[2] == self.interactive.directions[wumpus[2]]:
            self.interactive.shootArrow()
            self.interactive.move(wumpus[2])
        else:
            self.interactive.move(wumpus[2])
            self.interactive.shootArrow()
            self.interactive.move(wumpus[2])
        player = self.interactive.getPlayerPosition()
        self.knowledgeBase.initial(W, (wumpus[0], wumpus[1]))
        # print(Fore.BLUE + "May kill Wumpus at" + Fore.WHITE, wumpus)
        self.safe.append((wumpus[0], wumpus[1]))
        
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
                            self.view[(j[0], j[1])] = []
                            if (j[0], j[1]) not in self.safe:
                                self.safe.append((j[0], j[1]))
        # print("Estimate after killing" + Fore.CYAN, wumpus, Fore.WHITE + "is ", self.estimate)
        # self.agentMap() 
        
                        
    
    def updateBS(self, player):
        # estimate = [B, S]
        if self.interactive.isBreeze() and self.interactive.isStench():
            self.knowledgeBase.initial(B, (player[0], player[1]))
            self.knowledgeBase.add_conjunct(S, (player[0], player[1]), (player[0], player[1]))
            key = [1, 1]
        elif self.interactive.isBreeze():
            self.knowledgeBase.initial(B, (player[0], player[1]))
            key = [1, 0]
        else:
            self.knowledgeBase.initial(S, (player[0], player[1]))
            key = [0, 1]
                    # print("key", key, "at", player)
        for i in self.newMove((player[0], player[1])):
                    position = (i[0], i[1])
                    if position in self.estimate:
                        # print("Estimate", self.estimate[position])
                        compare = ((key[0] > 0) * 2 + (key[1] > 0)) ^ ((self.estimate[position][0] > 0) * 2 + (self.estimate[position][1] > 0))
                        # print(Fore.RED + "Compare", compare)
                        if compare == 0:
                            self.estimate[position] = [self.estimate[position][0] + key[0], self.estimate[position][1] + key[1]]
                            self.knowledgeBase.add((i[0], i[1]), (player[0], player[1]))
                        elif key == [1,1]:
                            if self.estimate[position] == [0, 1]:
                                self.knowledgeBase.add_conjunct(S, (i[0], i[1]), (player[0], player[1]))
                            else:
                                self.knowledgeBase.add_conjunct(B, (i[0], i[1]), (player[0], player[1]))
                            self.estimate[position] = [(self.estimate[position][0] + key[0]) * (self.estimate[position][0] > 0), (self.estimate[position][1] + key[1]) * (self.estimate[position][1] > 0)]
                        else:
                            if self.estimate[position] == [0, 1]:
                                self.knowledgeBase.add_conjunct(S, (i[0], i[1]), (player[0], player[1]))
                            else:
                                self.knowledgeBase.add_conjunct(B, (i[0], i[1]), (player[0], player[1]))
                            if self.estimate[position] == [1, 1]:
                                self.estimate[position] = [self.estimate[position][0] * key[0] + key[0], self.estimate[position][1] * key[1] + key[1]]
                            else:
                                # print(Fore.RED + "Found safe position" + Fore.WHITE, position)
                                self.knowledgeBase.add((i[0], i[1]), (player[0], player[1]))
                                self.knowledgeBase.add_entail(M, (i[0], i[1]), (i[0], i[1]))
                                self.knowledgeBase.close_entail((i[0], i[1]))
                                self.safe.append(position)
                                self.view[position] = []
                                self.estimate[position] = [0, 0]
                                # print("----------------------------------")
                                # self.displayKB()
                    else:
                        self.knowledgeBase.add((i[0], i[1]), (player[0], player[1]))
                        self.estimate[position] = key
        # print(Fore.RED + "Estimate" + Fore.WHITE,self.estimate)
    
    def killWumpus(self):
        # search for possible wumpus in estimate: estimate[1] > 1
        max_stench = max([self.estimate[i][1] for i in self.estimate])
        if max_stench == 0:
            return False
        self.wumpus = [i for i in self.estimate if self.estimate[i][1] == max_stench]
        # print(Fore.RED + "Possible wumpus: " + Fore.WHITE, self.wumpus)
        self.travelWumpus(self.interactive.getPlayerPosition())
        return True    
    def solve(self):
        self.interactive.gameStart() # donot modify this line
        player = self.interactive.getPlayerPosition()
        self.safe = [(player[0], player[1])]
        
        
        while not self.interactive.isEnd:
            self.displayKB()
            self.interactive.debug()
            player = self.interactive.getPlayerPosition()
            
            # print(Fore.YELLOW + "\nPlayer is at" + Fore.WHITE, player)
            self.view[(player[0], player[1])] = self.interactive.getCellView()
            if self.interactive.isBreeze() or self.interactive.isStench():
                self.updateBS(player)  
            # print("Estimate position", self.estimate)
            if self.interactive.isNone():
                self.knowledgeBase.initial(M, (player[0], player[1]))
                for i in self.newMove((player[0], player[1])):
                    if (i[0], i[1]) not in self.safe:
                        self.safe.append((i[0], i[1]))
                        self.knowledgeBase.add_entail(M, (player[0], player[1]), (i[0], i[1]))
                self.knowledgeBase.close_entail((player[0], player[1]))
            
            # print(Fore.CYAN + "Estimate: " + Fore.WHITE, self.estimate)                
            # print(Fore.CYAN + "View: " + Fore.WHITE, self.view)                
                    
            # print(Fore.WHITE + "Safe position" + Fore.WHITE, self.safe)
            previous = player
            # print(previous)
            self.safe.remove((previous[0], previous[1]))
            # print(Fore.GREEN + "Safe position" + Fore.WHITE, self.safe)
            if self.travelNextMove(previous):
                # print("Move to safe position")
                continue
            else:
                # print("Cannot move to safe position")
                # TODO shoot the possible wumbus
                if (self.killWumpus()):
                    # print("I may kill a wumpus")
                    continue
                print(Fore.GREEN + "\nTry to escape" + Fore.WHITE)
                self.escape()
                self.interactive.isEnd = True
        # print(Fore.GREEN + "\n\nWhat i have view: ")
        # print(self.view)
        self.agentMap() 
        self.interactive.gameEnd()
        return self.interactive.getLogs() # donot modify this line
    
    def displayKB(self):
        print(Fore.YELLOW + "KB: " + Fore.WHITE)
        self.knowledgeBase.display()