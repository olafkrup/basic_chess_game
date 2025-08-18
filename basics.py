import numpy as np

abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
board = []  # table of all tiles


def create(tile, board0):  # ensures tiles arent duplicated
    for x in board0:
        if x == tile:
            return x
    board0.append(tile)
    return tile


def to_tile(notation):  # converts a chess notation into a tile
    if type(notation) == str:
        if len(notation) == 2:
            row = int(abc.index(notation[0]))
            column = int(notation[1]) - 1
            return create(Tile(row, column), board)


class Tile:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.occupied = False
        self.occupant = 0  # arbitrary definition

    def distance(self, tile):  # Euclidean distance between tiles
        return float(((self.row - tile.row)**2 + (self.column - tile.column)**2)**0.5)

    def bounded(self):  # ensures the tile is within 8x8 bounds
        if 0 <= self.row <= 7 and 0 <= self.column <= 7:
            return True
        return False

    def __add__(self, tile):
        return create(Tile(self.row + tile.row, self.column + tile.column), board)

    def __eq__(self, tile):
        return isinstance(tile, Tile) and self.row == tile.row and self.column == tile.column

    def __hash__(self):
        return hash((self.row, self.column))

    def gt(self, tile1, tile2):
        if (self.distance(tile1) > self.distance(tile2)) and (tile1.distance(tile2) <= self.distance(tile1)):
            return True
        return False

    def printout(self):
        return abc[self.row] + str(self.column + 1)

    def color(self):  # White = 1, Black = 0
        if self.row % 2 == self.column % 2:
            return 1
        return 0


class Piece:
    def __init__(self, tile, move, color, name):
        self.tile = create(tile, board)
        self.tile.occupied = True
        self.tile.occupant = self
        self.move = move  # coordinates [x,y] of possible moves
        self.color = color  # white = 1, black = 0
        self.is_dead = False
        self.name = name

    def where_move(self):
        ret = []
        to_rmv = []
        for cord in self.move:  # list of [x,y] coordinates
            dest = self.tile + Tile(cord[0], cord[1])
            if dest.bounded():
                ret.append(dest)
        for tile in ret:
            if tile.occupied:  # disables jumping
                for tile2 in ret:
                    if self.tile.gt(tile2, tile):
                        to_rmv.append(tile2)
                if tile.occupant.color == self.color:  # no friendly-fire
                    to_rmv.append(tile)

        ret = [tile for tile in ret if tile not in set(to_rmv)]
        return ret

    def occupy(self, tile):
        tile = create(tile, board)
        self.tile.occupied = False  # moving leaves the tile unoccupied

        if tile in self.where_move():
            if tile.occupied:
                tile.occupant.is_dead = True
                print(self.name + "x" + tile.printout())
            else:
                print(self.name + tile.printout())

            tile.occupied = True
            tile.occupant = self
            self.tile = create(tile, board)


class Knight(Piece):
    def where_move(self):
        ret = []
        to_rmv = []

        for cord in self.move:  # list of [x,y] coordinates
            dest = self.tile + Tile(cord[0], cord[1])
            if dest.bounded():
                ret.append(dest)
        # attacking (with allowed jumping)
        for tile in ret:
            if tile.occupied and tile.occupant.color == self.color:  # no friendly-fire
                to_rmv.append(tile)

        ret = [tile for tile in ret if tile not in set(to_rmv)]
        return ret


class Pawn(Piece):
    def __init__(self, tile, move, color, name):
        super().init(tile, move, color, name)
        self.first_move = True
        self.copy_move = self.move.copy()

    def where_move(self):
        # allowing pawns to move two spaces in first move
        if self.first_move():
            self.move = np.array(self.move.tolist() + self.copy_move.tolist())
        else:
            self.move = self.copy_move
        # standard
        ret = []
        for cord in self.move:  # list of [x,y] coordinates
            dest = self.tile + Tile(cord[0], cord[1])
            if dest.bounded() and not dest.occupied:
                ret.append(dest)
        # pawn attack
        if self.color:  # white
            attack_move = np.array([[1, 1], [-1, 1]])
        else:  # black
            attack_move = np.array([[-1, 1], [-1, -1]])
        for cord in attack_move:
            dest_attack = self.tile + Tile(cord[0], cord[1])
            if dest_attack.occupied:
                if dest_attack.occupant.color != self.color:
                    ret.append(dest_attack)
        return ret

    def occupy(self, tile):
        super().occupy(self, tile)
        self.first_move = False


print("Hello World!")

