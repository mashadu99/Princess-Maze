import pygame
import sys

FONT_PATH = "assets/fonts/SeraphsDEMO-CalligraphicRegular.otf"
IMAGE_PATH = "assets/images/won.png"

def render_text_with_outline(text, font, text_color, outline_color, outline_width):
    base = font.render(text, True, outline_color)
    text_surface = font.render(text, True, text_color)
    w, h = text_surface.get_size()

    outline_surface = pygame.Surface((w + 2 * outline_width, h + 2 * outline_width), pygame.SRCALPHA)

    # ציור טקסט outline מסביב
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                outline_surface.blit(base, (dx + outline_width, dy + outline_width))

    # ציור טקסט רגיל מעל
    outline_surface.blit(text_surface, (outline_width, outline_width))
    return outline_surface

def show_end_screen(screen):
    pygame.init()

    # טען רקע
    try:
        background = pygame.image.load(IMAGE_PATH).convert()
        background = pygame.transform.scale(background, screen.get_size())
    except:
        background = pygame.Surface(screen.get_size())
        background.fill((0, 0, 0))

    # טען פונט
    font = pygame.font.Font(FONT_PATH, 40)

    # יצירת כפתור
    button_rect = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 - 30, 200, 60)

    selected = True

    running = True
    while running:
        screen.blit(background, (0, 0))

        # צייר כפתור מעוגל
        pygame.draw.rect(screen, (200, 200, 200), button_rect, border_radius=20)

        # טקסט עם תוחם לבן
        text_surface = render_text_with_outline("Exit", font, (0, 0, 0), (255, 255, 255), 2)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and selected:
                    pygame.quit()
                    sys.exit()
