import sys
import os
import pygame


def show_loss_screen(screen):
    pygame.display.set_caption("Maze Princess - You Lost")

    screen_width, screen_height = screen.get_size()

    background_image = pygame.image.load(os.path.join("assets", "images", "loss.png"))
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (80, 80, 80)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    title_font = pygame.font.SysFont("georgia", 60, bold=True)
    button_font = pygame.font.SysFont("georgia", 40)

    quit_button = pygame.Rect(screen_width // 2 - 100, 450, 200, 60)
    menu_button = pygame.Rect(screen_width // 2 - 100, 530, 200, 60)

    def draw_text_with_outline(text, font, x, y, text_color, outline_color, outline_size=2):
        base = font.render(text, True, text_color)
        for dx in [-outline_size, 0, outline_size]:
            for dy in [-outline_size, 0, outline_size]:
                if dx != 0 or dy != 0:
                    outline = font.render(text, True, outline_color)
                    screen.blit(outline, (x + dx, y + dy))
        screen.blit(base, (x, y))

    def draw_loss_screen():
        screen.blit(background_image, (0, 0))

        text = "YOU LOST"
        text_surface = title_font.render(text, True, WHITE)
        text_x = screen_width // 2 - text_surface.get_width() // 2
        text_y = 80
        draw_text_with_outline(text, title_font, text_x, text_y, WHITE, BLACK, outline_size=2)

        pygame.draw.rect(screen, LIGHT_GRAY, quit_button, border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, quit_button, width=2, border_radius=10)
        quit_text = button_font.render("Quit", True, BLACK)
        screen.blit(quit_text, (
            quit_button.x + (quit_button.width - quit_text.get_width()) // 2,
            quit_button.y + (quit_button.height - quit_text.get_height()) // 2
        ))

        pygame.draw.rect(screen, LIGHT_GRAY, menu_button, border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, menu_button, width=2, border_radius=10)
        menu_text = button_font.render("Main Menu", True, BLACK)
        screen.blit(menu_text, (
            menu_button.x + (menu_button.width - menu_text.get_width()) // 2,
            menu_button.y + (menu_button.height - menu_text.get_height()) // 2
        ))

        pygame.display.flip()

    while True:
        draw_loss_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif menu_button.collidepoint(event.pos):
                    from src.ui.start_screen import show_start_screen
                    show_start_screen(screen)
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_q]:
                    pygame.quit()
                    sys.exit()
