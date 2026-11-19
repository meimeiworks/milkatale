import pygame
import sys
import os
from story import (
    BLACK, WHITE, ICE_BLUE, MOSS_GLOW,
    build_story, draw_dachshund, draw_story_illustration
)

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 500
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MilkaTale: Под-Эверест")
clock = pygame.time.Clock()

title_font = pygame.font.SysFont("Courier New", 42, bold=True)
menu_font = pygame.font.SysFont("Courier New", 26, bold=True)
story_font = pygame.font.SysFont("Courier New", 20, bold=True)
small_font = pygame.font.SysFont("Courier New", 17)

YELLOW = (255, 225, 60)

state = "MENU"
menu_options = ["НАЧАТЬ ИГРУ", "УПРАВЛЕНИЕ", "ВЫХОД"]
selected_menu = 0
show_controls = False

player_name = ""
confirm_choice = 0
story_slides = []
current_slide = 0
char_index = 0.0

player_rect = pygame.Rect(376, 305, 48, 28)
player_dir = "right"
dialog_text = ""

def draw_wrapped_text(surface, text, font_obj, color, rect):
    words = text.split(" ")
    lines = []
    line = ""
    for w in words:
        test = line + w + " "
        if font_obj.size(test)[0] <= rect.width:
            line = test
        else:
            lines.append(line)
            line = w + " "
    lines.append(line)

    y = rect.y
    for l in lines:
        surface.blit(font_obj.render(l, True, color), (rect.x, y))
        y += font_obj.get_height() + 8

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if state == "MENU":
                if show_controls:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE, pygame.K_z):
                        show_controls = False
                else:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected_menu = (selected_menu - 1) % 3
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected_menu = (selected_menu + 1) % 3
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_z):
                        if selected_menu == 0:
                            state = "NAME_INPUT"
                            player_name = ""
                        elif selected_menu == 1:
                            show_controls = True
                        elif selected_menu == 2:
                            pygame.quit()
                            sys.exit()

            elif state == "NAME_INPUT":
                if event.key == pygame.K_RETURN:
                    if not player_name.strip():
                        player_name = "Милка"
                    state = "CONFIRM_NAME"
                    confirm_choice = 0
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    state = "MENU"
                elif len(player_name) < 12 and event.unicode.isprintable():
                    player_name += event.unicode

            elif state == "CONFIRM_NAME":
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                    confirm_choice = 1 - confirm_choice
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_z):
                    if confirm_choice == 0:
                        story_slides = build_story(player_name.strip())
                        current_slide = 0
                        char_index = 0.0
                        state = "STORY"
                    else:
                        state = "NAME_INPUT"

            elif state == "STORY":
                full_text = story_slides[current_slide]["text"]
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_z):
                    if int(char_index) < len(full_text):
                        char_index = float(len(full_text))
                    else:
                        current_slide += 1
                        char_index = 0.0
                        if current_slide >= len(story_slides):
                            state = "GAME"
                            dialog_text = f"* {player_name} очнулся на дне Под-Эвереста. Пора искать путь наверх!"

            elif state == "GAME":
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_z):
                    if dialog_text:
                        dialog_text = ""
                    elif player_rect.colliderect(pygame.Rect(350, 130, 100, 80)):
                        dialog_text = f"* Ледяной камень гласит: «Впереди пещеры Под-Эвереста». ({player_name} полон решимости!)"

    screen.fill(BLACK)

    if state == "MENU":
        for i in range(25):
            sx = (i * 73 + pygame.time.get_ticks() // 40) % WIDTH
            sy = (i * 41 + pygame.time.get_ticks() // 25) % HEIGHT
            pygame.draw.circle(screen, ICE_BLUE, (sx, sy), 2)

        t1 = title_font.render("ПОД-ЭВЕРЕСТ", True, WHITE)
        t2 = small_font.render("MilkaTale: История путешественника", True, ICE_BLUE)
        screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 65))
        screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 120))
        draw_dachshund(screen, WIDTH // 2 - 24, 180, "right", 1.1)

        if show_controls:
            pygame.draw.rect(screen, WHITE, (140, 240, 520, 175), 3)
            screen.blit(story_font.render("Стрелки / WASD — движение", True, WHITE), (165, 265))
            screen.blit(story_font.render("Enter / Пробел / Z — действие", True, WHITE), (165, 305))
            screen.blit(small_font.render("Нажмите Enter, чтобы вернуться", True, YELLOW), (165, 365))
        else:
            for idx, opt in enumerate(menu_options):
                col = YELLOW if idx == selected_menu else WHITE
                pref = "> " if idx == selected_menu else "  "
                screen.blit(menu_font.render(pref + opt, True, col), (WIDTH // 2 - 140, 265 + idx * 50))

    elif state == "NAME_INPUT":
        p1 = menu_font.render("Назовите таксу-путешественника:", True, WHITE)
        p2 = small_font.render("(Введите имя и нажмите Enter)", True, ICE_BLUE)
        screen.blit(p1, (WIDTH // 2 - p1.get_width() // 2, 110))
        screen.blit(p2, (WIDTH // 2 - p2.get_width() // 2, 155))

        box = pygame.Rect(WIDTH // 2 - 180, 215, 360, 55)
        pygame.draw.rect(screen, WHITE, box, 3)
        cur = "_" if (pygame.time.get_ticks() // 400) % 2 == 0 else ""
        screen.blit(title_font.render(player_name + cur, True, YELLOW), (box.x + 20, box.y + 6))

        tip = small_font.render("Если оставить пустым, героя назовут Милка", True, (150, 150, 170))
        screen.blit(tip, (WIDTH // 2 - tip.get_width() // 2, 305))

    elif state == "CONFIRM_NAME":
        q1 = menu_font.render(f"Выбрано имя: {player_name}", True, YELLOW)
        q2 = story_font.render("Отправиться в путь с этим именем?", True, WHITE)
        screen.blit(q1, (WIDTH // 2 - q1.get_width() // 2, 135))
        screen.blit(q2, (WIDTH // 2 - q2.get_width() // 2, 190))

        screen.blit(menu_font.render(("> ДА" if confirm_choice == 0 else "  ДА"), True, YELLOW if confirm_choice == 0 else WHITE), (WIDTH // 2 - 170, 270))
        screen.blit(menu_font.render(("> ИЗМЕНИТЬ" if confirm_choice == 1 else "  ИЗМЕНИТЬ"), True, YELLOW if confirm_choice == 1 else WHITE), (WIDTH // 2 + 10, 270))

    elif state == "STORY":
        slide = story_slides[current_slide]
        draw_story_illustration(screen, slide["scene"])
        pygame.draw.rect(screen, BLACK, (60, 295, 680, 150))
        pygame.draw.rect(screen, WHITE, (60, 295, 680, 150), 4)

        if char_index < len(slide["text"]):
            char_index += 0.65

        draw_wrapped_text(screen, slide["text"][:int(char_index)], story_font, WHITE, pygame.Rect(85, 315, 630, 115))
        hint = small_font.render("[Enter / Пробел — далее]", True, YELLOW)
        screen.blit(hint, (WIDTH - hint.get_width() - 75, 458))

    elif state == "GAME":
        if not dialog_text:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_rect.x -= 4
                player_dir = "left"
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_rect.x += 4
                player_dir = "right"
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player_rect.y -= 4
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player_rect.y += 4
            player_rect.clamp_ip(pygame.Rect(80, 110, 640, 320))

        pygame.draw.rect(screen, (20, 25, 45), (70, 100, 660, 340))
        pygame.draw.rect(screen, ICE_BLUE, (70, 100, 660, 340), 4)
        pygame.draw.ellipse(screen, MOSS_GLOW, (320, 285, 160, 65))
        pygame.draw.polygon(screen, ICE_BLUE, [(400, 130), (380, 175), (420, 175)])
        draw_dachshund(screen, player_rect.x, player_rect.y, player_dir, 1.0)

        hud = small_font.render(f"ГЕРОЙ: {player_name}   |   ЛОКАЦИЯ: ДНО ПОД-ЭВЕРЕСТА", True, WHITE)
        screen.blit(hud, (70, 65))

        if dialog_text:
            pygame.draw.rect(screen, BLACK, (60, 330, 680, 135))
            pygame.draw.rect(screen, WHITE, (60, 330, 680, 135), 4)
            draw_wrapped_text(screen, dialog_text, story_font, WHITE, pygame.Rect(85, 350, 630, 100))

    pygame.display.flip()
    clock.tick(FPS)
