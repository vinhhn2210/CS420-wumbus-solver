class InteractiveGame:
    def __init__(self, mapState):
        self.mapState = copy.deepcopy(mapState)
        self.playerPosition = (0, 0)


    def play(self):
        while True:
            print(self.game)
            if self.game.is_over():
                break
            self.game.play_turn()
        print(self.game)
        print("Game over!")
        print("Winner: {}".format(self.game.winner()))
    