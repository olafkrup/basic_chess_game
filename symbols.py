import numpy as np
import basics

abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

board_tiles = []

for row in range(8):
    board_tiles.append([basics.to_tile(abc[column] + str(row + 1)) for column in range(8)])

Pawns = ()

for tile in board_tiles[1]:
    pawn = basics.Pawn(tile, [[0, 1]], 1, '')

