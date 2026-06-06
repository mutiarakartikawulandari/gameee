import pygame
import sys


# 1. Struktur Node dan Linked List
class Node:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.next = None

class LinkedList:
    def __init__(self, x, y):
        self.head = Node(x, y)

    def set_pos(self, x, y):
        self.head.x, self.head.y = x, y

# 2. Pengaturan Arena & Game
pygame.init()
TILE_SIZE = 30
MAZE = [
    "####################",
    "#........##........#",
    "#.##.###.##.###.##.#",
    "#..................#",
    "#.##.#.######.#.##.#",
    "#....#...##...#....#",
    "####.###.##.###.####",
    "#........##........#",
    "#.######.##.######.#",
    "#..................#",
     "####################"
]
# ubah maze ke list  agar dot bisa di hapus
grid=[list(row) for row in MAZE]

WIDTH = len(MAZE[0]) * TILE_SIZE
HEIGHT = len(MAZE) * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Maze Linked List")

# Warna
YELLOW, RED, BLUE, BLACK, WHITE = (255, 255, 0), (255, 0, 0), (0, 0, 255), (0, 0, 0), (255, 255, 255)

# Inisialisasi Karakter (Menggunakan Linked List)
pacman = LinkedList(TILE_SIZE * 1, TILE_SIZE * 1)
ghost = LinkedList(TILE_SIZE * 18, TILE_SIZE * 9)

def can_move(x, y):
    grid_x, grid_y = int(x // TILE_SIZE), int(y // TILE_SIZE)
    if 0 <= grid_y < len(MAZE) and 0 <= grid_x < len(MAZE[0]):
        return MAZE[grid_y][grid_x] != "#"
    return False

clock = pygame.time.Clock() 
p_dir = [0, 0]

# 3. Main Loop
while True:
    screen.fill(BLACK)
    
    # Render Labirin
    for row_idx, row in enumerate(MAZE):
        for col_idx, cell in enumerate(row):
            if cell == "#":
                pygame.draw.rect(screen, BLUE, (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
            elif cell == ".":
                pygame.draw.circle(screen, WHITE, (col_idx * TILE_SIZE + TILE_SIZE//2, row_idx * TILE_SIZE + TILE_SIZE//2), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: p_dir = [-2, 0]
            if event.key == pygame.K_RIGHT: p_dir = [2, 0]
            if event.key == pygame.K_UP: p_dir = [0, -2]
            if event.key == pygame.K_DOWN: p_dir = [0, 2]

    # Update Pac-Man (Check Dinding)
    next_px = pacman.head.x + p_dir[0]
    next_py = pacman.head.y + p_dir[1]
    if can_move(next_px, next_py) and can_move(next_px + TILE_SIZE - 5, next_py + TILE_SIZE - 5):
        pacman.set_pos(next_px, next_py)

    # Pergerakan Musuh (Ghost AI Sederhana)
    gx, gy = ghost.head.x, ghost.head.y
    if gx < pacman.head.x: gx += 1
    elif gx > pacman.head.x: gx -= 1
    if gy < pacman.head.y: gy += 1
    elif gy > pacman.head.y: gy -= 1
    
    if can_move(gx, gy):
        ghost.set_pos(gx, gy)

    # Gambar Karakter
    pygame.draw.circle(screen, YELLOW, (int(pacman.head.x + TILE_SIZE//2), int(pacman.head.y + TILE_SIZE//2)), TILE_SIZE//2 - 2)
    pygame.draw.rect(screen, RED, (ghost.head.x + 2, ghost.head.y + 2, TILE_SIZE - 4, TILE_SIZE - 4))

    # Cek Tabrakan (Game Over)
    if abs(pacman.head.x - ghost.head.x) < 20 and abs(pacman.head.y - ghost.head.y) < 20:
        print("Game Over! Kamu tertangkap Ghost.")
        pygame.quit(); sys.exit()

    pygame.display.flip()
    clock.tick(60)
