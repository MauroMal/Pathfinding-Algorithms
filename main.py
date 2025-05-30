import pygame
import math, time
from queue import PriorityQueue
from collections import deque

pygame.init()
pygame.font.init()

WIDTH = 800
MENU_HEIGHT = 75
GRID_SIZE = WIDTH
WIN = pygame.display.set_mode((WIDTH, GRID_SIZE + MENU_HEIGHT))
pygame.display.set_caption("Pathfinder")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

BUTTON_WIDTH = 143
BUTTON_HEIGHT = 30

buttons = [
    {"label": "A Star", "x": 10, "y": 10, "width": BUTTON_WIDTH, "height": BUTTON_HEIGHT},
    {"label": "Dijkstra", "x": 170, "y": 10, "width": BUTTON_WIDTH, "height": BUTTON_HEIGHT},
    {"label": "BFS", "x": 330, "y": 10, "width": BUTTON_WIDTH, "height": BUTTON_HEIGHT},
    {"label": "Bellman-Ford", "x": 490, "y": 10, "width": BUTTON_WIDTH, "height": BUTTON_HEIGHT},
    {"label": "Reset", "x": 650, "y": 10, "width": BUTTON_WIDTH, "height": BUTTON_HEIGHT, "color": RED}
]

def draw_menu_bar(win):
    pygame.draw.rect(win, "#D9E8EA", (0, 0, WIDTH, MENU_HEIGHT))
    font = pygame.font.SysFont(None, 25)

    for button in buttons:
        button_color = button.get("color", WHITE)
        pygame.draw.rect(win, button_color, (button["x"], button["y"], button["width"], button["height"]), border_radius=10)
        
        text = font.render(button["label"], True, BLACK)
        text_rect = text.get_rect(center=(button["x"] + button["width"] // 2, button["y"] + button["height"] // 2))
        win.blit(text, text_rect)
    
    instructions = "Left Click: Set Start/End & Barriers    |    Right Click: Remove    |    Shift+Click: Add Weight"
    instructions_font = pygame.font.SysFont(None, 25)
    instructions_text = instructions_font.render(instructions, True, BLACK)
    win.blit(instructions_text, (30, 50))

def button_clicked(pos):
    x, y = pos
    if y > MENU_HEIGHT:
        return None
    for button in buttons:
        if button["x"] <= x <= button["x"] + button["width"] and button["y"] <= y <= button["y"] + button["height"]:
            return button["label"]
    return None

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = MENU_HEIGHT + col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.weight = 1

    def get_pos(self):
        return self.row, self.col 
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK
        self.weight = float('inf')

    def make_weighted(self, weight):
        self.color = YELLOW
        self.weight = weight

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
    
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def A_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + neighbor.weight

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()

        if current != start and current !=end:
            current.make_closed()

    return None

def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + neighbor.weight

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))  # Priority based only on g_score
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start and current != end:
            current.make_closed()

    return None

def bfs(draw, grid, start, end):
    queue = deque()  # FIFO queue
    queue.append(start)
    came_from = {}
    visited = {spot: False for row in grid for spot in row}
    visited[start] = True

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.popleft()  # Remove the first element (FIFO)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if not visited[neighbor]:
                came_from[neighbor] = current
                queue.append(neighbor)
                visited[neighbor] = True
                neighbor.make_open()

        draw()

        if current != start and current != end:
            current.make_closed()

    return None

import time

import time

def bellman_ford(draw, grid, start, end):

    # Update all neighbors before starting the algorithm
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)

    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    for _ in range(len(grid) * len(grid[0]) - 1):  # Relax edges |V| - 1 times
        changed = False  

        for row in grid:
            for spot in row:
                if g_score[spot] == float("inf"):  # Ignore unvisited nodes
                    continue

                for neighbor in spot.neighbors:  # Use precomputed neighbors
                    temp_g_score = g_score[spot] + neighbor.weight

                    if temp_g_score < g_score[neighbor]:  # Relaxation step
                        g_score[neighbor] = temp_g_score
                        came_from[neighbor] = spot
                        neighbor.color = GREEN  # Show updating nodes
                        changed = True

        draw()  
        time.sleep(0.065)  

        for row in grid:
            for spot in row:
                if spot.color == GREEN and spot != start and spot != end:
                    spot.make_closed()  # Mark finalized nodes as closed

        if not changed:  # Stop early if no updates
            break

    # Check for negative cycles
    for row in grid:
        for spot in row:
            for neighbor in spot.neighbors:  
                if g_score[spot] + neighbor.weight < g_score[neighbor]:  
                    print("Negative cycle detected! Bellman-Ford cannot work.")
                    return None

    # Reconstruct path if the end was reached
    if end in came_from:
        reconstruct_path(came_from, end, draw)
        start.make_start()
        end.make_end()
        return True

    return None  # No path found

def reset_scan(grid):
    for row in grid:
        for spot in row:
            if not spot.is_start() and not spot.is_end() and not spot.is_barrier():
                if spot.weight > 1:  
                    spot.color = YELLOW
                else:
                    spot.reset()

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, MENU_HEIGHT + i * gap), (width, MENU_HEIGHT + i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, MENU_HEIGHT), (j * gap, MENU_HEIGHT + width))
            
def draw(win, grid, rows, width):
    win.fill(WHITE)
    draw_menu_bar(win) #DRAW MENU

    for row in grid:
            for spot in row:
                spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    y, x  = pos
    if x < MENU_HEIGHT:
        return None
    x -= MENU_HEIGHT

    gap = width // rows
    ## y, x = pos
    row = y // gap
    col = x // gap
    
    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    
    start = None
    end = None
    run = True

    while run:
        draw(win, grid, ROWS, width)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]: #LEFT
                pos = pygame.mouse.get_pos()
                clicked = get_clicked_pos(pos, ROWS, width)
                if clicked:
                    row, col = clicked
                    spot = grid[row][col]

                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:  # Check Shift key
                        if not spot.is_start() and not spot.is_end():
                            spot.make_weighted(10)

                    elif not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                    
                    elif spot != end and spot != start:
                        spot.make_barrier()
                        
            elif pygame.key.get_mods() & pygame.KMOD_SHIFT and pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                clicked = get_clicked_pos(pos, ROWS, width)
                if clicked:
                    row, col = clicked
                    spot = grid[row][col]
                    if not spot.is_start() and not spot.is_end():
                        spot.make_weighted(5)

            elif pygame.mouse.get_pressed()[2]: #RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()

                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            ##if event.type == pygame.KEYDOWN:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                button_label = button_clicked(pos)
                ##if event.key == pygame.K_SPACE and start and end:
                if button_label == "A Star" and start and end:
                    reset_scan(grid)
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    A_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
            
                elif button_label == "Dijkstra" and start and end:
                    reset_scan(grid)
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

                elif button_label == "BFS" and start and end:
                    reset_scan(grid)
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                elif button_label == "Bellman-Ford" and start and end:
                    reset_scan(grid)
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    bellman_ford(lambda: draw(win, grid, ROWS, width), grid, start, end)

                elif button_label == "Reset":
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

            pygame.display.update()

    pygame.quit()

main(WIN, WIDTH)