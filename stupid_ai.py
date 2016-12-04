from random import randint
from game import SIZE

class StupidAI:
    def __init__(self):
        self.name = 'StupidAI #' + str(randint(100, 999))

    def get_ships(self):
        return [ ((0, 0), (0, 1)),
                 ((1, 0), (1, 2)),
                 ((2, 0), (2, 2)),
                 ((3, 0), (3, 3)),
                 ((4, 0), (4, 4)) ]

    def get_move(self):
        x, y = randint(0, SIZE - 1), randint(0, SIZE - 1)
        while self.shots[x][y]:
            x, y = randint(0, SIZE - 1), randint(0, SIZE - 1)
        return (x, y)
