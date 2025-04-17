import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Set up display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(GRID_COUNT//2, GRID_COUNT//2)]
        self.direction = (1, 0)
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            
        self.body.insert(0, new_head)

    def check_collision(self):
        head = self.body[0]
        # Check wall collision
        if (head[0] < 0 or head[0] >= GRID_COUNT or 
            head[1] < 0 or head[1] >= GRID_COUNT):
            return True
        
        # Check self collision
        if head in self.body[1:]:
            return True
        
        return False

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = self.spawn_food()
        self.score = 0

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_COUNT-1), 
                   random.randint(0, GRID_COUNT-1))
            if food not in self.snake.body:
                return food

    def update(self):
        self.snake.move()
        
        if self.snake.check_collision():
            return False

        if self.snake.body[0] == self.food:
            self.snake.grow = True
            self.food = self.spawn_food()
            self.score += 1

        return True

    def draw(self):
        screen.fill(BLACK)
        
        # Draw snake
        for segment in self.snake.body:
            pygame.draw.rect(screen, GREEN, 
                           (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE,
                            GRID_SIZE-1, GRID_SIZE-1))
        
        # Draw food
        pygame.draw.rect(screen, RED,
                        (self.food[0]*GRID_SIZE, self.food[1]*GRID_SIZE,
                         GRID_SIZE-1, GRID_SIZE-1))
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

def main():
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.snake.direction != (0, 1):
                    game.snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and game.snake.direction != (0, -1):
                    game.snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and game.snake.direction != (1, 0):
                    game.snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and game.snake.direction != (-1, 0):
                    game.snake.direction = (1, 0)

        if not game.update():
            print(f"Game Over! Final Score: {game.score}")
            running = False
            
        game.draw()
        clock.tick(10)  # Control game speed

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
