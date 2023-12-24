import copy
from queue import Queue
from interactive import *

class KnowledgeBase:
    def __init__(self):
        self.clauses = []

    def addClause(self, clause):
        for i in self.clauses:
            if i == clause:
                return
        self.clauses.append(clause)

    def removeClause(self, clause):
        self.clauses = [elem for elem in self.clauses if elem != clause]

    def getClause(self):
        return copy.deepcopy(self.clauses)

    def getClauseDetail(self, row, col):
        res = []

        for i in self.clauses:
            curDict = {}
            isExist = False
            for j in i:
                val, X, Y = j.split('_')
                X = int(X)
                Y = int(Y)
                if X == row and Y == col:
                    isExist = True
                curDict[j] = i[j]

            if isExist == True:
                res.append(curDict)

        return res

class DPLLAlgo:
    def __init__(self, mapState):
        self.interactive = InteractiveGame()
        self.interactive.loadMap(mapState)

        self.mapSize = 4

        self.KB = KnowledgeBase()

        self.roomDict = {}

        # -------------------Set up intitial state for game-----------------------
        for row in range(0, self.mapSize):
            for col in range(0, self.mapSize):         
                # Add Stench-Wumpus bijection Clauses
                curNextRoom = self.getAdjacentRoomList(row, col)
                curCNFDict = {f'S_{row}_{col}': -1}
                for X, Y in curNextRoom:
                    curCNF = {}
                    curCNF[f'W_{X}_{Y}'] = -1
                    curCNF[f'S_{row}_{col}'] = 1
                    self.KB.addClause(curCNF)
                    curCNFDict[f'W_{X}_{Y}'] = 1
                self.KB.addClause(curCNFDict)

                # Add Breeze-Pit bijection Clauses
                curCNFDict = {f'B_{row}_{col}': -1}
                for X, Y in curNextRoom:
                    curCNF = {}
                    curCNF[f'P_{X}_{Y}'] = -1
                    curCNF[f'B_{row}_{col}'] = 1
                    self.KB.addClause(curCNF)
                    curCNFDict[f'P_{X}_{Y}'] = 1
                self.KB.addClause(curCNFDict)

    def addClauseToKB(self, literal, val):
        curClause = {literal: val}
        if self.roomDict.get(literal) == None:
            self.roomDict[literal] = val
            self.KB.addClause(curClause)

    def removeClauseFromKB(self, literal, val):
        if self.roomDict.get(literal) != None:
            self.roomDict.pop(literal)
            self.KB.removeClause({literal: 1})

    def getAdjacentRoomList(self, X, Y):
        NEXTDIR = ((0, -1), (0, 1), (-1, 0), (1, 0))
        adjacentRooms = []

        for i in range(4):
            nX = X + NEXTDIR[i][0]
            nY = Y + NEXTDIR[i][1]

            if nX < 0 or nX >= self.mapSize or nY < 0 or nY >= self.mapSize:
                continue

            adjacentRooms.append((nX, nY))

        return adjacentRooms

    def FindPureSymbol(self, clauses, symbols):
        for symbol in symbols:
            positive = 0
            negative = 0
            for clause in clauses:
                if symbol in clause:
                    if clause[symbol] == 1:
                        positive = positive + 1
                    else:
                        negative = negative + 1
            if negative == 0:
                return symbol, 1
            elif positive == 0:
                return symbol, -1
        return -1, 0

    def FindUnitClause(self, clauses):
        for clause in clauses:
            if len(clause)==1:
                for symbol in clause:
                    return symbol, clause[symbol]
        return -1, 0

    def selectSymbol(self, clauses, symbols):
        count = {}
        positive = {}
        negative = {}
        for clause in clauses:
            for literal in clause:
                if literal not in count:
                    count[literal] = 0
                    positive[literal] = 0
                    negative[literal] = 0

                count[literal]= count[literal] + 1
                if clause[literal] == 1:
                    positive[literal] = positive[literal] + 1
                else:
                    negative[literal] = negative[literal] + 1
        
        maxLiteral = list(symbols.keys())[0]
        maxCount = 0
        for literal in count:
            if count[literal] > maxCount:
                maxLiteral = literal
                maxCount = count[literal]

        if positive[maxLiteral] > negative[maxLiteral]:
            return maxLiteral, 1
        return maxLiteral, -1

    def DPLL(self, clauses, symbols, model):
        removeClauses = []
        for clause in clauses:
            valueUnknown = True
            deleteLiterals = []
            for literal in clause.keys():
                if literal in model.keys():
                    if model[literal] == clause[literal]: #clause is true
                        removeClauses.append(clause)
                        valueUnknown = False
                        break
                    else:
                        deleteLiterals.append(literal)
            
            for literal in deleteLiterals:
                del clause[literal]
            if valueUnknown == True and not bool(clause): #clause is false
                return False

        clauses = [x for x in clauses if x not in removeClauses]

        if len(clauses) == 0: # all clauses are true
            return True

        pureSymbol, value = self.FindPureSymbol(clauses, symbols)
        if value != 0:
            del symbols[pureSymbol]
            model[pureSymbol] = value
            return self.DPLL(clauses, symbols, model)
        
        unitSymbol, value = self.FindUnitClause(clauses)
        if value != 0:
            del symbols[unitSymbol]
            model[unitSymbol] = value
            return self.DPLL(clauses, symbols, model)

        symbol, value = self.selectSymbol(clauses, symbols)
        del symbols[symbol]
        model[symbol] = value

        if self.DPLL(copy.deepcopy(clauses), copy.deepcopy(symbols), copy.deepcopy(model)):
            return True
        
        model[symbol] = -value
        return DPLL(clauses, symbols, model)

    def DPLLSatisfiable(self, clauses):
        symbols = {}
        for clause in clauses:
            for literal in clause:
                symbols[literal] = True
        
        model = {}
        return self.DPLL(clauses, symbols, model)

    def moveToNextStep(self, start, visited, newRooms):
        queue = []
        queue.append(start)

        dist = {}
        pre = {}
        dist[start] = 0

        while queue:
            curRoom = queue.pop(0)
            nextRooms = self.getAdjacentRoomList(curRoom[0], curRoom[1])

            for i in nextRooms:
                X, Y = i

                if visited.get((X, Y)) == True or newRooms.get((X, Y)) == True:
                    if dist.get((X, Y)) == None:
                        dist[(X, Y)] = dist[curRoom] + 1
                        pre[(X, Y)] = curRoom
                        queue.append((X, Y))

        resRoom = None
        for i in newRooms:
            if dist.get(i) != None:
                if resRoom == None or dist[resRoom] > dist[i]:
                    resRoom = i

        DIR = ('UP', 'DOWN', 'LEFT', 'RIGHT')
        DIR_VAL = ((-1, 0), (1, 0), (0, -1), (0, 1))

        path = []
        while resRoom != None:
            if pre.get(resRoom) != None:
                preRoom = pre[resRoom]

                for i in range(4):
                    if DIR_VAL[i][0] == resRoom[0] - preRoom[0] and DIR_VAL[i][1] == resRoom[1] - preRoom[1]:
                        path.append(DIR[i])
                        break

            resRoom = pre.get(resRoom)

        path.reverse()
        for i in path:
            self.interactive.moveImmediately(i)

        print('Path: ', path)

    def findWumpusToShoot(self, start, visited, wumpusRooms):
        queue = []
        queue.append(start)

        dist = {}
        pre = {}
        dist[start] = 0

        while queue:
            curRoom = queue.pop(0)
            nextRooms = self.getAdjacentRoomList(curRoom[0], curRoom[1])

            for i in nextRooms:
                X, Y = i

                if visited.get((X, Y)) == True or wumpusRooms.get((X, Y)) == True:
                    if dist.get((X, Y)) == None:
                        dist[(X, Y)] = dist[curRoom] + 1
                        pre[(X, Y)] = curRoom
                        queue.append((X, Y))

        resRoom = None
        for i in wumpusRooms:
            if dist.get(i) != None:
                if resRoom == None or dist[resRoom] > dist[i]:
                    resRoom = i

        DIR = ('UP', 'DOWN', 'LEFT', 'RIGHT')
        DIR_VAL = ((-1, 0), (1, 0), (0, -1), (0, 1))

        path = []
        while resRoom != None:
            if pre.get(resRoom) != None:
                preRoom = pre[resRoom]

                for i in range(4):
                    if DIR_VAL[i][0] == resRoom[0] - preRoom[0] and DIR_VAL[i][1] == resRoom[1] - preRoom[1]:
                        path.append(DIR[i])
                        break

            resRoom = pre.get(resRoom)

        if len(path) == 0:
            return False

        path.reverse()
        for i in range(len(path) - 1):
            self.interactive.moveImmediately(path[i])

        self.interactive.changeDirection(path[len(path) - 1])  
        isShootWumpusSucessful = self.interactive.shootArrow()   

        if isShootWumpusSucessful == True:
            curPos = self.interactive.getPlayerPosition()
            newPos = [curPos[0], curPos[1]]

            for i in range(4):
                if DIR[i] == path[len(path) - 1]:
                    newPos[0] += DIR_VAL[i][0]
                    newPos[1] += DIR_VAL[i][1]
                    break

            # Remove Wumpus in current position
            wumpusLiteral = f'W_{newPos[0]}_{newPos[1]}'
            self.removeClauseFromKB(wumpusLiteral, 1)

            # Remove Stench in adjacent room
            adjacentRooms = self.getAdjacentRoomList(newPos[0], newPos[1])
            for room in adjacentRooms:
                stenchLiteral = f'S_{room[0]}_{room[1]}'
                self.removeClauseFromKB(stenchLiteral, 1)

            # Add No Wumpus at current position after shooting
            wumpusLiteral = f'W_{newPos[0]}_{newPos[1]}'
            self.addClauseToKB(wumpusLiteral, -1)

        print('Path To Kill Wumpus: ', path)
        print('######## Shoot Wumpus Successful')

        return True

    def exitWumpusWorld(self):
        visited = {}

        while not self.interactive.isEnd:
            curAgentState = self.interactive.getPlayerPosition()
            curPos = (curAgentState[0], curAgentState[1])

            visited[curPos] = True

            # Add no Wumpus on current room
            wumpusLiteral = f'W_{curPos[0]}_{curPos[1]}'
            self.addClauseToKB(wumpusLiteral, -1)
            # Add no Pit on current room
            pitLiteral = f'P_{curPos[0]}_{curPos[1]}'
            self.addClauseToKB(pitLiteral, -1)

            # Check for stench
            if self.interactive.isStench() == True:
                stenchLiteral = f'S_{curPos[0]}_{curPos[1]}'
                self.addClauseToKB(stenchLiteral, 1)
            else:
                stenchLiteral = f'S_{curPos[0]}_{curPos[1]}'
                self.addClauseToKB(stenchLiteral, -1)

            # Check for breeze
            breezeClause = {}
            if self.interactive.isBreeze() == True:
                breezeLiteral = f'B_{curPos[0]}_{curPos[1]}'
                self.addClauseToKB(breezeLiteral, 1)
            else:
                breezeLiteral = f'B_{curPos[0]}_{curPos[1]}'
                self.addClauseToKB(breezeLiteral, -1)

            # Find safe room to visit
            newRoomDict = {}
            wumpusRoomDict = {}

            for row, col in visited:
                adjacentRoomList = self.getAdjacentRoomList(row, col)

                for X, Y in adjacentRoomList:
                    if visited.get((X, Y)) == None:
                        # Check for no Wumpus and no Pit cell
                        tmpClauses = self.KB.getClause()
                        checkClauses = {f'W_{X}_{Y}': 1, f'P_{X}_{Y}': 1}
                        tmpClauses.append(checkClauses)

                        if self.DPLLSatisfiable(tmpClauses) == False:
                            # Add No Wumpus to KB
                            wumpusLiteral = f'W_{X}_{Y}'
                            self.addClauseToKB(wumpusLiteral, -1)
                            # Add No Pit to KB
                            pitLiteral = f'P_{X}_{Y}'
                            self.addClauseToKB(pitLiteral, -1)

                            newRoomDict[(X, Y)] = True

                        # Check if room has Wumpus
                        tmpClauses = self.KB.getClause()
                        checkClauses = {f'W_{X}_{Y}': -1}
                        tmpClauses.append(checkClauses)

                        if self.DPLLSatisfiable(tmpClauses) == False:
                            wumpusLiteral = f'W_{X}_{Y}'
                            self.addClauseToKB(wumpusLiteral, 1)
                            wumpusRoomDict[(X, Y)] = True

                        # # Check if room has Pit
                        tmpClauses = self.KB.getClause()
                        checkClauses = {f'P_{X}_{Y}': -1}
                        tmpClauses.append(checkClauses)

                        if self.DPLLSatisfiable(tmpClauses) == False:
                            pitLiteral = f'P_{X}_{Y}'
                            self.addClauseToKB(pitLiteral, 1)

            print("Current Position: ", curPos)
            print("Next Valid Room: ", newRoomDict)

            if len(newRoomDict) == 0:
                print("--------------------Find Wumpus To Kill !!!!!!!!!!!!!!!!!!!!!--------------------")
                isWumpus = self.findWumpusToShoot(curPos, visited, wumpusRoomDict)

                if isWumpus == False:
                    print("No Wumpus Left, No Move Left")

                    

                    break
            else:
                self.moveToNextStep(curPos, visited, newRoomDict)

    def solve(self):
        self.interactive.gameStart() # donot modify this line
        
        self.exitWumpusWorld()
        
        return self.interactive.getLogs() # donot modify this line
