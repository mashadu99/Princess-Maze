# C:\Users\User\Desktop\maze_game\grid_visualizer.py
import pygame
import os

class GridVisualizer:
    """
    מחלקה האחראית על כל הויזואליזציה של המשחק.
    טוענת את התמונות ומציירת את המפה, השחקנים והממשק.
    """
    def __init__(self, tile_size):
        self.tile_size = tile_size
        self.images = self._load_images()
        try:
            self.font = pygame.font.Font(os.path.join('assets', 'fonts', 'PressStart2P-Regular.ttf'), 24)
            self.small_font = pygame.font.Font(os.path.join('assets', 'fonts', 'PressStart2P-Regular.ttf'), 14)
        except (pygame.error, FileNotFoundError):
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 22)

    def _create_mud_image(self, floor_image):
        """יוצר תמונת בוץ מתוך תמונת הרצפה"""
        mud_image = floor_image.copy()
        # הוספת צבע חום לבוץ
        mud_surface = pygame.Surface(mud_image.get_size(), pygame.SRCALPHA)
        mud_surface.fill((139, 69, 19, 100))  # צבע חום עם שקיפות
        mud_image.blit(mud_surface, (0, 0))
        return mud_image

    def _load_images(self):
        image_files = {
            'P': 'princess.png', 'D': 'dragon.png', 'W': 'tree_wall.png',
            'G': 'castle_gate.png', 'K': 'golden_key.png', 'I': 'ice_tile.png',
            'H': 'heart.png',  # לב נוסף
            '.': 'floor.png', 'HEART': 'heart.png', 'KEY_ICON': 'golden_key.png'
        }
        loaded_images = {}
        # שימוש בנתיב מוחלט כדי להבטיח טעינה נכונה של התמונות
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'images')
        
        for key, filename in image_files.items():
            try:
                img = pygame.image.load(os.path.join(path, filename)).convert_alpha()
                size = (self.tile_size // 2, self.tile_size // 2) if key in ['HEART', 'KEY_ICON'] else (self.tile_size, self.tile_size)
                loaded_images[key] = pygame.transform.scale(img, size)
            except pygame.error as e:
                print(f"Error loading image {filename}: {e}")
                loaded_images[key] = pygame.Surface((self.tile_size, self.tile_size))
        
        # יצירת תמונת בוץ מתוך תמונת הרצפה
        if '.' in loaded_images:
            loaded_images['B'] = self._create_mud_image(loaded_images['.'])
        
        return loaded_images

    def draw_grid(self, screen, grid):
        for y, row in enumerate(grid):
            for x, tile in enumerate(row):
                screen.blit(self.images['.'], (x * self.tile_size, y * self.tile_size))
                if tile != '.':
                    screen.blit(self.images.get(tile), (x * self.tile_size, y * self.tile_size))

    def draw_hud(self, screen, hearts, has_key, level, turn_count, grace_turns, dragon_state="waiting"):
        hud_rect = pygame.Rect(0, screen.get_height() - 60, screen.get_width(), 60)
        pygame.draw.rect(screen, (10, 20, 30), hud_rect)
        pygame.draw.line(screen, (200, 200, 200), (0, screen.get_height() - 60), (screen.get_width(), screen.get_height() - 60), 2)

        # הצגת לבבות
        for i in range(hearts):
            screen.blit(self.images['HEART'], (10 + i * (self.tile_size // 2 + 5), screen.get_height() - 45))
        
        # הצגת מפתח
        key_icon = self.images['KEY_ICON']
        key_icon.set_alpha(255 if has_key else 80)
        screen.blit(key_icon, (screen.get_width() - 50, screen.get_height() - 45))
        
        # הצגת מספר השלב
        level_text = self.font.render(f"Level: {level}", True, (255, 215, 0))
        screen.blit(level_text, level_text.get_rect(centerx=screen.get_width() // 2, y=screen.get_height() - 50))
        
        # הצגת מצב הדרקון
        if turn_count < grace_turns:
            info_text = self.small_font.render(f"Grace: {grace_turns - turn_count}", True, (0, 255, 150))
        else:
            info_text = self.small_font.render("Dragon is hunting!", True, (255, 50, 50))
        screen.blit(info_text, (120, screen.get_height() - 42))

    def draw_message(self, screen, text):
        if not text: return
        message_surface = self.font.render(text, True, (255, 255, 255))
        rect = message_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 100))
        bg_rect = rect.inflate(20, 20)
        pygame.draw.rect(screen, (50, 50, 80, 200), bg_rect, border_radius=10)
        screen.blit(message_surface, rect)
        
    def draw_game_over(self, screen, won):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        text, color = ("You Won!", (0, 255, 0)) if won else ("Game Over", (255, 0, 0))
            
        title = self.font.render(text, True, color)
        subtitle = self.small_font.render("Press 'R' to Restart", True, (255, 255, 255))
        
        screen.blit(title, title.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 30)))
        screen.blit(subtitle, subtitle.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 30)))