SIZE = 10
SHIPS = [2, 3, 3, 4, 5]
NAMES = ['patrol boat',
 'submarine',
 'destroyer',
 'battleship',
 'aircraft carrier']

def size(((x1, y1), (x2, y2))):
    assert x1 < x2 or y1 < y2, 'Points have to be ordered'
    if x1 == x2:
        return y2 - y1 + 1
    assert y1 == y2, 'Ships can\'t be diagonal'
    return x2 - x1 + 1

def hit(x, y):
    def f(((x1, y1), (x2, y2))):
        if x1 == x2:
            return x == x1 and y1 <= y <= y2
        return y == y1 and x1 <= x <= x2
    return f

def intersect(((x1, y1), (x2, y2)), ((x3, y3), (x4, y4))):
    if x1 == x2 == x3 == x4: return y2 >= y3 or y4 >= y1
    if y1 == y2 == y3 == y4: return x2 >= x3 or x4 >= x1
    if x1 == x2 and x3 == x4: return False
    if y1 == y2 and y3 == y4: return False
    if x1 == x2: return x3 <= x1 <= x4 and y1 <= y3 <= y2
    return y3 <= y1 <= y4 and x1 <= x3 <= x2

def no_overlaps(ships):
    checked = []
    for ship in ships:
        for other in checked:
            if intersect(ship, other):
                return False
        checked.append(ship)
    return True


class Game:
    def __init__(self, a, b):
        assert a.name != b.name, 'The two players must have unique names'
        self.a = a
        self.b = b
        self.player = None
        self.a.shots = [ [ False for _ in range(SIZE) ] for _ in range(SIZE) ]
        self.b.shots = [ [ False for _ in range(SIZE) ] for _ in range(SIZE) ]
        self.a.ships = None
        self.b.ships = None
        self.a.hits = None
        self.b.hits = None

    def check_ships(self):
        return len(self.a.ships) == 5 and len(self.b.ships) == 5 \
            and map(size, self.a.ships) == SHIPS \
            and map(size, self.b.ships) == SHIPS \
            and no_overlaps(self.a.ships) and no_overlaps(self.b.ships)

    def start(self):
        self.player = self.a
        self.a.shots = [ [ False for _ in range(SIZE) ] for _ in range(SIZE) ]
        self.b.shots = [ [ False for _ in range(SIZE) ] for _ in range(SIZE) ]
        self.a.ships = self.a.get_ships()
        self.b.ships = self.b.get_ships()
        self.a.ships.sort(key=size)
        self.b.ships.sort(key=size)
        self.a.hits = [0] * 5
        self.b.hits = [0] * 5
        assert self.check_ships(), 'Ships must be valid'

    def toggle_player(self):
        if self.player is self.a:
            self.player = self.b
        else:
            self.player = self.a

    def check_hit(self, x, y):
        res = map(hit(x, y), self.player.ships)
        for i, r in enumerate(res):
            if r:
                self.player.hits[i] += 1
                return (True, i if self.player.hits[i] == SHIPS[i] else None)
        return (False, None)

    def move(self, x, y):
        assert 0 <= x < SIZE and 0 <= y < SIZE, 'Shot has to be in bounds'
        if self.player.shots[x][y]: return (None, None)
        self.player.shots[x][y] = True
        return self.check_hit(x, y)

    def over(self):
        return self.a.hits == SHIPS or self.b.hits == SHIPS

    def winner(self):
        assert self.over(), 'Game must be over'
        if self.a.hits == SHIPS:
            return self.a
        return self.b

    def main(self):
        print 'Starting game between %s and %s' % (self.a.name, self.b.name)
        self.start()
        while not self.over():
            x, y = self.player.get_move()
            print self.player.name + ' shoots for (%s, %s)' % (x, y),
            h, s = self.move(x, y)
            if h is None:
                print 'invalid move...'
                continue
            if h:
                print 'hit!',
                if s >= 0:
                    print self.player.name + ' sunk the ' + NAMES[s] + '!'
                else:
                    print
            else:
                print 'miss.'
                print '\n' + '-' * 40 + '\n'
                self.toggle_player()

        print self.winner().name + ' wins!'
