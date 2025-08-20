import numpy as np
import basics

abc = basics.abc

board_tiles = []

# tiles
for row in range(8):
    board_tiles.append([basics.to_tile(abc[column] + str(row + 1)) for column in range(8)])

pieces = []

# pawns
for tile in board_tiles[1]:
    pawn = basics.Pawn(tile, [[0, 1]], 1, '')
    pieces.append(pawn)

for tile in board_tiles[6]:
    pawn = basics.Pawn(tile, [[0, -1]], 0, '')
    pieces.append(pawn)

# move definition
rook_move = np.array([[i, j] for i in range(-7, 8) for j in range(-7, 8)])
rook_move = rook_move[ (rook_move[:, 0] == 0) | (rook_move[:, 1] == 0) ]
rook_move = rook_move[ (rook_move[:, 0] != 0) | (rook_move[:, 1] != 0) ]

knight_move = np.array([[i, j] for i in range(-2, 3) for j in range(-2, 3)])  # fancy array slicing
knight_move = knight_move[ knight_move[:, 0]**2 != knight_move[:, 1]**2 ]
knight_move = knight_move[(knight_move[:, 0] != 0) & (knight_move[:, 1] != 0)]

bishop_move = np.array([[i, j] for i in range(-7, 8) for j in [-i, i]])
bishop_move = bishop_move[ bishop_move[:, 0] * bishop_move[:, 1] != 0 ]


queen_move = np.array(rook_move.tolist() + bishop_move.tolist())

king_move = [[i, j] for i in range(-1, 2) for j in range(-1, 2)]
king_move.remove([0, 0])

# rooks
pieces.append(basics.Piece(board_tiles[0][0], rook_move, 1, "R"))
pieces.append(basics.Piece(board_tiles[0][7], rook_move, 1, "R"))
pieces.append(basics.Piece(board_tiles[7][0], rook_move, 0, "R"))
pieces.append(basics.Piece(board_tiles[7][7], rook_move, 0, "R"))

# knights
pieces.append(basics.Knight(board_tiles[0][1], knight_move, 1, 'N'))
pieces.append(basics.Knight(board_tiles[0][6], knight_move, 1, 'N'))
pieces.append(basics.Knight(board_tiles[7][1], knight_move, 0, 'N'))
pieces.append(basics.Knight(board_tiles[7][6], knight_move, 0, 'N'))

# bishops
pieces.append(basics.Piece(board_tiles[0][2], bishop_move, 1, 'B'))
pieces.append(basics.Piece(board_tiles[0][5], bishop_move, 1, 'B'))
pieces.append(basics.Piece(board_tiles[7][2], bishop_move, 0, 'B'))
pieces.append(basics.Piece(board_tiles[7][5], bishop_move, 0, 'B'))

#queens
pieces.append(basics.Piece(board_tiles[0][3], queen_move, 1, 'Q'))
pieces.append(basics.Piece(board_tiles[7][3], queen_move, 0, 'Q'))

#kings
pieces.append(basics.Piece(board_tiles[0][4], king_move, 1, 'K'))
pieces.append(basics.Piece(board_tiles[7][4], king_move, 0, 'K'))

for x in pieces:
    print(x)


