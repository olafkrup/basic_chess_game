import basics
import symbols
import numpy as np
import pygame
from sys import exit

width = 1200
height = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

moving = 0

moved = 0
moved_from = 0

attacked = False

turn = 1

while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for piece in symbols.pieces:
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
                    moved = moving
                    moving = 0
                    for tile2 in basics.board:
                        tile2.to_move = False
                        tile2.to_attack = False

    for tile in basics.board:
        screen.blit(tile.image, tile.rect)

    if moving != 0:
        screen.blit(symbols.moving_img, moving.tile.rect.topleft)

    for piece in symbols.pieces:
        if piece.is_dead:
            symbols.pieces.remove(piece)
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
