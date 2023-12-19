from colorama import Fore
from mapstate import *

# set logging level
# logging.basicConfig(level=logging.DEBUG)

CONVERT = {'B': 1, 'S': 2, 'BS': 3}

# def expandview(view, theMap, nSize, playerPos):
#     availableView = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#     if playerPos[0] == 0:
#         availableView.remove((-1, 0))
#     if playerPos[0] == nSize - 1:
#         availableView.remove((1, 0))
#     if playerPos[1] == 0:
#         availableView.remove((0, -1))
#     if playerPos[1] == nSize - 1:
#         availableView.remove((0, 1))
#     for i in availableView:
#         if i not in view:
#             view[i] = theMap[playerPos[0] + i[0]][playerPos[1] + i[1]]
#     return view
def possibleMove(playerPos, nSize):
    ''' return a list of possible move from the current position'''
    available = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    if playerPos[0] == 0:
        available.remove((-1, 0))
    if playerPos[0] == nSize - 1:
        available.remove((1, 0))
    if playerPos[1] == 0:
        available.remove((0, -1))
    if playerPos[1] == nSize - 1:
        available.remove((0, 1))
    possibleMove = []
    for i in available:
        possibleMove.append((playerPos[0] + i[0], playerPos[1] + i[1]))
    # print(Fore.YELLOW + "Possible move: ")
    # print(Fore.WHITE, possibleMove)
    return possibleMove

def newMove(view, playerPos, nSize):
    '''return a list of new move from the current position'''
    return [i for i in possibleMove(playerPos, nSize) if i not in view]

def travelCost(initial, goal, point, view, nSize):
    ''' bfs search to find the shortest path from previous to current
        return the path and the point, each step cost 10 point
        '''
    path = []
    visit= [initial]
    parent = {}
    parent[initial] = None
    while (visit):
        current = visit.pop(0)
        if current == goal:
            print([(current[0], current[1], point)])
            return [(current[0], current[1], point)], point
        for i in possibleMove(current, nSize):
            if i in view and i not in parent:
                parent[i] = current
                visit.append(i)
        point -= 10
    reverse = point + 10
    # print(parent)
    while (current != initial):
        res = (current[0], current[1], reverse)
        path.append(res)
        current = parent[current]
        reverse += 10
    print(path[::-1])
    return path[::-1], point

def agentMap(mapstate, view):
    nSize = mapstate.nSize
    temp = [[[] for i in range(nSize)] for j in range(nSize)]
    for i in range(nSize):
        for j in range(nSize):
            if (i, j) not in view:
                # view[i, j] = ['x']
                temp[i][j] = ['x']
            else:
                temp[i][j] = mapstate.mazer[i][j]
                # temp[i][j] = view[(i, j)]
                # temp[i][j] = ']
    print(Fore.YELLOW + "Agent map: ")
    MapState('agentMap', nSize, temp).printMap()


def findNextMove(previous, explore, view, nSize, point):
    ''' find the next move from the current position using bfs search
        return the next move and the point
        '''
    # print(Fore.YELLOW + "\nFind next move start from: ", previous)
    # print(Fore.WHITE + "Explore: ", explore)
    # print("")
    visit = [previous]
    parent = {}
    parent[previous] = None
    flag = False
    while (visit):
        current = visit.pop(0)
        # print("Consider", current)
        if current in explore:
            break
        for i in possibleMove(current, nSize):
            # print("From ", current, " check ", i, " in", explore)
            if i in view and i not in parent:
                parent[i] = current
                visit.append(i)
            if i in explore:
                parent[i] = current
                current = i
                destination = current
                # print("Found: ", i)
                flag = True
                break
        point -= 10
        if flag:
            break        
    # trace back the path
    if current not in explore:
        return None, None, point
    
    path = []
    tmp = point
    destination = current
    while (current != previous):
        path.append((current[0], current[1], tmp))
        tmp += 10
        current = parent[current]
    return path[::-1], destination, point
    

def nerve(mapstate, point):
    '''
    return the solution of the problem which is a list of (x, y, point, shoot) tuple
    '''
    view = {}
    estimate = {}
    current = mapstate.initialPos
    solution = [(current[0], current[1], point)]
    nSize = mapstate.nSize
    explore = [(current[0], current[1])]
    mapstate.printMap()
    
    while (True):
        
        ### CHECK current's state
        curPos = (current[0], current[1])
        view[curPos] = mapstate.mazer[current[0]][current[1]]
        # contain gold
        if 'G' in view[curPos]:
            point += 1000
            solution[-1] = (current[0], current[1], point)
        # contain warning
        if 'B' in view[curPos] or 'S' in view[curPos]:
            for i in newMove(view, current, nSize):
                if 'B' in view[curPos] and 'S' in view[curPos]:
                    key = CONVERT['BS']
                elif 'B' in view[curPos]:
                    key= CONVERT['B']
                elif 'S' in view[curPos]:
                    key = CONVERT['S'] 
                if i in estimate:
                    compare = key ^ estimate[i]
                    if compare == 0 or key == 3:
                        continue
                    else:
                        if estimate[i] == 3:
                            estimate[i] = key
                            continue
                        else:
                            # this room is safe
                            explore.append(i)
                            view[i] = []
                else:
                    estimate[i] = key
        # contain "-"
        if '-' in view[curPos]:
            # print("It's a -")
            for i in newMove(view, current, nSize):
                explore.append(i)
        
        if explore == []:
            break
        
        ### FIND next move
        previous = current
        explore.remove(current)
        extraMove, current, point = findNextMove(previous, explore, view, nSize, point)
        # print("Next move: ", current)
        # if current is None, escape the maze
        if current is None:
            # check if the door is visible
            door = (nSize - 1, 0)
            if door in view:
                explore = [door]
                extraMove, current, point = findNextMove(previous, explore, view, nSize, point)
                solution.extend(extraMove)
                solution.append((4, 0, point + 10))
            else:
                print("Have not found the door")
            
            break
        else:
            # print("Remove: ", current)
            if extraMove:
                solution.extend(extraMove)
    print(Fore.GREEN + "\n\nWhat i have view: ")
    agentMap(mapstate, view)
    return solution
    