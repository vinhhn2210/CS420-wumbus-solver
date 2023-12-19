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
        self.estimate = {}
        self.door = (self.interactive.size, 0)
        self.safe = []
        

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
        self.findNextMove(player)
    
    def findNextMove(self, previous):
        '''travel to the optimal safe position'''
        visit = [(previous[0], previous[1], None)]
        parent = {}
        parent[(previous[0], previous[1])] = None
        flag = False
        while (visit):
            
            current = visit.pop(0)
            # print("\nConsider", Fore.CYAN + f'{current}')
            if (current[0], current[1]) in self.safe:
                break
            for i in self.possibleMove((current[0], current[1])):
                # print(Fore.WHITE + "Check", i, "is in", self.safe)
                if (i[0], i[1]) in self.view and (i[0], i[1]) not in parent:
                    # print("Repeat this step", Fore.RED + f'{i}')
                    parent[(i[0], i[1])] = current
                    visit.append(i)
                if (i[0], i[1]) in self.safe:
                    parent[(i[0], i[1])] = current
                    current = i
                    destination = current
                    flag = True
                    # print("Found safe position", Fore.YELLOW + f'{destination}')
                    break
            if flag:
                break
        if (current[0], current[1]) not in self.safe:
            return False
        path = []
        # print(Fore.CYAN + "Destination: ", destination)
        while (current):
            path.append(current)
            current = parent[(current[0], current[1])]
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
    
    def solve(self):
        self.interactive.gameStart() # donot modify this line
        player = self.interactive.getPlayerPosition()
        self.safe = [(player[0], player[1])]
        while not self.interactive.isEnd:

            player = self.interactive.getPlayerPosition()
            
            # print("Player is at", player)
            self.view[(player[0], player[1])] = self.interactive.getCellView()
            
            if self.interactive.isBreeze() or self.interactive.isStench():
                for i in self.newMove((player[0], player[1])):
                    if self.interactive.isBreeze() and self.interactive.isStench():
                        key = CONVERT['BS']
                    elif self.interactive.isBreeze():
                        key = CONVERT['B']
                    else:
                        key = CONVERT['S']
            # TODO: change estimate to count the number of B, S, BS
                    position = (i[0], i[1])
                    if position in self.estimate:
                        compare = key ^ self.estimate[position]
                        # print(Fore.RED + "Compare", compare)
                        if compare == 0 or key == 3:
                            continue
                        else:
                            if self.estimate[position] == 3:
                                self.estimate[position] = key
                                continue
                            else:
                                self.safe.append(position)
                                self.view[position] = []
                                self.estimate[position] = 0
                    else:
                        self.estimate[position] = key
            if self.interactive.isNone():
                for i in self.newMove((player[0], player[1])):
                    self.safe.append((i[0], i[1]))
            # print(Fore.CYAN + "Estimate: " + Fore.WHITE, self.estimate)                
                    
            previous = player
            # print(previous)
            # print(self.safe)
            self.safe.remove((previous[0], previous[1]))
            if self.findNextMove(previous):
                continue
            else:
                # print(Fore.GREEN + "\nTry to escape" + Fore.WHITE)
                self.escape()
                self.interactive.isEnd = True
        print(Fore.GREEN + "\n\nWhat i have view: ")
        print(self.view)
        self.agentMap() 
        return self.interactive.getLogs() # donot modify this line