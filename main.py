import pygame
from random import randint
pygame.init()

CLOCK = pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 720, 720
SCREEN = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption('PySnake')

UNIT = 40
STARTING_SPEED = 2
SPEED_DELTA = 1

class Game():
    def __init__(self):
        self.speed = STARTING_SPEED
        self.wall = True
        
    def increase_speed(self):
        self.speed += SPEED_DELTA
    

class Snake(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([UNIT, UNIT])
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        
        self.x = 2
        self.y = 0
        
        self.prev_x = 0
        self.prev_y = 0
        
        self.direction = (1, 0)
        self.state = "moveright"
        
        self.body = [Tail(1,0),Tail(0,0)]
        
    def draw(self):
        SCREEN.blit(self.image, (self.x*UNIT, self.y*UNIT))
        for tail in self.body:
            tail.draw()
            
    def change_dirct(self, dirct):
        if dirct == "up" and self.state != "movedown":
            self.direction = (0, -1)
            self.state = "moveup"
        elif dirct == "down" and self.state != "moveup":
            self.direction = (0, 1)
            self.state = "movedown"
        elif dirct == "left" and self.state != "moveright":
            self.direction = (-1, 0)
            self.state = "moveleft"
        elif dirct == "right" and self.state != "moveleft":
            self.direction = (1, 0)
            self.state = "moveright"
                
    def move(self):
        self.prev_x = self.x
        self.prev_y = self.y
        
        self.x += self.direction[0]
        self.y += self.direction[1]
        
        prev = (self.prev_x, self.prev_y)
        for tail in self.body:
            prev = tail.move(prev)
            
    def ate(self):
        self.body.append(Tail(self.body[-1].prev_x, self.body[-1].prev_x,))
            
        
class Tail(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([UNIT, UNIT])
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        
        self.prev_x = 0
        self.prev_y = 0
    
    def draw(self):
        SCREEN.blit(self.image, (self.x*UNIT, self.y*UNIT))
        
    def move(self, where):
        self.prev_x = self.x
        self.prev_y = self.y
        
        self.x, self.y = where
        return (self.prev_x,self.prev_y)
        
    
class Point(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([UNIT, UNIT])
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        
        self.x = 4
        self.y = 5
        
    def draw(self):
        SCREEN.blit(self.image, (self.x*UNIT, self.y*UNIT))
        
    def eaten(self):
        self.x = randint (0, SCREEN_WIDTH/UNIT)
        self.y = randint (0, SCREEN_HEIGHT/UNIT)


def main():
    game = Game()
    snake = Snake()
    point = Point()
    background = pygame.Surface(SCREEN.get_size())
    background = background.convert()
    background.fill((0,0,0))
    while True:
        CLOCK.tick(game.speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.change_dirct("right")
                elif event.key == pygame.K_LEFT:
                    snake.change_dirct("left")
                elif event.key == pygame.K_UP:
                    snake.change_dirct("up")
                elif event.key == pygame.K_DOWN:
                    snake.change_dirct("down")

        SCREEN.blit(background, (0, 0))
        snake.move()
        
        #wall collide
        if game.wall:
            if snake.x < 0 or snake.y < 0:
                pygame.quit()
                exit()
          
        #tail collide - not working  
        if pygame.Rect.collidelist(snake.rect, snake.body):
            pass
        
        #fruit cllide
        if snake.x == point.x and snake.y == point.y:
            snake.ate()
            point.eaten()
            
        snake.draw()
        point.draw()


        pygame.display.update()


if __name__ == "__main__":
    main()
