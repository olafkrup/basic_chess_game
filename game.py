import basics
import symbols
import pygame
from sys import exit

width = 1200
height = 1000

pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

moving = 0
moved = 0
moved_from = 0

attacked = False

check = False

checkmate = False

turn = 1

turn_text = pygame.font.Font(None, 80)

text = pygame.font.Font(None, 35)

sanity_check = []

over = False

while not over:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()

    # visuals representing which color moves
    if turn % 2 == 0:
        clr1 = 'White'
        clr2 = "Black"
    else:
        clr1 = 'Black'
        clr2 = 'White'

    turn_text_surface = turn_text.render("Turn " + str(turn), True, clr2)
    turn_rect = turn_text_surface.get_rect(center=(1000, 150))

    check_text = turn_text.render("Check!", True, clr2)
    check_rect = check_text.get_rect(center = (1000, 500))

    checkmate_text = turn_text.render("Checkmate!", True, clr2)
    checkmate_rect = checkmate_text.get_rect(center = (1000, 500))

    # displaying last 3 moves
    move1 = text.render(basics.moves[-3] + " ", True, clr1)
    move2 = text.render(basics.moves[-2] + " ", True, clr2)
    move3 = text.render(basics.moves[-1] + " ", True, clr1)

    move_rect1 = move1.get_rect(center=(900, 350))
    move_rect2 = move1.get_rect(center=(1000, 350))
    move_rect3 = move1.get_rect(center=(1100, 350))

    screen.blit(symbols.backgr, (0, 0))
    screen.blit(move1, move_rect1)
    screen.blit(move2, move_rect2)
    screen.blit(move3, move_rect3)
    screen.blit(turn_text_surface, turn_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            over = True
        # showing available moves
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for piece in basics.Piece.pieces:
                if piece.tile.rect.collidepoint(mouse_pos) \
                        and not piece.tile.to_move and turn % 2 == piece.color:
                    moving = piece
                    for tile in basics.board:
                        tile.to_move = False
                        tile.to_attack = False
                    for tile in piece.where_move():
                        tile.to_move = True
                        if tile.occupied:
                            tile.to_attack = True
            # moving pieces
            for tile in basics.board:
                if tile.rect.collidepoint(mouse_pos) and tile.to_move:
                    attacked = False
                    moved_from = moving.tile
                    if tile.occupied:
                        attacked = True
                    moving.occupy(tile)
                    all_moves = []
                    turn += 1
                    # pawn promotion
                    for pawn in basics.Pawn.pawns:
                        if pawn.promoted:
                            if pawn.color:
                                basics.Piece.pieces.append(basics.Queen(pawn.tile, symbols.queen_move, pawn.color, 'Q', symbols.queen_img1))
                                pawn.tile.occupant = basics.Piece.pieces[-1]
                            else:
                                basics.Piece.pieces.append(basics.Queen(pawn.tile, symbols.queen_move, pawn.color, 'Q', symbols.queen_img2))
                                pawn.tile.occupant = basics.Piece.pieces[-1]
                            basics.Pawn.pawns.remove(pawn)
                            pawn.is_dead = True
                    # checking all possible moves in order to update check conditions etc
                    for piece in basics.Piece.pieces:
                        sanity_check = piece.where_move()
                        if turn % 2 == piece.color:
                            piece.really_checking = False
                        else:
                            if isinstance(piece, basics.King):
                                piece.check = False
                    # checking if the player has any moves
                    for piece in basics.Piece.pieces:
                        if turn % 2 == piece.color:
                            for tile2 in piece.where_move():
                                all_moves.append(tile2)
                    if len(all_moves) == 0:
                        for king in basics.King.kings:
                            if king.color == turn % 2:
                                if king.check:
                                    print("Checkmate!")
                                    checkmate = True
                                else:
                                    print("Stalemate")
                    else:
                        for king in basics.King.kings:
                            if king.check:
                                print("Check")
                                check = True
                            else:
                                check = False
                    moved = moving
                    moving = 0
                    for tile2 in basics.board:
                        tile2.to_move = False
                        tile2.to_attack = False
                    break

    for tile in basics.board:
        screen.blit(tile.image, tile.rect)

    if moving != 0:
        screen.blit(symbols.moving_img, moving.tile.rect.topleft)

    # displaying and removing pieces
    for piece in basics.Piece.pieces:
        if piece.is_dead:
            if isinstance(piece, basics.Queen):
                basics.Piece.pieces.remove(piece.rook)
                basics.Piece.pieces.remove(piece.bishop)
            basics.Piece.pieces.remove(piece)
        else:
            screen.blit(piece.image, piece.tile.rect)

    # highlighting some pieces
    if moved != 0:
        if attacked:
            screen.blit(symbols.attacked_img, moved.tile.rect.topleft)
            screen.blit(symbols.attacked_img, moved_from.rect.topleft)
        else:
            screen.blit(symbols.moved_img, moved.tile.rect.topleft)
            screen.blit(symbols.moved_img, moved_from.rect.topleft)
        if checkmate:
            screen.blit(checkmate_text, checkmate_rect)
        else:
            for king in basics.King.kings:
                if king.check:
                    screen.blit(symbols.check_img, king.tile.rect.topleft)
                    screen.blit(check_text, check_rect)

    for tile in basics.board:
        if tile.to_move:
            if tile.to_attack:
                screen.blit(symbols.attack_img, tile.rect.topleft)
            else:
                screen.blit(symbols.move_img, tile.rect.topleft)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
exit()
