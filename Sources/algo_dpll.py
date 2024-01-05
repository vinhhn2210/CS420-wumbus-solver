import copy
from queue import Queue
from interactive import *

numClauses = 0

class KnowledgeBase:
    def __init__(self):
        self.clauses = []

    def addClause(self, clause):
        self.clauses.append(clause)

    def removeClause(self, clause):
        self.clauses = [elem for elem in self.clauses if elem != clause]

    def getClause(self):
        return copy.deepcopy(self.clauses)

class DPLLAlgo:
    def __init__(self, mapState):
        self.interactive = InteractiveGame()
        self.interactive.loadMap(mapState)

        self.mapSize = mapState.nSize

        self.KB = KnowledgeBase()
        self.roomDict = {}
        self.step = 0

    def addClauseToKB(self, literal, val):
        curClause = {literal: val}
        if self.roomDict.get(literal) == None:
            self.roomDict[literal] = val
            self.KB.addClause(curClause)

    def removeClauseFromKB(self, literal, val):
        if self.roomDict.get(literal) != None:
            self.roomDict.pop(literal)
            self.KB.removeClause({literal: val})

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
            if len(clause) == 1:
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

                count[literal] = count[literal] + 1
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
        global numClauses
        numClauses += 1

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
        return self.DPLL(clauses, symbols, model)

    def DPLLSatisfiable(self, clauses):
        symbols = {}
        for clause in clauses:
            for literal in clause:
                symbols[literal] = True

        model = {}

        for clause in clauses:
            if len(clause) == 1:
                for symbol in clause:
                    model[symbol] = clause[symbol]
        
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

            for X, Y in nextRooms:
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

    def shootWumpus(self, direction):
        DIR = ('UP', 'DOWN', 'LEFT', 'RIGHT')
        DIR_VAL = ((-1, 0), (1, 0), (0, -1), (0, 1))

        self.interactive.changeDirection(direction)  
        isShootWumpusSucessful = self.interactive.shootArrow()   

        if isShootWumpusSucessful == True:
            curPos = self.interactive.getPlayerPosition()
            newPos = [curPos[0], curPos[1]]

            for i in range(4):
                if DIR[i] == direction:
                    newPos[0] += DIR_VAL[i][0]
                    newPos[1] += DIR_VAL[i][1]
                    break

            # Remove Wumpus in current position
            wumpusLiteral = f'W_{newPos[0]}_{newPos[1]}'
            self.removeClauseFromKB(wumpusLiteral, 1)

            # Remove Stench in adjacent room
            adjacentRooms = self.getAdjacentRoomList(newPos[0], newPos[1])
            for room in adjacentRooms:
                if self.interactive.isStenchVisionView(room[0], room[1]) == 0:
                    stenchLiteral = f'S_{room[0]}_{room[1]}'
                    self.removeClauseFromKB(stenchLiteral, 1)
                    self.addClauseToKB(stenchLiteral, -1)

            # Add No Wumpus at current position after shooting
            wumpusLiteral = f'W_{newPos[0]}_{newPos[1]}'
            self.addClauseToKB(wumpusLiteral, -1)

            # Add No Pit at current position after shooting
            pitLiteral = f'P_{newPos[0]}_{newPos[1]}'
            self.addClauseToKB(pitLiteral, -1)

            print('######## Shoot Wumpus Successful at: ', newPos)
            return True

        return False

    def findWumpusToShoot(self, start, visited, wumpusRooms):
        queue = []
        queue.append(start)

        dist = {}
        pre = {}
        dist[start] = 0

        while queue:
            curRoom = queue.pop(0)
            nextRooms = self.getAdjacentRoomList(curRoom[0], curRoom[1])

            for X, Y in nextRooms:
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

        isShoot = self.shootWumpus(path[len(path) - 1])
        if isShoot == True:
            print('Path To Kill Wumpus: ', path)

        return True

    def goToExit(self, start, visited):
        queue = []
        queue.append(start)

        dist = {}
        pre = {}
        dist[start] = 0

        while queue:
            curRoom = queue.pop(0)
            nextRooms = self.getAdjacentRoomList(curRoom[0], curRoom[1])

            for X, Y in nextRooms:
                if visited.get((X, Y)) == True:
                    if dist.get((X, Y)) == None:
                        dist[(X, Y)] = dist[curRoom] + 1
                        pre[(X, Y)] = curRoom
                        queue.append((X, Y))

        resRoom = None
        if dist.get((0, 0)) == None:
            return False

        resRoom = (0, 0)

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
        return True

    def findStenchToShootWumpus(self, start, visited):
        queue = []
        queue.append(start)

        dist = {}
        pre = {}
        dist[start] = 0

        while queue:
            curRoom = queue.pop(0)
            nextRooms = self.getAdjacentRoomList(curRoom[0], curRoom[1])

            for X, Y in nextRooms:
                if visited.get((X, Y)) == True:
                    if dist.get((X, Y)) == None:
                        dist[(X, Y)] = dist[curRoom] + 1
                        pre[(X, Y)] = curRoom
                        queue.append((X, Y))

        resRoom = None
        for i in visited:
            if dist.get(i) != None:
                if self.roomDict.get(f'S_{i[0]}_{i[1]}') != None:
                    if self.roomDict[f'S_{i[0]}_{i[1]}'] == 1:
                        if resRoom == None or dist[resRoom] > dist[i]:
                            resRoom = i

        if resRoom == None:
            return False

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

        for index in range(len(DIR)):
            U, V, D = self.interactive.getPlayerPosition()
            U += DIR_VAL[index][0]
            V += DIR_VAL[index][1]
            if self.roomDict.get(f'W_{U}_{V}') != -1:
                isShootSuccessful = self.shootWumpus(DIR[index])
                if isShootSuccessful == True:
                    break

        return True

    def exitWumpusWorld(self):
        visited = {}

        while not self.interactive.isEnd:
            curAgentState = self.interactive.getPlayerPosition()
            curPos = (curAgentState[0], curAgentState[1])

            print("Number of Clauses: ", len(self.KB.clauses))

            visited[curPos] = True

            # Add Stench-Wumpus bijection Clauses
            row, col = curPos
            curNextRoom = self.getAdjacentRoomList(row, col)
            curCNFDict = {f'S_{row}_{col}': -1}
            for X, Y in curNextRoom:
                curCNF = {}
                curCNF[f'W_{X}_{Y}'] = -1
                curCNF[f'S_{row}_{col}'] = 1
                if curCNF not in self.KB.clauses:
                    self.KB.addClause(curCNF)
                curCNFDict[f'W_{X}_{Y}'] = 1
            if curCNFDict not in self.KB.clauses:
                self.KB.addClause(curCNFDict)

            # Add Breeze-Pit bijection Clauses
            curCNFDict = {f'B_{row}_{col}': -1}
            for X, Y in curNextRoom:
                curCNF = {}
                curCNF[f'P_{X}_{Y}'] = -1
                curCNF[f'B_{row}_{col}'] = 1
                if curCNF not in self.KB.clauses:
                    self.KB.addClause(curCNF)
                curCNFDict[f'P_{X}_{Y}'] = 1
            if curCNFDict not in self.KB.clauses:
                self.KB.addClause(curCNFDict)

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

            nextRoomStep = []
            for row, col in visited:
                adjacentRoomList = self.getAdjacentRoomList(row, col)
                for X, Y in adjacentRoomList:
                    if visited.get((X, Y)) == None:
                        nextRoomStep.append((X, Y))
                        if self.roomDict.get(f'W_{X}_{Y}') == -1 and self.roomDict.get(f'P_{X}_{Y}') == -1:
                            newRoomDict[(X, Y)] = True

                    if self.roomDict.get(f'W_{X}_{Y}') == 1:
                        wumpusRoomDict[(X, Y)] = True

            nextRoomStep = set(nextRoomStep)

            # print("Before: ", numClauses)

            for X, Y in nextRoomStep:
                # Check for no Wumpus and no Pit cell
                if self.roomDict.get(f'W_{X}_{Y}') == -1 and self.roomDict.get(f'P_{X}_{Y}') == -1:
                    pass
                else:
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
                        # Update Room Dictionary
                        newRoomDict[(X, Y)] = True

                # Check if room has Wumpus
                if self.roomDict.get(f'W_{X}_{Y}') == 1:
                    pass
                else:
                    tmpClauses = self.KB.getClause()
                    checkClauses = {f'W_{X}_{Y}': -1}
                    tmpClauses.append(checkClauses)

                    if self.DPLLSatisfiable(tmpClauses) == False:
                        wumpusLiteral = f'W_{X}_{Y}'
                        self.addClauseToKB(wumpusLiteral, 1)
                        wumpusRoomDict[(X, Y)] = True

                # Check if room has Pit
                if self.roomDict.get(f'P_{X}_{Y}') == 1:
                    pass
                else:
                    tmpClauses = self.KB.getClause()
                    checkClauses = {f'P_{X}_{Y}': -1}
                    tmpClauses.append(checkClauses)

                    if self.DPLLSatisfiable(tmpClauses) == False:
                        pitLiteral = f'P_{X}_{Y}'
                        self.addClauseToKB(pitLiteral, 1)

            # print("After: ", numClauses)

            # Add to Knowledgebase Log
            self.step += 1
            self.interactive.appendKBLog(f'Step {self.step}: List of CNF Sentences')
            for sentence in self.KB.clauses:
                cnt = 0
                curCNFStr = ''
                for literal in sentence:
                    if cnt > 0:
                        curCNFStr += '|'
                    if sentence[literal] == -1:
                        curCNFStr += chr(172)
                    curCNFStr += literal.replace('_', '')
                    cnt += 1
                self.interactive.appendKBLog(curCNFStr)

            # self.interactive.debug()  
            print("Next Valid Room: ", newRoomDict)

            if len(newRoomDict) == 0:
                print("--------------------Find Wumpus To Kill !!!!!!!!!!!!!!!!!!!!!--------------------")
                isWumpus = self.findWumpusToShoot(curPos, visited, wumpusRoomDict)

                if isWumpus == False:
                    print("######No Wumpus To Shoot, Let's Find Stench To Shoot######")
                    isGoToStench = self.findStenchToShootWumpus(curPos, visited)

                    if isGoToStench == False:
                        print("No Wumpus Left, No Move Left")

                        isGoToExit = self.goToExit(curPos, visited)

                        if isGoToExit == False:
                            print("No Path To Exit!!!!!")
                            self.interactive.gameEnd()
                        else:
                            print('Go To Cell 1, 1 Successful!!!!!')
                            self.interactive.gameEnd()
                        break                        
            else:
                self.moveToNextStep(curPos, visited, newRoomDict)

    def solve(self):
        self.interactive.gameStart() # donot modify this line
        
        self.exitWumpusWorld()
        
        return self.interactive.getLogs() # donot modify this line

