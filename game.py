import basics
import symbols
import numpy as np
import pygame
from sys import exit

width = 1200
height = 800

pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

moving = 0
moved = 0
moved_from = 0

attacked = False

turn = 1

turn_text = pygame.font.Font(None, 80)

text = pygame.font.Font(None, 35)

sanity_check = []

while True:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()

    if turn % 2 == 0:
        clr1 = 'White'
        clr2 = "Black"
    else:
        clr1 = 'Black'
        clr2 = 'White'

    turn_text_surface = turn_text.render("Turn " + str(turn), True, clr2)
    turn_rect = turn_text_surface.get_rect(center=(1000, 150))

    move1 = text.render(basics.moves[-3] + " ", True, clr1)
    move2 = text.render(basics.moves[-2] + " ", True, clr2)
    move3 = text.render(basics.moves[-1] + " ", True, clr1)

    move_rect1 = move1.get_rect(center=(900, 350))
    move_rect2 = move1.get_rect(center=(1000, 350))
    move_rect3 = move1.get_rect(center=(1100, 350))

    screen.blit(symbols.backgr, (800, 0))
    screen.blit(move1, move_rect1)
    screen.blit(move2, move_rect2)
    screen.blit(move3, move_rect3)
    screen.blit(turn_text_surface, turn_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
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
            for tile in basics.board:
                if tile.rect.collidepoint(mouse_pos) and tile.to_move:
                    attacked = False
                    moved_from = moving.tile
                    if tile.occupied:
                        attacked = True
                    moving.occupy(tile)
                    turn += 1
                    for piece in basics.Piece.pieces:
                        sanity_check = piece.where_move()
                    moved = moving
                    moving = 0
                    for tile2 in basics.board:
                        tile2.to_move = False
                        tile2.to_attack = False

    for tile in basics.board:
        screen.blit(tile.image, tile.rect)

    if moving != 0:
        screen.blit(symbols.moving_img, moving.tile.rect.topleft)

    for piece in basics.Piece.pieces:
        if piece.is_dead:
            basics.Piece.pieces.remove(piece)
        else:
            screen.blit(piece.image, piece.tile.rect)

    if moved != 0:
        if attacked:
            screen.blit(symbols.attacked_img, moved.tile.rect.topleft)
            screen.blit(symbols.attacked_img, moved_from.rect.topleft)
        else:
            screen.blit(symbols.moved_img, moved.tile.rect.topleft)
            screen.blit(symbols.moved_img, moved_from.rect.topleft)

    for tile in basics.board:
        if tile.to_move:
            if tile.to_attack:
                screen.blit(symbols.attack_img, tile.rect.topleft)
            else:
                screen.blit(symbols.move_img, tile.rect.topleft)

    pygame.display.update()
    clock.tick(60)
