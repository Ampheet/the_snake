from random import choice, randint
import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


class Apple:
    """Класс для отображения и управления яблоком"""

    def __init__(self, position):
        self.position = position
        self.color = APPLE_COLOR

    def draw(self, surface):
        """Отображение яблока на игровом поле"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake:
    """Класс для отображения и управления змейкой"""

    def __init__(self, position):
        self.positions = [position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.color = SNAKE_COLOR
        self.last = None

    def draw(self, surface):
        """Отображение змейки на игровом поле"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                (position[0], position[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновление направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def check_collision(self):
        """Проверка столкновения с самой собой"""
        return len(self.positions) != len(set(self.positions))


class Game:
    """Класс для управления основной логикой игры"""

    def __init__(self):
        self.snake = Snake((GRID_WIDTH // 2 * GRID_SIZE, 
                            GRID_HEIGHT // 2 * GRID_SIZE))
        self.apple = Apple((randint(0, GRID_WIDTH - 1) * GRID_SIZE, 
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE))

    def handle_keys(self):
        """Обработка пользовательского ввода"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != DOWN:
                    self.snake.next_direction = UP
                elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                    self.snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                    self.snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                    self.snake.next_direction = RIGHT

    def update(self):
        """Обновление состояния игры"""
        self.snake.update_direction()
        self.snake.last = self.snake.positions[-1]
        for i in range(len(self.snake.positions) - 1, 0, -1):
            self.snake.positions[i] = self.snake.positions[i - 1][:]
        if self.snake.direction == UP:
            self.snake.positions[0] = (self.snake.positions[0][0],
            (self.snake.positions[0][1] - GRID_SIZE) % SCREEN_HEIGHT)
        elif self.snake.direction == DOWN:
            self.snake.positions[0] = (self.snake.positions[0][0],
            (self.snake.positions[0][1] + GRID_SIZE) % SCREEN_HEIGHT)
        elif self.snake.direction == LEFT:
            self.snake.positions[0] = ((self.snake.positions[0][0] - GRID_SIZE) % SCREEN_WIDTH,
                                        self.snake.positions[0][1])
        elif self.snake.direction == RIGHT:
            self.snake.positions[0] = ((self.snake.positions[0][0] + GRID_SIZE) % SCREEN_WIDTH,
                                        self.snake.positions[0][1])

        if self.snake.check_collision():
            pygame.quit()
            raise SystemExit

        if self.snake.positions[0] == self.apple.position:
            self.snake.positions.append(self.snake.last)
            self.apple.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                                    randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        """Отображение игрового состояния на экране"""
        surface.fill(BOARD_BACKGROUND_COLOR)
        self.snake.draw(surface)
        self.apple.draw(surface)
        pygame.display.update()


def main():
    """Основная функция игры"""
    game = Game()
    while True:
        clock.tick(SPEED)
        game.handle_keys()
        game.update()
        game.draw(screen)


if __name__ == '__main__':
    main()
