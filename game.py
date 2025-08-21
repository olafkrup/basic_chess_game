import basics
import symbols
import numpy as np
import pygame

width = 800
height = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

move_img1 = pygame.Surface((100, 100), pygame.SRCALPHA)
move_img1.fill((0, 0, 0, 0))
pygame.draw.circle(move_img1, (0, 255, 0, 128), (50, 50), 25)

while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for piece in symbols.pieces:
                if piece.tile.rect.collidepoint(mouse_pos):
                    for tile in basics.board:
                        tile.to_move = False
                    for tile in piece.where_move():
                        tile.to_move = True

    for tile in basics.board:
        screen.blit(tile.image, tile.rect)

    for piece in symbols.pieces:
        if not piece.is_dead:
            screen.blit(piece.image, piece.rect)

    for tile in basics.board:
        if tile.to_move:
            screen.blit(move_img1, tile.rect.topleft)

    pygame.display.update()
    clock.tick(60)
