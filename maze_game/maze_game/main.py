# C:\Users\User\Desktop\maze_game\main.py
import pygame
import sys
import time
from copy import deepcopy
from grid_visualizer import GridVisualizer
from src.pathfinding.astar import find_path

# הגדרות כלליות
TILE_SIZE = 48
GRACE_TURNS = 3
PLAYER_HEARTS = 3
DRAGON_THINK_TIME = 0.5 # שניות

LEVELS = [
    # שלב 1 - קטן ופשוט
    {"grid": [
        ['W','W','W','W','W','W','W','W','W','W'],
        ['W','P','.','.','.','.','.','K','.','W'],
        ['W','.','W','W','.','W','W','.','W','W'],
        ['W','.','.','.','.','.','.','.','.','W'],
        ['W','.','W','.','W','W','W','.','W','W'],
        ['W','.','.','.','.','.','.','.','.','W'],
        ['W','W','W','.','W','.','W','W','.','W'],
        ['W','.','.','.','.','D','.','.','.','W'],
        ['W','.','W','W','W','W','W','.','G','W'],
        ['W','W','W','W','W','W','W','W','W','W']
    ]},
    
    # שלב 2 - תוספת קרח ומפתח
    {"grid": [
        ['W','W','W','W','W','W','W','W','W','W','W','W'],
        ['W','P','.','.','W','.','.','I','.','.','K','W'],
        ['W','.','W','.','W','.','W','W','W','W','.','W'],
        ['W','D','.','.','.','.','.','.','.','W','.','W'],
        ['W','.','W','W','W','W','W','.','W','W','.','W'],
        ['W','.','.','.','.','.','.','.','.','.','.','W'],
        ['W','W','W','W','.','W','W','I','W','W','.','W'],
        ['W','.','.','.','.','.','.','.','.','.','.','W'],
        ['W','.','W','W','W','W','W','W','W','.','.','W'],
        ['W','.','.','.','.','.','.','.','.','.','.','W'],
        ['W','W','W','W','W','W','W','W','W','W','G','W']
    ]},
    
    # שלב 3 - גריד גדול עם בוץ, קרח, לב נוסף
    {"grid": [
        ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],
        ['W','P','.','.','W','.','.','I','.','.','K','.','.','H','W'],
        ['W','.','W','.','W','.','W','W','W','W','.','W','.','.','W'],
        ['W','D','.','.','.','.','.','.','.','W','.','W','.','.','W'],
        ['W','.','W','W','W','W','W','B','W','W','.','W','.','.','W'],
        ['W','.','.','B','.','.','.','.','.','.','.','W','.','.','W'],
        ['W','W','W','W','.','W','W','I','W','W','.','W','B','.','W'],
        ['W','.','.','.','B','.','.','.','.','.','.','W','.','.','W'],
        ['W','.','W','W','W','W','W','W','W','B','.','W','.','.','W'],
        ['W','.','.','.','.','.','B','.','.','.','.','W','.','.','W'],
        ['W','.','W','W','W','W','W','W','W','W','.','W','.','.','W'],
        ['W','.','.','.','B','.','.','.','.','.','.','W','.','.','W'],
        ['W','.','W','W','W','W','W','W','W','W','.','W','B','.','W'],
        ['W','.','.','.','.','.','.','B','.','.','.','W','.','.','W'],
        ['W','W','W','W','W','W','W','W','W','W','W','W','W','G','W']
    ]}
]

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.visualizer = GridVisualizer(TILE_SIZE)
        self.running = True
        self.clock = pygame.time.Clock()
        self.dragon_just_moved = False  # Flag to prevent double dragon turns
        self.player_slipped = False  # Flag to track if player slipped on ice
        self.reset_game()

    def reset_game(self, level_idx=0):
        self.game_state = 'playing'
        self.level_idx = level_idx
        self.turn_count = 0
        self.is_player_turn = True
        self.message, self.message_timer = "", 0
        self.setup_level()
        
    def setup_level(self):
        self.grid = deepcopy(LEVELS[self.level_idx]["grid"])
        self.player_pos = self._find_char('P')
        self.dragon_pos = self._find_char('D')
        self.start_pos = self.player_pos
        # שמירת מספר הלבבות הנוכחי (לא מאפס בכל שלב)
        if not hasattr(self, 'hearts'):
            self.hearts = PLAYER_HEARTS
        self.has_key = False
        self.set_message(f"Level {self.level_idx + 1}", 3)

    def _find_char(self, char):
        for y, r in enumerate(self.grid):
            if char in r: return (y, r.index(char))

    def set_message(self, text, duration):
        self.message = text
        self.message_timer = time.time() + duration

    def handle_input(self):
        if not self.is_player_turn:
            return  # Prevent input when it's not the player's turn
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN:
                if self.game_state != 'playing':
                    if event.key == pygame.K_r: self.reset_game(0 if self.game_state == 'win' else self.level_idx)
                elif self.is_player_turn and not self.player_slipped:  # Prevent movement if slipped
                    moves = {pygame.K_UP: (-1, 0), pygame.K_DOWN: (1, 0), pygame.K_LEFT: (0, -1), pygame.K_RIGHT: (0, 1)}
                    if event.key in moves: self.move_player(*moves[event.key])

    def move_player(self, dy, dx):
        py, px = self.player_pos
        ny, nx = py + dy, px + dx

        if not (0 <= ny < len(self.grid) and 0 <= nx < len(self.grid[0])) or self.grid[ny][nx] == 'W': return
            
        self.grid[py][px] = '.'
        target_tile = self.grid[ny][nx]

        if target_tile == 'K':
            self.has_key = True
            self.set_message("You found the key!", 2)
            self.player_pos = (ny, nx)
        elif target_tile == 'H':
            if self.hearts < PLAYER_HEARTS:
                self.hearts += 1
                self.set_message("Extra heart collected!", 2)
            else:
                self.set_message("You're already at full health!", 2)
            self.player_pos = (ny, nx)
        elif target_tile == 'G':
            if self.has_key:
                if self.level_idx + 1 < len(LEVELS):
                    self.level_idx += 1
                    self.setup_level()
                    self.set_message("Level Complete!", 2)
                else: 
                    self.game_state = 'win'
                return
            else:
                self.set_message("The gate is locked!", 2)
                self.grid[py][px] = 'P'; return
        elif target_tile == 'I':
            print(f"ICE: Slipping from {self.player_pos} back to {self.start_pos}")  # דיבאג
            self.set_message("Slipped on ice!", 2)
            self.player_pos = self.start_pos  # Return to start position
            print(f"ICE: Princess returned to start position: {self.player_pos}")  # דיבאג
        elif target_tile == 'B':
            print(f"MUD: Player stuck in mud at {(ny, nx)}")  # Debug
            self.set_message("Stuck in mud!", 1)
            self.grid[ny][nx] = '.'  # הבוץ נשבר והופך לרצפה רגילה
            self.grid[py][px] = 'P'  # משאירה את עצמה באותו מקום
            self.end_player_turn()
            return
        elif (ny, nx) == self.dragon_pos:
            self.handle_dragon_collision()
            self.grid[py][px] = 'P'; self.end_player_turn(); return
        else: self.player_pos = (ny, nx)

        self.grid[self.player_pos[0]][self.player_pos[1]] = 'P'
        self.end_player_turn()

    def handle_dragon_collision(self):
        self.hearts -= 1
        self.set_message("Ouch! A dragon hit you!", 2)
        if self.hearts <= 0: 
            self.game_state = 'lose'
        else:
            # איפוס השלב הנוכחי במקום כל המשחק
            self.setup_level()
            self.set_message(f"Level {self.level_idx + 1} restarted! Hearts remaining: {self.hearts}", 3)

    def end_player_turn(self):
        self.turn_count += 1
        self.is_player_turn = False
        self.player_slipped = False # Reset slipped flag when player ends turn
        self.dragon_just_moved = False  # Reset flag when player ends turn

    def dragon_turn(self):
        if self.turn_count < GRACE_TURNS:
            self.is_player_turn = True; return
        
        if self.dragon_just_moved:  # Prevent double dragon turns
            return

        time.sleep(DRAGON_THINK_TIME)
        dy, dx = self.dragon_pos
        self.grid[dy][dx] = '.'
        
        print(f"DRAGON: Planning path from {self.dragon_pos} to {self.player_pos}")  # Debug
        path = find_path(self.grid, self.dragon_pos, self.player_pos)
        print(f"Dragon path length: {len(path)}")  # Debug: show path length
        
        # Calculate total path cost for debugging
        if len(path) > 1:
            total_cost = 0
            for i in range(len(path) - 1):
                y, x = path[i + 1]
                tile = self.grid[y][x]
                cost = 1 if tile == '.' else (2 if tile == 'I' else 3 if tile == 'B' else 1)
                total_cost += cost
            print(f"Dragon path total cost: {total_cost}")
        
        if len(path) > 1: 
            self.dragon_pos = path[1]
        
        if self.dragon_pos == self.player_pos: self.handle_dragon_collision()
        
        dy, dx = self.dragon_pos
        self.grid[dy][dx] = 'D'
        self.dragon_just_moved = True  # Set flag to prevent double moves
        self.is_player_turn = True

    def run(self):
        while self.running:
            self.handle_input()
            if self.game_state == 'playing' and not self.is_player_turn: self.dragon_turn()
            if time.time() > self.message_timer: self.message = ""

            self.screen.fill((0, 0, 0))
            self.visualizer.draw_grid(self.screen, self.grid)
            self.visualizer.draw_hud(self.screen, self.hearts, self.has_key, self.level_idx + 1, self.turn_count, GRACE_TURNS)
            if self.message: self.visualizer.draw_message(self.screen, self.message)
            if self.game_state != 'playing': self.visualizer.draw_game_over(self.screen, self.game_state == 'win')
            pygame.display.flip()
            
            self.clock.tick(60)

if __name__ == '__main__':
    pygame.init()
    max_w = max(len(lvl["grid"][0]) for lvl in LEVELS)
    max_h = max(len(lvl["grid"]) for lvl in LEVELS)
    screen = pygame.display.set_mode((max_w * TILE_SIZE, max_h * TILE_SIZE + 60))
    pygame.display.set_caption("Princess Maze - A* Agent")
    
    Game(screen).run()
    
    pygame.quit()
    sys.exit()