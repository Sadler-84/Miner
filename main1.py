import pygame
import random


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[-1] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size

        if 0 <= cell_x < self.width and 0 <= cell_y < self.height:
            return cell_x, cell_y
        else:
            return None

    def on_click(self, cell_coords):
        x, y = cell_coords
        if self.board[y][x] != 10:
            summ = 0
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if 0 <= i < self.height and 0 <= j < self.width:
                        if self.board[i][j] == 10:
                            summ += 1
            self.board[y][x] = summ

    def get_click(self, mouse_pos):
        cell_coords = self.get_cell(mouse_pos)
        if cell_coords:
            self.on_click(cell_coords)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    self.left + x * self.cell_size,
                    self.top + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)

                # Отрисовка мин
                if self.board[y][x] == 10:
                    mine_rect = pygame.Rect(
                        self.left + x * self.cell_size + 1,
                        self.top + y * self.cell_size + 1,
                        self.cell_size - 2,
                        self.cell_size - 2
                    )
                    pygame.draw.rect(screen, (255, 0, 0), mine_rect)
                # Отрисовка чисел (если клетка открыта и не мина)
                elif self.board[y][x] != -1:
                    font = pygame.font.Font(None, 36)
                    text_surface = font.render(str(self.board[y][x]), True, (255, 100, 100))
                    text_x = self.left + x * self.cell_size + (self.cell_size // 4)
                    text_y = self.top + y * self.cell_size + (self.cell_size // 4)
                    screen.blit(text_surface, (text_x, text_y))


class Minesweeper(Board):
    def __init__(self, width, height, mines):
        super().__init__(width, height)
        self.mines = mines
        self.make_random_mines()

    def make_random_mines(self):
        for i in range(self.mines):
            while True:
                random_y = random.randint(0, self.height - 1)
                random_x = random.randint(0, self.width - 1)

                if self.board[random_y][random_x] != 10:
                    self.board[random_y][random_x] = 10
                    break

    def open_cell(self, pos):
        cell_coords = self.get_cell(pos)
        if cell_coords:
            self.on_click(cell_coords)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 400))

    minesweeper = Minesweeper(5, 5, 5)
    minesweeper.set_view(25, 25, 70)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                minesweeper.open_cell(pos)

        screen.fill((0, 0, 0))
        minesweeper.render(screen)
        pygame.display.flip()

    pygame.quit()