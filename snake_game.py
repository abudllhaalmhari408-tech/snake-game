import pygame
import random
import sys

# تهيئة pygame
pygame.init()

# الألوان
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# حجم الشاشة
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20

# سرعة اللعبة
SPEED = 10

# إنشاء الشاشة
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("لعبة الثعبان 🐍")

# الساعة للتحكم بالسرعة
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (GRID_SIZE, 0)
        self.grow_pending = False

    def move(self):
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # التحقق من الاصطدام بالجدران
        if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or
            new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT):
            return False

        # التحقق من الاصطدام بالنفس
        if new_head in self.positions:
            return False

        self.positions.insert(0, new_head)

        if not self.grow_pending:
            self.positions.pop()
        else:
            self.grow_pending = False

        return True

    def grow(self):
        self.grow_pending = True

    def draw(self, surface):
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, GREEN, rect)
            pygame.draw.rect(surface, WHITE, rect, 1)

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        return (x, y)

    def draw(self, surface):
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)

def main():
    snake = Snake()
    food = Food()
    score = 0
    font = pygame.font.Font(None, 36)
    running = True

    while running:
        clock.tick(SPEED)

        # معالجة الأحداث
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, GRID_SIZE):
                    snake.direction = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -GRID_SIZE):
                    snake.direction = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and snake.direction != (GRID_SIZE, 0):
                    snake.direction = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-GRID_SIZE, 0):
                    snake.direction = (GRID_SIZE, 0)

        # حركة الثعبان
        if not snake.move():
            print(f"انتهت اللعبة! النقاط النهائية: {score}")
            running = False
            break

        # التحقق من الاصطدام بالطعام
        if snake.positions[0] == food.position:
            snake.grow()
            food.position = food.random_position()
            score += 10

        # رسم اللعبة
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)

        # رسم النقاط
        score_text = font.render(f"النقاط: {score}", True, YELLOW)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
