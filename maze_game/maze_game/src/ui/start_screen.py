import pygame
import sys

FONT_PATH = "assets/fonts/SeraphsDEMO-CalligraphicRegular.otf"
BACKGROUND_IMAGE_PATH = "assets/images/princess_load_screen.jpg"

def render_text_with_outline(text, font, text_color, outline_color, outline_width=2):
    base = font.render(text, True, text_color)
    size = (base.get_width() + 2 * outline_width, base.get_height() + 2 * outline_width)
    img = pygame.Surface(size, pygame.SRCALPHA)

    for dx in [-outline_width, 0, outline_width]:
        for dy in [-outline_width, 0, outline_width]:
            if dx != 0 or dy != 0:
                img.blit(font.render(text, True, outline_color), (dx + outline_width, dy + outline_width))

    img.blit(base, (outline_width, outline_width))
    return img

def show_start_screen(screen):
    pygame.init()
    background = pygame.image.load(BACKGROUND_IMAGE_PATH)
    background = pygame.transform.scale(background, screen.get_size())

    title_font = pygame.font.Font(FONT_PATH, 80)
    button_font = pygame.font.Font(FONT_PATH, 36)

    title_text = render_text_with_outline("Maze Princess", title_font, (255, 255, 255), (0, 0, 0), 2)
    start_text = render_text_with_outline("Start Game", button_font, (0, 0, 0), (255, 255, 255), 2)
    quit_text = render_text_with_outline("Quit", button_font, (0, 0, 0), (255, 255, 255), 2)

    start_button = pygame.Rect(300, 350, 200, 60)
    quit_button = pygame.Rect(300, 430, 200, 60)
    buttons = [start_button, quit_button]
    selected_index = 0

    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 40))

        for i, button in enumerate(buttons):
            color = (255, 215, 0) if i == selected_index else (200, 200, 200)
            pygame.draw.rect(screen, color, button, border_radius=12)

        # מרכוז מדויק של הטקסטים על הכפתורים
        start_text_rect = start_text.get_rect(center=(start_button.centerx, start_button.centery - 2))
        quit_text_rect = quit_text.get_rect(center=(quit_button.centerx, quit_button.centery - 2))

        screen.blit(start_text, start_text_rect)
        screen.blit(quit_text, quit_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected_index = (selected_index - 1) % len(buttons)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected_index = (selected_index + 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:
                        return
                    elif selected_index == 1:
                        pygame.quit()
                        sys.exit()
