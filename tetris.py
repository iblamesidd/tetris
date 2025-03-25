import pygame
import random
pygame.init()

WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
COLUMNS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE

WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
COLORS = [
    (0, 255, 255),  # Cyan
    (0, 0, 255),  # Blue
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),  # Green
    (128, 0, 128),  # Purple
    (255, 0, 0)  # Red
]

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1],
     [0, 1, 0]],  # T
    [[1, 1, 0],
     [0, 1, 1]],  # Z
    [[0, 1, 1],
     [1, 1, 0]],  # S
    [[1, 1],
     [1, 1]],  # O
    [[1, 1, 1],
     [1, 0, 0]],  # L
    [[1, 1, 1],
     [0, 0, 1]]  # J
]

class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


def create_grid(locked_positions):
    grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
    for (x, y), color in locked_positions.items():
        grid[y][x] = color
    return grid


def draw_grid(screen, grid, score, current_piece):
    screen.fill(GRAY)
    for y in range(ROWS):
        for x in range(COLUMNS):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

    for y, row in enumerate(current_piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_piece.color, (
                (current_piece.x + x) * GRID_SIZE, (current_piece.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def is_valid_move(piece, grid):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x, new_y = piece.x + x, piece.y + y
                if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS or (new_y >= 0 and grid[new_y][new_x] is not None):
                    return False
    return True


def clear_rows(grid, locked):
    full_rows = [i for i, row in enumerate(grid) if None not in row]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [None] * COLUMNS)
        for x in range(COLUMNS):
            if (x, row) in locked:
                del locked[(x, row)]


    new_locked = {}
    for (x, y), color in locked.items():
        new_y = y
        while new_y + 1 < ROWS and (x, new_y + 1) not in locked:
            new_y += 1
        new_locked[(x, new_y)] = color
    return len(full_rows), new_locked


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    locked_positions = {}
    current_piece = Tetromino(COLUMNS // 2, 0, random.choice(SHAPES))
    running = True
    fall_time = 0
    fall_speed = 500
    fast_fall_speed = 50
    score = 0
    fast_fall = False

    while running:
        screen.fill(GRAY)
        grid = create_grid(locked_positions)
        draw_grid(screen, grid, score, current_piece)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not is_valid_move(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not is_valid_move(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    fast_fall = True
                elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    current_piece.rotate()
                    if not is_valid_move(current_piece, grid):
                        current_piece.rotate()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    fast_fall = False

        fall_time += clock.get_rawtime()
        if fall_time > (fast_fall_speed if fast_fall else fall_speed):
            current_piece.y += 1
            if not is_valid_move(current_piece, grid):
                current_piece.y -= 1
                for y, row in enumerate(current_piece.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            locked_positions[(current_piece.x + x, current_piece.y + y)] = current_piece.color
                cleared, locked_positions = clear_rows(grid, locked_positions)
                score += cleared * 10
                current_piece = Tetromino(COLUMNS // 2, 0, random.choice(SHAPES))
                if not is_valid_move(current_piece, grid):
                    running = False  # Game over
            fall_time = 0
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main()