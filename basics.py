import numpy as np
import pygame

abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
board = []  # table of all tiles
moves = [" ", " ", " ... "]  #


size = 800
tile_size = 100

dead = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)


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
    def __init__(self, row, column, image=dead):
        self.row = row
        self.column = column
        self.occupied = False
        self.occupant = 0  # arbitrary definition
        self.image = image

        pos = (self.row * tile_size, size - self.column * tile_size)
        self.rect = self.image.get_rect(bottomleft=pos)

        self.to_move = False
        self.to_attack = False

    def distance(self, tile):  # Euclidean distance between tiles
        return float(((self.row - tile.row)**2 + (self.column - tile.column)**2)**0.5)

    def bounded(self):  # ensures the tile is within 8x8 bounds
        if 0 <= self.row <= 7 and 0 <= self.column <= 7:
            return True
        return False

    def cord(self):
        return [self.row, self.column]

    def __add__(self, cord):  # creates a new tile with added coordinates
        return create(Tile(self.row + cord[0], self.column + cord[1]), board)

    def __sub__(self, cord):
        return create(Tile(self.row - cord[0], self.column - cord[1]), board)

    def __eq__(self, tile):
        return isinstance(tile, Tile) and self.row == tile.row and self.column == tile.column

    def __hash__(self):
        return hash((self.row, self.column))

    def __str__(self):
        return self.name()

    def gt(self, tile1, tile2):
        if (self.distance(tile1) > self.distance(tile2)) and (tile1.distance(tile2) <= self.distance(tile1)):
            return True
        return False

    def name(self):
        return abc[self.row] + str(self.column + 1)

    def color(self):  # White = 1, Black = 0
        if self.row % 2 == self.column % 2:
            return 1
        return 0


class Piece:
    def __init__(self, tile, move, color, name, image=dead):
        self.tile = create(tile, board)
        self.tile.occupied = True
        self.tile.occupant = self
        if not isinstance(move, list):
            self.move = move.tolist()
        else:
            self.move = move
        self.color = color  # white = 1, black = 0
        self.is_dead = False
        self.name = name
        self.image = image
        self.first_move = True
        tile_center = self.tile.rect.center
        self.rect = self.image.get_rect(center=tile_center)

    def __str__(self):
        return self.name + self.tile.name()

    def where_move(self):
        ret = []
        to_rmv = []
        for cord in self.move:  # list of [x,y] coordinates
            dest = self.tile + cord
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

    def occupy(self, tile, if_print=True):
        tile = create(tile, board)
        self.tile.occupied = False  # moving leaves the tile unoccupied
        if tile.occupied:
            tile.occupant.is_dead = True
            tile.occupant.image = dead
            if if_print:
                moves.append(self.name + "x" + tile.name())
        elif if_print:
            moves.append(self.name + tile.name())

        tile.occupied = True
        tile.occupant = self
        self.first_move = False
        self.tile = create(tile, board)
        tile_center = self.tile.rect.center
        self.rect = self.image.get_rect(center=tile_center)


class Knight(Piece):
    def where_move(self):
        ret = []
        to_rmv = []

        for cord in self.move:  # list of [x,y] coordinates
            dest = self.tile + cord
            if dest.bounded():
                ret.append(dest)
        # attacking (with allowed jumping)
        for tile in ret:
            if tile.occupied and tile.occupant.color == self.color:  # no friendly-fire
                to_rmv.append(tile)

        ret = [tile for tile in ret if tile not in set(to_rmv)]
        return ret


class Pawn(Piece):
    def __init__(self, tile, move, color, name, image=dead):
        super().__init__(tile, move, color, name, image)
        self.copy_move = self.move.copy()
        if self.color:  # white
            self.attack_move = [[1, 1], [-1, 1]]
        else:  # black
            self.attack_move = [[1, -1], [-1, -1]]

    def where_move(self):
        # allowing pawns to move two spaces in first move
        if self.first_move:
            if self.color:
                self.move.append([0, 2])
            else:
                self.move.append([0, -2])
        else:
            self.move = self.copy_move
        ret = super().where_move()
        to_rmv = []
        # pawn attack
        for cord in self.attack_move:
            dest_attack = self.tile + cord
            if dest_attack.occupied:
                if dest_attack.occupant.color != self.color:
                    ret.append(dest_attack)
        ret = [tile for tile in ret if tile not in set(to_rmv)]
        return ret


class Queen(Piece):
    def __init__(self, tile, move, color, name, image=dead):
        super().__init__(tile, move, color, name, image)
        self.rook = Piece(tile, move[0], color, '')
        self.bishop = Piece(tile, move[1], color, '')
        tile.occupant = self

    def where_move(self):
        return self.rook.where_move() + self.bishop.where_move()

    def occupy(self, tile):
        super().occupy(tile)
        self.rook.tile = tile
        self.bishop.tile = tile


class King(Piece):
    def __init__(self, tile, move, color, name, image=dead):
        super().__init__(tile, move, color, name, image)
        self.rook = Piece(tile, move[0], color, '')
        self.bishop = Piece(tile, move[1], color, '')
        self.castle_tile1 = 0
        self.castle_tile2 = 0
        tile.occupant = self

    def can_castle(self, rook):
        if rook.name == 'R' and rook.first_move and rook.color == self.color:
            for tile in self.rook.where_move():
                if tile in rook.where_move():
                    self.castle_tile1 = tile + (tile - self.tile.cord()).cord()
                    self.castle_tile2 = tile
                    return True
        return False

    def where_move(self):
        ret = self.rook.where_move() + self.bishop.where_move()
        to_rmv = []
        # castling
        if self.first_move:
            for tile in [to_tile("A1"), to_tile("A8"), to_tile("H1"), to_tile("H8")]:
                if tile.occupied:
                    rook = tile.occupant
                    if self.can_castle(rook):
                        ret.append(self.castle_tile1)
        # no sacrificing
        for tile in board:
            if tile.occupied:
                piece = tile.occupant
                if piece.color != self.color:
                    if isinstance(piece, King):
                        for tile2 in ret:
                            if tile2 in (piece.rook.where_move() + piece.bishop.where_move()):
                                to_rmv.append(tile2)
                    elif isinstance(piece, Pawn):
                        for tile2 in ret:
                            for cord in piece.attack_move:
                                if tile2 == (piece.tile + cord):
                                    to_rmv.append(tile2)
                    else:
                        for tile2 in ret:
                            if tile2 in piece.where_move():
                                to_rmv.append(tile2)

        ret = [tile for tile in ret if tile not in set(to_rmv)]
        return ret

    def occupy(self, tile):
        if self.castle_tile1 == tile:
            for tile0 in [to_tile("A1"), to_tile("A8"), to_tile("H1"), to_tile("H8")]:
                if tile0.occupied:
                    rook = tile0.occupant
                    if tile in rook.where_move():
                        rook.occupy(self.castle_tile2)
        self.first_move = False
        super().occupy(tile)
        self.rook.tile = tile
        self.bishop.tile = tile


print("Hello World!")

