import numpy as np
import basics
import pygame

abc = basics.abc

board_tiles = []

black = pygame.Surface((100, 100))
black.fill('black')

white = pygame.Surface((100, 100))
white.fill('white')

# tiles

for row in range(8):
    for column in range(8):
        tile = basics.create(basics.Tile(row, column), basics.board)
        if tile.color():
            tile.image = white
        else:
            tile.image = black

for row in range(8):
    board_tiles.append([basics.to_tile(abc[column] + str(row + 1)) for column in range(8)])

pieces = []

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
king_move = np.array(king_move)

# images
pawn_img1 = pygame.image.load('images/white_pawn2.png')
pawn_img2 = pygame.image.load('images/black_pawn2.png')

rook_img1 = pygame.image.load('images/white_rook2.png')
rook_img2 = pygame.image.load('images/black_rook2.png')

knight_img1 = pygame.image.load('images/white_knight2.png')
knight_img2 = pygame.image.load('images/black_knight2.png')

bishop_img1 = pygame.image.load('images/white_bishop2.png')
bishop_img2 = pygame.image.load('images/black_bishop2.png')

queen_img1 = pygame.image.load('images/white_queen2.png')
queen_img2 = pygame.image.load('images/black_queen2.png')

king_img1 = pygame.image.load('images/white_king2.png')
king_img2 = pygame.image.load('images/black_king2.png')

# pawns
for tile in board_tiles[1]:
    pawn = basics.Pawn(tile, np.array([[0, 1]]), 1, '', pawn_img1)
    pieces.append(pawn)

for tile in board_tiles[6]:
    pawn = basics.Pawn(tile, np.array([[0, -1]]), 0, '', pawn_img2)
    pieces.append(pawn)

# rooks
pieces.append(basics.Piece(board_tiles[0][0], rook_move, 1, "R", rook_img1))
pieces.append(basics.Piece(board_tiles[0][7], rook_move, 1, "R", rook_img1))
pieces.append(basics.Piece(board_tiles[7][0], rook_move, 0, "R", rook_img2))
pieces.append(basics.Piece(board_tiles[7][7], rook_move, 0, "R", rook_img2))

# knights
pieces.append(basics.Knight(board_tiles[0][1], knight_move, 1, 'N', knight_img1))
pieces.append(basics.Knight(board_tiles[0][6], knight_move, 1, 'N', knight_img1))
pieces.append(basics.Knight(board_tiles[7][1], knight_move, 0, 'N', knight_img2))
pieces.append(basics.Knight(board_tiles[7][6], knight_move, 0, 'N', knight_img2))

# bishops
pieces.append(basics.Piece(board_tiles[0][2], bishop_move, 1, 'B', bishop_img1))
pieces.append(basics.Piece(board_tiles[0][5], bishop_move, 1, 'B', bishop_img1))
pieces.append(basics.Piece(board_tiles[7][2], bishop_move, 0, 'B', bishop_img2))
pieces.append(basics.Piece(board_tiles[7][5], bishop_move, 0, 'B', bishop_img2))

# queens
pieces.append(basics.Piece(board_tiles[0][3], queen_move, 1, 'Q', queen_img1))
pieces.append(basics.Piece(board_tiles[7][3], queen_move, 0, 'Q', queen_img2))

# kings
pieces.append(basics.Piece(board_tiles[0][4], king_move, 1, 'K', king_img1))
pieces.append(basics.Piece(board_tiles[7][4], king_move, 0, 'K', king_img2))



