import numpy as np
import basics
import pygame

abc = basics.abc

board_tiles = []

# images

backgr = pygame.Surface((1200, 1000))
backgr.fill((128, 128, 128))

black = pygame.Surface((100, 100))
black.fill('black')

white = pygame.Surface((100, 100))
white.fill('white')

black2 = pygame.Surface((100, 100))
black2.fill((210, 140, 69))

white2 = pygame.Surface((100, 100))
white2.fill((255, 207, 159))

move_img = pygame.Surface((100, 100), pygame.SRCALPHA)
move_img.fill((0, 0, 0, 0))
pygame.draw.circle(move_img, (90, 255, 67, 150), (50, 50), 25)

moving_img = pygame.image.load('images/moving_img.png')
moving_img.set_alpha(150)

moved_img = pygame.image.load('images/moved_img.png')
moved_img.set_alpha(150)

attack_img = pygame.image.load('images/attack_img.png')
attack_img.set_alpha(150)

attacked_img = pygame.image.load('images/attacked_img.png')
attacked_img.set_alpha(150)

check_img = pygame.image.load('images/check_img.png')
check_img.set_alpha(150)

pawn_img1 = pygame.image.load('images/white_pawn.png')
pawn_img2 = pygame.image.load('images/black_pawn.png')

rook_img1 = pygame.image.load('images/white_rook.png')
rook_img2 = pygame.image.load('images/black_rook.png')

knight_img1 = pygame.image.load('images/white_knight.png')
knight_img2 = pygame.image.load('images/black_knight.png')

bishop_img1 = pygame.image.load('images/white_bishop.png')
bishop_img2 = pygame.image.load('images/black_bishop.png')

queen_img1 = pygame.image.load('images/white_queen.png')
queen_img2 = pygame.image.load('images/black_queen.png')

king_img1 = pygame.image.load('images/white_king3.png')
king_img2 = pygame.image.load('images/black_king.png')

# tile definition
for row in range(8):
    for column in range(8):
        tile = basics.create(basics.Tile(row, column), basics.board)
        if tile.color():
            tile.image = white2
        else:
            tile.image = black2

for row in range(8):
    board_tiles.append([basics.to_tile(abc[column] + str(row + 1)) for column in range(8)])

# move definition
rook_move = np.array([[i, j] for i in range(-7, 8) for j in range(-7, 8)])
rook_move = rook_move[ (rook_move[:, 0] == 0) | (rook_move[:, 1] == 0) ]
rook_move = rook_move[ (rook_move[:, 0] != 0) | (rook_move[:, 1] != 0) ]

knight_move = np.array([[i, j] for i in range(-2, 3) for j in range(-2, 3)])  # fancy array slicing
knight_move = knight_move[ knight_move[:, 0]**2 != knight_move[:, 1]**2 ]
knight_move = knight_move[(knight_move[:, 0] != 0) & (knight_move[:, 1] != 0)]

bishop_move = np.array([[i, j] for i in range(-7, 8) for j in [-i, i]])
bishop_move = bishop_move[ bishop_move[:, 0] * bishop_move[:, 1] != 0 ]

queen_move = [rook_move.copy(), bishop_move.copy()]

king_move1 = [[0, 1], [0, -1], [1, 0], [-1, 0]]
king_move2 = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
king_move = [king_move1, king_move2]

# pawns
for tile in board_tiles[1]:
    pawn = basics.Pawn(tile, np.array([[0, 1]]), 1, '', pawn_img1)
    basics.Piece.pieces.append(pawn)

for tile in board_tiles[6]:
    pawn = basics.Pawn(tile, np.array([[0, -1]]), 0, '', pawn_img2)
    basics.Piece.pieces.append(pawn)

# rooks
basics.Piece.pieces.append(basics.Rook(board_tiles[0][0], rook_move, 1, "R", rook_img1))
basics.Piece.pieces.append(basics.Rook(board_tiles[0][7], rook_move, 1, "R", rook_img1))
basics.Piece.pieces.append(basics.Rook(board_tiles[7][0], rook_move, 0, "R", rook_img2))
basics.Piece.pieces.append(basics.Rook(board_tiles[7][7], rook_move, 0, "R", rook_img2))

# knights
basics.Piece.pieces.append(basics.Knight(board_tiles[0][1], knight_move, 1, 'N', knight_img1))
basics.Piece.pieces.append(basics.Knight(board_tiles[0][6], knight_move, 1, 'N', knight_img1))
basics.Piece.pieces.append(basics.Knight(board_tiles[7][1], knight_move, 0, 'N', knight_img2))
basics.Piece.pieces.append(basics.Knight(board_tiles[7][6], knight_move, 0, 'N', knight_img2))

# bishops
basics.Piece.pieces.append(basics.Piece(board_tiles[0][2], bishop_move, 1, 'B', bishop_img1))
basics.Piece.pieces.append(basics.Piece(board_tiles[0][5], bishop_move, 1, 'B', bishop_img1))
basics.Piece.pieces.append(basics.Piece(board_tiles[7][2], bishop_move, 0, 'B', bishop_img2))
basics.Piece.pieces.append(basics.Piece(board_tiles[7][5], bishop_move, 0, 'B', bishop_img2))

# queens
basics.Piece.pieces.append(basics.Queen(board_tiles[0][3], queen_move, 1, 'Q', queen_img1))
basics.Piece.pieces.append(basics.Queen(board_tiles[7][3], queen_move, 0, 'Q', queen_img2))

# kings
basics.Piece.pieces.append(basics.King(board_tiles[0][4], king_move, 1, 'K', king_img1))
basics.Piece.pieces.append(basics.King(board_tiles[7][4], king_move, 0, 'K', king_img2))


