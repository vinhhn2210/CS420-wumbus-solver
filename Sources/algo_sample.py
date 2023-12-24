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
    + self.interactive.isGold() -> return True if agent get a gold, False otherwise
'''

class AlgoSample:
    def __init__(self, mapState):
        self.interactive = InteractiveGame()
        self.interactive.loadMap(mapState)

    def solve(self):
        self.interactive.gameStart() # donot modify this line
        
        player = self.interactive.getPlayerPosition()
        while not self.interactive.isEnd:
            self.interactive.move('UP')
        
        return self.interactive.getLogs() # donot modify this line