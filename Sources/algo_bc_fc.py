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

B = Fore.BLUE + "B" + Fore.WHITE
S = Fore.RED + "S" + Fore.WHITE
M = Fore.GREEN + "M" + Fore.WHITE
W = Fore.MAGENTA + "~W" + Fore.WHITE
P = Fore.CYAN + "~P" + Fore.WHITE

class BC_FC_KB:
    def __init__(self, n):
        self.m = [[0 for i in range(n)] for j in range(n)]
        self.s = [[0 for i in range(n)] for j in range(n)]
        self.b = [[0 for i in range(n)] for j in range(n)]
        self.p = [[0 for i in range(n)] for j in range(n)]
        self.w = {}
        self.n = n
        self.rule = [
            "self.M(i + 1, j) => self.M(i, j)",
            "self.M(i - 1, j) => self.M(i, j)",
            "self.M(i, j + 1) => self.M(i, j)",
            "self.M(i, j - 1) => self.M(i, j)",
            
            "self.B(i + 1, j) AND self.S(i - 1, j) AND self.notB(i + 1, j) => self.M(i, j)",
            "self.B(i + 1, j) AND self.S(i, j + 1) AND self.notB(i + 1, j) => self.M(i, j)",
            "self.B(i + 1, j) AND self.S(i, j - 1) AND self.notB(i + 1, j) => self.M(i, j)",
            
            "self.B(i - 1, j) AND self.S(i + 1, j) AND self.notB(i - 1, j) => self.M(i, j)",
            "self.B(i - 1, j) AND self.S(i, j + 1) AND self.notB(i - 1, j) => self.M(i, j)",
            "self.B(i - 1, j) AND self.S(i, j - 1) AND self.notB(i - 1, j) => self.M(i, j)",
            
            "self.B(i, j + 1) AND self.S(i, j - 1) AND self.notB(i, j + 1) => self.M(i, j)",
            "self.B(i, j + 1) AND self.S(i + 1, j) AND self.notB(i, j + 1) => self.M(i, j)",
            "self.B(i, j + 1) AND self.S(i - 1, j) AND self.notB(i, j + 1) => self.M(i, j)",
            
            "self.B(i, j - 1) AND self.S(i, j + 1) AND self.notB(i, j - 1) => self.M(i, j)",
            "self.B(i, j - 1) AND self.S(i + 1, j) AND self.notB(i, j - 1) => self.M(i, j)",
            "self.B(i, j - 1) AND self.S(i - 1, j) AND self.notB(i, j - 1) => self.M(i, j)",
        ]
        self.pit_rule = [
            "self.B(i, j) AND self.notP(i - 1, j) AND self.notP(i, j + 1) AND self.notP(i, j - 1) => self.P(i + 1, j)",
            "self.B(i, j) AND self.notP(i + 1, j) AND self.notP(i, j + 1) AND self.notP(i, j - 1) => self.P(i - 1, j)",
            "self.B(i, j) AND self.notP(i + 1, j) AND self.notP(i - 1, j) AND self.notP(i, j - 1) => self.P(i, j + 1)",
            "self.B(i, j) AND self.notP(i + 1, j) AND self.notP(i - 1, j) AND self.notP(i, j + 1) => self.P(i, j - 1)",
        ]
        
        # optimistic positive
        self.wumpus_rule = [
            # "self.S(i, j) AND self.notB(i, j) AND self.notB(i + 2, j) AND self.notB(i + 1, j - 1) AND self.notB(i + 1, j + 1) => self.W(i + 1, j)",
            # "self.S(i, j) AND self.notB(i, j) AND self.notB(i - 2, j) AND self.notB(i - 1, j + 1) AND self.notB(i - 1, j - 1) => self.W(i - 1, j)",
            # "self.S(i, j) AND self.notB(i, j) AND self.notB(i, j + 2) AND self.notB(i + 1, j + 1) AND self.notB(i - 1, j + 1) => self.W(i, j + 1)",
            # "self.S(i, j) AND self.notB(i, j) AND self.notB(i, j - 2) AND self.notB(i + 1, j - 1) AND self.notB(i - 1, j - 1) => self.W(i, j - 1)",
            "self.S(i, j) AND self.notB(i, j) => self.W(i + 1, j)",
            "self.S(i, j) AND self.notB(i, j) => self.W(i - 1, j)",
            "self.S(i, j) AND self.notB(i, j) => self.W(i, j + 1)",
            "self.S(i, j) AND self.notB(i, j) => self.W(i, j - 1)",
            
            "self.S(i, j) AND self.PM(i + 1, j) AND self.PM(i - 1, j) AND self.PM(i, j + 1) => self.W(i, j - 1)",
            "self.S(i, j) AND self.PM(i + 1, j) AND self.PM(i - 1, j) AND self.PM(i, j - 1) => self.W(i, j + 1)",
            "self.S(i, j) AND self.PM(i + 1, j) AND self.PM(i, j + 1) AND self.PM(i, j - 1) => self.W(i - 1, j)",
            "self.S(i, j) AND self.PM(i - 1, j) AND self.PM(i, j + 1) AND self.PM(i, j - 1) => self.W(i + 1, j)",
        ]
        self.knowledgeBase = []
        
    def bc_function(self, string, i, j):
        '''example: self.M(i + 1, j) => self.M(i, j)
        reduct to self.M(i + 1, j)'''
        clause = string[0:16]
        if "AND" in string:
            sub_clause1 = string[21:37]
            sub_clause2 = string[42:61]
            return eval(clause) and eval(sub_clause1) and eval(sub_clause2)
        return eval(clause)
    
    def print(self):
        print(f"Record of {M}")
        for i in range(self.n):
            for j in range(self.n):
                if self.m[i][j] == 1:
                    print(M, end=" ")
                else:
                    print("x", end=" ")
            print()
        print(f"Record of {B}")
        for i in range(self.n):
            for j in range(self.n):
                if self.b[i][j] == 1:
                    print(B, end=" ")
                else:
                    print("x", end=" ")
            print()
        print(f"Record of {S}")
        for i in range(self.n):
            for j in range(self.n):
                if self.s[i][j] == 1:
                    print(S, end=" ")
                else:
                    print("x", end=" ")
            print()
            
    def fc_function(self, string, i, j):
        # clause = [string[0:12], string[17:32], string[37:56], string[61:84], string[89:112]]
        # pair =  eval(string[122:132])
        if (len(string) == 52):
            clause = [string[0:12], string[17:32]]
            pair = eval(string[42:52])
            for fol in clause:
                if eval(fol) == False:
                    return False
            return self.updateWumpus(pair[0], pair[1])
        return False
            
    def M(self, i, j):
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            return False
        return self.m[i][j]
    
    def B(self, i, j):
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            return False
        return self.b[i][j]
    
    def P(self, i, j):
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            return False
        return self.p[i][j]
    
    def notP(self, i, j):
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            return True
        return self.p[i][j] == 0
    
    def S(self, i, j):
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            return False
        return self.s[i][j]
    
    def notB(self, i, j):
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            return True
        return self.b[i][j] == 0
    
    def PM(self, i, j):
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            return False
        return self.m[i][j] == 1 or self.p[i][j] == 1
    
    def updateWumpus(self, i, j):
        if i < 0 or i >= self.n or j < 0 or j >= self.n or self.m[i][j] == 1 or self.b[i][j] == 1 or self.s[i][j] == 1:
            return False
        self.w[(i, j)] = 1
        return True
    
    def backward_chaining(self, i, j):
        # print("Backward chaining with", i, j, "")
        # self.print()
        for rule in self.rule:
            if self.bc_function(rule, i, j):
                self.temp_rule = "BC: " + rule + ", {i/" + str(i) + ", j/" + str(j) + "}"
                return True
        return False
    
    def forward_chaining(self, i, j):
        for rule in self.wumpus_rule:
            if self.fc_function(rule, i, j):
                self.temp_rule = "FC: " + rule + ", {i/" + str(i) + ", j/" + str(j) + "}"
                return True
        return False
    
        
    def display(self):
        for i in self.knowledgeBase:
            print(i)

class BackAndForwardChaining:
    def __init__(self, mapState):
        self.interactive = InteractiveGame()
        self.interactive.loadMap(mapState)
        self.door = (0, 0, 'UP')
        self.n = mapState.nSize
        # self.door = (mapState.nSize - 1, 0, 'DOWN')
        self.safe = []
        self.knowledgeBase = BC_FC_KB(mapState.nSize)
        self.travel = [[0 for i in range(mapState.nSize)] for j in range(mapState.nSize)]
        self.stench = []
        
    def escape(self):
        self.safe = [(self.door[0], self.door[1])]
        if self.travelNextMove():
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
    
    def connectedRooms(self, x, y):
        '''return the list of connected rooms'''
        connected = []
        if x - 1 >= 0:
            connected.append((x - 1, y, 'UP'))
        if x + 1 < self.n:
            connected.append((x + 1, y, 'DOWN'))
        if y - 1 >= 0:
            connected.append((x, y - 1, 'LEFT'))
        if y + 1 < self.n:
            connected.append((x, y + 1, 'RIGHT'))
        return connected
    
    def findNextMove(self):
        '''find the optimal safe position'''
        # print("Find next move")
        current = self.interactive.getPlayerPosition()
        visit = [(current[0], current[1])]
        self.parent = {}
        self.parent[(current[0], current[1])] = None
        while (visit):
            current = visit.pop(0)
            # print("Visit: ", current)
            if current in self.safe:
                self.safe.remove(current)
                return (current[0], current[1])
            for i in self.connectedRooms(current[0], current[1]):
                # print("Checking", i)
                if (i[0], i[1]) in self.safe:
                    # print("Found safe position", i)
                    self.parent[(i[0], i[1])] = (i[2], current)
                    self.safe.remove((i[0], i[1]))
                    return (i[0], i[1])
                if (i[0], i[1]) not in self.parent and self.travel[i[0]][i[1]] == 1:
                    # print("Step again")
                    self.parent[(i[0], i[1])] = (i[2], current)
                    visit.append((i[0], i[1]))
        return None
        
    def travelNextMove(self):
        path = []
        current = self.findNextMove()
        # print("Next move: ", current)
        if (current == None):
            # print("No more move to go")
            return False
        # print(Fore.CYAN + "Destination: ", destination)
        while (self.parent[current]):
            move, current = self.parent[current]
            path.append(move)
        path = path[::-1]
        # print(Fore.WHITE + "    Path: ", path)
        for i in path:
            # print(Fore.YELLOW + "    Move to" + Fore.WHITE, i)
            self.interactive.moveImmediately(i)
            # self.interactive.debug()
            
            # print(self.interactive.getPlayerPosition())
        return True
    
    def findWumpus(self):
        '''find the optimal possible wumpus'''
        # print("Find next wumpus")
        current = self.interactive.getPlayerPosition()
        visit = [(current[0], current[1])]
        self.parent = {}
        self.parent[(current[0], current[1])] = None
        while (visit):
            current = visit.pop(0)
            # print("Visit: ", current)
            if current in self.knowledgeBase.w:
                return (current[0], current[1])
            for i in self.connectedRooms(current[0], current[1]):
                # print("Checking", i)
                if (i[0], i[1]) in self.knowledgeBase.w:
                    # print("Found wumpus", i)
                    self.parent[(i[0], i[1])] = (i[2], current)
                    return (i[0], i[1])
                if (i[0], i[1]) not in self.parent and self.travel[i[0]][i[1]] == 1:
                    # print("Step again")
                    self.parent[(i[0], i[1])] = (i[2], current)
                    visit.append((i[0], i[1]))
        return None
    
    def travelWumpus(self):
        # print("Travel to kill wumpus")
        path = []
        current = self.findWumpus()
        if (current == None):
            print("No more wumpus to kill")
            return False
        while (self.parent[current]):
            move, current = self.parent[current]
            path.append(move)
        wumpus = path.pop(0)
        path = path[::-1]
        # print(Fore.WHITE + "    Path: ", path)
        for i in path:
            self.interactive.moveImmediately(i)
        player = self.interactive.getPlayerPosition()
        if player[2] == self.interactive.directions[wumpus]:
            self.interactive.shootArrow()
            self.interactive.move(wumpus)
        else:
            self.interactive.move(wumpus)
            self.interactive.shootArrow()
            self.interactive.move(wumpus)
        player = self.interactive.getPlayerPosition()
        # print(Fore.BLUE + "May kill Wumpus at" + Fore.WHITE, wumpus)
        self.updateView((player[0], player[1]))
        return True
    
    def updateView(self, die_wumpus):
        '''update the view of the map'''
        # print("Updating view")
        for i in self.interactive.connectedRooms(die_wumpus[0], die_wumpus[1]):
            if self.travel[i[0]][i[1]] == 1:
                cell_check = self.interactive.getCell(i[0], i[1])
                # print("Checking", i, cell_check)
                if 'S' not in cell_check and self.knowledgeBase.s[i[0]][i[1]] == 1:
                    self.stench.remove((i[0], i[1]))
                    self.knowledgeBase.s[i[0]][i[1]] = 0
                    if cell_check == '-':
                        self.knowledgeBase.m[i[0]][i[1]] = 1
                    for j in self.interactive.connectedRooms(i[0], i[1]):
                        # print("Checking after updating", j)
                        if self.travel[j[0]][j[1]] == 0 and( j[0] != die_wumpus[0] or j[1] != die_wumpus[1]) and (j[0], j[1]) not in self.safe:
                            if self.knowledgeBase.backward_chaining(j[0], j[1]):
                                # print("Found safe position", j)
                                self.safe.append((j[0], j[1]))
                                self.knowledgeBase.knowledgeBase.append(self.knowledgeBase.temp_rule)
                                self.interactive.appendKBLog(self.knowledgeBase.temp_rule)
        # print("Estimate after killing" + Fore.CYAN, wumpus, Fore.WHITE + "is ", self.estimate)
        # self.agentMap() 
    
    
    def killWumpus(self):
        self.knowledgeBase.w = {}
        for s in self.stench:
            self.knowledgeBase.forward_chaining(s[0], s[1])
        # search for possible wumpus in estimate: estimate[1] > 1
        if self.knowledgeBase.w is {}:
            return False
            
        # print(Fore.RED + "Possible wumpus: " + Fore.WHITE, self.knowledgeBase.w)
        if self.travelWumpus() is False:
            return False
        self.interactive.appendKBLog(self.knowledgeBase.temp_rule)
        return True    
    def solve(self):
        self.interactive.gameStart() # donot modify this line
        # player = self.interactive.getPlayerPosition()
        # self.safe = [(player[0], player[1])]
        
        
        while not self.interactive.isEnd:
            # debug and display functions
            # self.displayKB()
            # self.interactive.debug()
            
            player = self.interactive.getPlayerPosition()
            position = (player[0], player[1])
            
            # print("Updating knowledge base")
            
            # update knowledge base
            if self.interactive.isNone():
                self.knowledgeBase.m[position[0]][position[1]] = 1
            if self.interactive.isBreeze():
                self.knowledgeBase.b[position[0]][position[1]] = 1
            if self.interactive.isStench():
                self.knowledgeBase.s[position[0]][position[1]] = 1
                self.stench.append((position[0], position[1]))
                # forward chaining
            self.travel[position[0]][position[1]] = 1
            
            # print("Backward chaining")
            
            t = self.interactive.connectedRooms(position[0], position[1])
            for i in t:
                # print("Checking", i)
                if self.travel[i[0]][i[1]] == 0:
                    if self.knowledgeBase.backward_chaining(i[0], i[1]):
                        if (i[0], i[1]) not in self.safe:
                            self.safe.append((i[0], i[1]))
                            self.knowledgeBase.knowledgeBase.append(self.knowledgeBase.temp_rule)
                            self.interactive.appendKBLog(self.knowledgeBase.temp_rule)
            # print(Fore.CYAN + "Safe position: " + Fore.WHITE, self.safe)
            if self.travelNextMove():
                
                continue
            else:
                if (self.killWumpus()):
                    continue
                print(Fore.GREEN + "\nTry to escape" + Fore.WHITE)
                self.escape()
                self.interactive.isEnd = True
        self.interactive.gameEnd()
        self.interactive.debug()
        return self.interactive.getLogs() # donot modify this line
    
    def displayKB(self):
        print(Fore.YELLOW + "KB: " + Fore.WHITE)
        self.knowledgeBase.display()