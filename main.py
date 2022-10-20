from cmath import rect
import pygame
from random import randint

pygame.init()
pygame.font.init()

HEAD_PIC = pygame.image.load("assets/snake_head.png")
BODY_PIC = pygame.image.load("assets/snake_segment.png")
FONT = pygame.font.SysFont("Comic Sans MS", 30)
CLOCK = pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 720, 720
SCREEN = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption("PySnake")

UNIT = 60
STARTING_SPEED = 2
SPEED_DELTA = 0.1


TAIL = pygame.transform.scale(BODY_PIC, (UNIT, UNIT))
HEAD_R = pygame.transform.scale(HEAD_PIC, (UNIT, UNIT))
HEAD_U = pygame.transform.rotate(HEAD_R, 90)
HEAD_L = pygame.transform.rotate(HEAD_R, 180)
HEAD_D = pygame.transform.rotate(HEAD_R, -90)

BACKGROUND = pygame.Surface(SCREEN.get_size())
BACKGROUND = BACKGROUND.convert()


class Game:
    def __init__(self):
        self.speed = STARTING_SPEED
        self.wall = True

    def increase_speed(self):
        self.speed += SPEED_DELTA


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = HEAD_R
        self.rect = self.image.get_rect()

        self.x = 2
        self.y = 0

        self.prev_x = 0
        self.prev_y = 0

        self.direction = (1, 0)
        self.state = "moveright"

        self.body = [Tail(1, 0), Tail(0, 0)]

    def draw(self):
        SCREEN.blit(self.image, (self.x * UNIT, self.y * UNIT))
        for tail in self.body:
            tail.draw()

    def change_dirct(self, dirct):
        if dirct == "up" and self.state != "movedown":
            self.direction = (0, -1)
            self.state = "moveup"
            self.image = HEAD_U
        elif dirct == "down" and self.state != "moveup":
            self.direction = (0, 1)
            self.state = "movedown"
            self.image = HEAD_D
        elif dirct == "left" and self.state != "moveright":
            self.direction = (-1, 0)
            self.state = "moveleft"
            self.image = HEAD_L
        elif dirct == "right" and self.state != "moveleft":
            self.direction = (1, 0)
            self.state = "moveright"
            self.image = HEAD_R

    def move(self):
        self.prev_x = self.x
        self.prev_y = self.y

        self.x += self.direction[0]
        self.y += self.direction[1]

        prev = (self.prev_x, self.prev_y)
        for tail in self.body:
            prev = tail.move(prev)

    def ate(self):
        self.body.append(Tail(self.prev_x, self.prev_y))

    def countPoints(self):
        return int(len(self.body)) - 2


class Tail(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = TAIL
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.prev_x = 0
        self.prev_y = 0

    def draw(self):
        SCREEN.blit(self.image, (self.x * UNIT, self.y * UNIT))

    def move(self, where):
        self.prev_x = self.x
        self.prev_y = self.y

        self.x, self.y = where
        return (self.prev_x, self.prev_y)


class Point(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([UNIT, UNIT])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

        self.x = 4
        self.y = 5

    def draw(self):
        SCREEN.blit(self.image, (self.x * UNIT, self.y * UNIT))

    def change_xy(self):
        self.x = randint(0, int(SCREEN_WIDTH / UNIT) - 1)
        self.y = randint(0, int(SCREEN_WIDTH / UNIT) - 1)


def draw_field():
    odd = False
    for u in range(0, SCREEN_HEIGHT, UNIT):
        odd = not odd
        for i in range(0, SCREEN_WIDTH, UNIT):
            if odd:
                pygame.draw.rect(BACKGROUND, (0, 150, 0), (i, u, UNIT, UNIT))
                odd = not odd
            else:
                pygame.draw.rect(BACKGROUND, (0, 200, 0), (i, u, UNIT, UNIT))
                odd = not odd


def main():
    game = Game()
    snake = Snake()
    point = Point()
    mode = "GAME"

    while True:
        if mode == "GAME":
            CLOCK.tick(game.speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        snake.change_dirct("right")
                        break
                    elif event.key == pygame.K_LEFT:
                        snake.change_dirct("left")
                        break
                    elif event.key == pygame.K_UP:
                        snake.change_dirct("up")
                        break
                    elif event.key == pygame.K_DOWN:
                        snake.change_dirct("down")
                        break

            draw_field()
            SCREEN.blit(BACKGROUND, (0, 0))
            snake.move()

            # wall collide
            if game.wall:
                if snake.x < 0 or snake.x > SCREEN_WIDTH / UNIT:
                    mode = "OVER"
                if snake.y < 0 or snake.y > SCREEN_HEIGHT / UNIT:
                    mode = "OVER"

            # fruit cllide
            if snake.x == point.x and snake.y == point.y:
                snake.ate()
                point.change_xy()
                game.increase_speed()

            # tail collide
            for t in snake.body:
                if snake.x == t.x and snake.y == t.y:
                    mode = "OVER"
                if point.x == t.x and point.y == t.y:
                    point.change_xy()

            point.draw()
            snake.draw()

        elif mode == "OVER":
            draw_field()
            text0 = FONT.render("GAME OVER", False, (220, 0, 0))
            text1 = FONT.render(
                f"your score is: {snake.countPoints()}", False, (220, 220, 220)
            )
            text2 = FONT.render("press space to play again", False, (100, 100, 100))
            # TODO: fix score number
            SCREEN.blit(text0, (SCREEN_WIDTH / 2 - 2 * UNIT, SCREEN_HEIGHT / 5 * 2))
            SCREEN.blit(text1, (SCREEN_WIDTH / 2 - 3 * UNIT, SCREEN_HEIGHT / 5 * 3))
            SCREEN.blit(text2, (SCREEN_WIDTH / 2 - 4 * UNIT, SCREEN_HEIGHT / 5 * 4))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main()

        pygame.display.update()


if __name__ == "__main__":
    main()
