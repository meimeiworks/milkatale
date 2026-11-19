import pygame
import sys
from story import BLACK, WHITE, ICE_BLUE, build_story, draw_dachshund, draw_story_illustration
from battle import BattleSystem

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 500
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MilkaTale: Снежные холмы")
clock = pygame.time.Clock()

title_font = pygame.font.SysFont("Courier New", 42, bold=True)
menu_font = pygame.font.SysFont("Courier New", 24, bold=True)
story_font = pygame.font.SysFont("Courier New", 19, bold=True)
small_font = pygame.font.SysFont("Courier New", 15, bold=True)

YELLOW = (255, 225, 60)
SNOW_GROUND = (220, 238, 255)
SNOW_SHADOW = (175, 205, 235)

state = "MENU"
menu_options = ["НАЧАТЬ ИГРУ", "УПРАВЛЕНИЕ", "ВЫХОД"]
selected_menu = 0
show_controls = False

player_name = ""
confirm_choice = 0
story_slides = []
current_slide = 0
char_index = 0.0

stats = {
    "lv": 1, "exp": 0, "hp": 20, "max_hp": 20,
    "leopard_kills": 0, "pug_kills": 0, "spares": 0, "tea": 3
}
battle = BattleSystem()

zone = 1
player_rect = pygame.Rect(110, 270, 48, 28)
player_dir = "right"
meimei_x, meimei_y = 220, 220
dialog_text = ""
step_counter = 0
zone2_intro_done = False

def get_route_name():
    total = stats["leopard_kills"] + stats["pug_kills"]
    if total == 0:
        return "ПАЦИФИСТ"
    if stats["leopard_kills"] >= 10 and stats["pug_kills"] >= 5:
        return "ГЕНОЦИД"
    return "НЕЙТРАЛ"

def draw_meimei(surface, x, y):
    pygame.draw.ellipse(surface, (230, 240, 255), (x, y + 10, 52, 26))
    pygame.draw.circle(surface, (230, 240, 255), (x + 46, y + 8), 14)
    pygame.draw.polygon(surface, (190, 205, 225), [(x + 36, y - 3), (x + 40, y - 14), (x + 45, y - 3)])
    pygame.draw.polygon(surface, (190, 205, 225), [(x + 47, y - 3), (x + 52, y - 14), (x + 56, y - 3)])
    pygame.draw.rect(surface, (145, 75, 210), (x + 30, y + 14, 18, 8), border_radius=3)
    pygame.draw.circle(surface, (90, 190, 255), (x + 50, y + 6), 3)

def draw_wrapped_text(surface, text, font_obj, color, rect):
    words = text.split(" ")
    lines, line = [], ""
    for w in words:
        text_w, _ = font_obj.size(line + w + " ")
        if text_w <= rect.width:
            line += w + " "
        else:
            lines.append(line)
            line = w + " "
    lines.append(line)
    y = rect.y
    for l in lines:
        surface.blit(font_obj.render(l, True, color), (rect.x, y))
        y += font_obj.get_height() + 7
stats.setdefault("gold", 30)
stats.setdefault("hrumki", 1)
stats.setdefault("gazyava", 1)
shop_open = False
shop_index = 0
shop_rect = pygame.Rect(520, 125, 115, 75)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if battle.active:
            res = battle.handle_input(event, stats)
            if res == "FINISHED":
                dialog_text = f"* Бой окончен! Путь: {get_route_name()} (Б:{stats['leopard_kills']}/10, М:{stats['pug_kills']}/5)."
            continue

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
                            state, player_name = "NAME_INPUT", ""
                        elif selected_menu == 1:
                            show_controls = True
                        elif selected_menu == 2:
                            pygame.quit()
                            sys.exit()

            elif state == "NAME_INPUT":
                if event.key == pygame.K_RETURN:
                    if not player_name.strip():
                        player_name = "Милка"
                    state, confirm_choice = "CONFIRM_NAME", 0
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
                        current_slide, char_index, state = 0, 0.0, "STORY"
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
                            state, zone = "GAME", 1
                            dialog_text = f"* Меймей: Привет, {player_name}! Это Снежные холмы. Справа есть лавка с припасами!"
            elif state == "GAME":
                if shop_open:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        shop_index = (shop_index - 1) % 3
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        shop_index = (shop_index + 1) % 3
                    elif event.key in (pygame.K_ESCAPE, pygame.K_x):
                        shop_open = False
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_z):
                        if shop_index == 2:
                            shop_open = False
                        elif stats["gold"] >= 10:
                            stats["gold"] -= 10
                            if shop_index == 0:
                                stats["hrumki"] += 1
                            else:
                                stats["gazyava"] += 1
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_z):
                    if dialog_text:
                        dialog_text = ""
                    elif zone == 1 and player_rect.colliderect(shop_rect.inflate(25, 25)):
                        shop_open, shop_index = True, 0
                    elif player_rect.colliderect(pygame.Rect(meimei_x - 20, meimei_y - 20, 90, 70)):
                        route = get_route_name()
                        if route == "ПАЦИФИСТ":
                            dialog_text = "* Меймей: Ты никого не обидел! Настоящий друг природы."
                        elif route == "ГЕНОЦИД":
                            dialog_text = "* Меймей (в ужасе): 10 барсов и 5 мопсов... Остановись."
                        else:
                            dialog_text = f"* Меймей: Барсов: {stats['leopard_kills']}/10, Мопсов: {stats['pug_kills']}/5."

    if battle.active:
        if battle.update(stats) == "DEFEAT":
            dialog_text = "* ОЗ закончились! Меймей оттащила тебя к привалу."
        battle.draw(screen, menu_font, small_font, player_name, stats)
        pygame.display.flip()
        clock.tick(FPS)
        continue

    screen.fill(BLACK)

    if state == "MENU":
        for i in range(25):
            sx = (i * 73 + pygame.time.get_ticks() // 40) % WIDTH
            sy = (i * 41 + pygame.time.get_ticks() // 25) % HEIGHT
            pygame.draw.circle(screen, ICE_BLUE, (sx, sy), 2)
        t1 = title_font.render("ПОД-ЭВЕРЕСТ", True, WHITE)
        t2 = small_font.render("MilkaTale: Снежные холмы", True, ICE_BLUE)
        screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 65))
        screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 120))
        draw_dachshund(screen, WIDTH // 2 - 24, 180, "right", 1.1)
        if show_controls:
            pygame.draw.rect(screen, WHITE, (140, 240, 520, 175), 3)
            screen.blit(story_font.render("Стрелки / WASD — движение и уклонение", True, WHITE), (160, 265))
            screen.blit(story_font.render("Enter / Пробел / Z — действие и лавка", True, WHITE), (160, 305))
            screen.blit(small_font.render("Нажмите Enter, чтобы вернуться", True, YELLOW), (160, 365))
        else:
            for idx, opt in enumerate(menu_options):
                col = YELLOW if idx == selected_menu else WHITE
                pref = "> " if idx == selected_menu else "  "
                screen.blit(menu_font.render(pref + opt, True, col), (WIDTH // 2 - 140, 265 + idx * 50))

    elif state == "NAME_INPUT":
        p1 = menu_font.render("Назовите таксу-путешественника:", True, WHITE)
        screen.blit(p1, (WIDTH // 2 - p1.get_width() // 2, 110))
        box = pygame.Rect(WIDTH // 2 - 180, 215, 360, 55)
        pygame.draw.rect(screen, WHITE, box, 3)
        cur = "_" if (pygame.time.get_ticks() // 400) % 2 == 0 else ""
        screen.blit(title_font.render(player_name + cur, True, YELLOW), (box.x + 20, box.y + 6))

    elif state == "CONFIRM_NAME":
        q1 = menu_font.render(f"Выбрано имя: {player_name}", True, YELLOW)
        screen.blit(q1, (WIDTH // 2 - q1.get_width() // 2, 135))
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

    elif state == "GAME":
        moved = False
        if not dialog_text and not shop_open:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_rect.x -= 4
                player_dir, moved = "left", True
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_rect.x += 4
                player_dir, moved = "right", True
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player_rect.y -= 4
                moved = True
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player_rect.y += 4
                moved = True
            if zone == 1 and player_rect.right >= 735:
                zone, player_rect.x, meimei_x, meimei_y, step_counter = 2, 85, 180, 220, 0
                if not zone2_intro_done:
                    dialog_text = "* Меймей: Дальше Тропа Мопсов! Будь начеку."
                    zone2_intro_done = True
            elif zone == 2 and player_rect.left <= 65:
                zone, player_rect.x, meimei_x, meimei_y, step_counter = 1, 670, 220, 220, 0
            player_rect.clamp_ip(pygame.Rect(65, 105, 670, 330))

        if moved:
            step_counter += 1
            if step_counter >= 115:
                step_counter = 0
                battle.start("leopard" if zone == 1 else "pug")

        pygame.draw.rect(screen, SNOW_GROUND, (60, 100, 680, 340))
        pygame.draw.rect(screen, ICE_BLUE, (60, 100, 680, 340), 4)
        pygame.draw.ellipse(screen, SNOW_SHADOW, (140, 150, 160, 45))
        pygame.draw.ellipse(screen, SNOW_SHADOW, (460, 340, 180, 50))

        if zone == 1:
            pygame.draw.rect(screen, (140, 80, 45), shop_rect, border_radius=6)
            pygame.draw.polygon(screen, (200, 60, 60), [(510, 125), (577, 92), (645, 125)])
            screen.blit(small_font.render("ЛАВКА", True, YELLOW), (550, 148))
            pygame.draw.polygon(screen, YELLOW, [(725, 270), (705, 255), (705, 285)])
        else:
            pygame.draw.polygon(screen, YELLOW, [(75, 270), (95, 255), (95, 285)])

        draw_meimei(screen, meimei_x, meimei_y)
        draw_dachshund(screen, player_rect.x, player_rect.y, player_dir, 1.0)

        hud_str = f"УР {stats['lv']} | ПУТЬ: {get_route_name()} | Б:{stats['leopard_kills']}/10 М:{stats['pug_kills']}/5 | ЗОЛОТО: {stats['gold']}"
        screen.blit(small_font.render(hud_str, True, WHITE), (60, 65))

        if dialog_text:
            pygame.draw.rect(screen, BLACK, (60, 330, 680, 135))
            pygame.draw.rect(screen, WHITE, (60, 330, 680, 135), 4)
            draw_wrapped_text(screen, dialog_text, story_font, WHITE, pygame.Rect(85, 350, 630, 100))

        if shop_open:
            pygame.draw.rect(screen, BLACK, (150, 140, 500, 230))
            pygame.draw.rect(screen, YELLOW, (150, 140, 500, 230), 4)
            screen.blit(menu_font.render(f"ЛАВКА ПРИПАСОВ (Золото: {stats['gold']})", True, YELLOW), (175, 160))
            items = [
                f"Хрумки (10G) — у вас: {stats['hrumki']} шт.",
                f"Газява (10G) — у вас: {stats['gazyava']} шт.",
                "Выйти из лавки"
            ]
            for i, it in enumerate(items):
                col = YELLOW if shop_index == i else WHITE
                pref = "> " if shop_index == i else "  "
                screen.blit(small_font.render(pref + it, True, col), (180, 215 + i * 35))
            screen.blit(small_font.render("Комбо в бою: Хрумки + Газява = +30 ОЗ!", True, ICE_BLUE), (180, 330))

    pygame.display.flip()
    clock.tick(FPS)
