from ast import match_case
from email.mime import image
import pygame
import sys
import os


pygame.init()
CLOCK = pygame.time.Clock()
W_WIDTH, W_HEIGHT = 720, 720
SNAKE_STEP = 60
B_WIDTH, B_HEIGHT = 600, 600
B_RECT = (SNAKE_STEP, SNAKE_STEP)

WIN = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
pygame.display.set_caption("Snake")
BOARD = pygame.Surface((W_WIDTH - SNAKE_STEP, W_HEIGHT - SNAKE_STEP))

FPS = 60

snake_head = pygame.image.load("assets/snake_head.png").convert_alpha()
snake_body = pygame.image.load("assets/snake_segment.png").convert_alpha()


def drawBoard():
    BOARD.fill((0, 0, 0))
    for i in range(0, B_HEIGHT, SNAKE_STEP):
        for j in range(0, B_WIDTH, SNAKE_STEP):
            pygame.draw.rect(BOARD, (80, 80, 80), ((i, j), B_RECT), 1)


def rotate_head(snake_head, direction, snake_rot):
    match direction, snake_rot:
        case "up":
            match snake_rot:
                case "right":
                    snake_head = pygame.transform.rotate(snake_head, 270)
                case "down":
                    snake_head = pygame.transform.rotate(snake_head, 90)
                case "left":
                    snake_head = pygame.transform.rotate(snake_head, 180)
                case other:
                    pass
        case other:
            pass
    return snake_head


def round_xy(snake_x, snake_y):
    snake_y = int(SNAKE_STEP * round(snake_y / float(SNAKE_STEP)))
    snake_x = int(SNAKE_STEP * round(snake_x / float(SNAKE_STEP)))
    return (snake_x, snake_y)


def main():
    snake_head = pygame.image.load("assets/snake_head.png").convert_alpha()
    snake_body = pygame.image.load("assets/snake_segment.png").convert_alpha()
    snake_x = 60
    snake_y = 0
    snake_rot = "right"
    pase = 1
    mode = "game"
    mov = (0, 0)
    body_prev = [[0, 0]]
    snake_len = 1

    while True:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if mode == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        mov = (0, 1)
                        # if snake_rot in ["up", "down"]:
                        # snake_x, snake_y = round_xy(snake_x, snake_y)
                        # snake_head = rotate_head(snake_head, "up", snake_rot)
                        snake_rot = "right"
                    elif event.key == pygame.K_LEFT:
                        mov = (0, -1)
                        snake_rot = "left"
                    elif event.key == pygame.K_UP:
                        mov = (-1, 0)
                        snake_rot = "up"
                    elif event.key == pygame.K_DOWN:
                        mov = (1, 0)
                        snake_rot = "down"

        if mode == "game":

            # body_prev.append([snake_x, snake_y])
            if len(body_prev) > snake_len:
                body_prev.pop(0)
            snake_x = snake_x + (pase * mov[1])
            snake_y = snake_y + (pase * mov[0])
            for ele in body_prev:
                ele[0] += pase * mov[1]
                ele[1] += pase * mov[0]

            drawBoard()
            for el in body_prev:
                BOARD.blit(snake_body, el)
            BOARD.blit(snake_head, (snake_x, snake_y))
            WIN.blit(BOARD, (SNAKE_STEP, SNAKE_STEP))

        pygame.display.update()


if __name__ == "__main__":
    main()
