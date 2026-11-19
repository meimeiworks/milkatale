import pygame

BLACK = (10, 10, 16)
WHITE = (245, 245, 250)
ICE_BLUE = (130, 210, 255)
DARK_BLUE = (25, 45, 85)
DACHSHUND_BROWN = (155, 85, 40)
DACHSHUND_DARK = (105, 50, 20)
MOSS_GLOW = (80, 230, 170)

def build_story(name):
    return [
        {
            "scene": "everest_climb",
            "text": f"Давным-давно отважный маленький такс по имени {name} решил покорить высочайшую вершину мира — гору Эверест."
        },
        {
            "scene": "snowstorm",
            "text": f"Шаг за шагом, сквозь ледяной ветер и снежную бурю, {name} взбирался всё выше к облакам..."
        },
        {
            "scene": "collapse",
            "text": "Но у самой вершины раздался оглушительный треск! Снежный карниз обрушился прямо под лапами..."
        },
        {
            "scene": "falling",
            "text": f"{name} сорвался вниз, в бездонную ледяную расщелину, ведущую в таинственный Под-Эверест."
        },
        {
            "scene": "landing",
            "text": f"Чудом уцелев на мягком сугробе светящегося мха, {name} твёрдо решает найти путь наверх!"
        }
    ]

def draw_dachshund(surface, x, y, facing="right", scale=1.0):
    w = int(48 * scale)
    h = int(24 * scale)
    pygame.draw.rect(surface, DACHSHUND_BROWN, (x, y, w, h), border_radius=8)

    leg_w = int(8 * scale)
    leg_h = int(10 * scale)
    pygame.draw.rect(surface, DACHSHUND_DARK, (x + int(6 * scale), y + h - 2, leg_w, leg_h), border_radius=3)
    pygame.draw.rect(surface, DACHSHUND_DARK, (x + w - int(14 * scale), y + h - 2, leg_w, leg_h), border_radius=3)

    if facing == "right":
        pygame.draw.circle(surface, DACHSHUND_BROWN, (x + w, y + int(4 * scale)), int(13 * scale))
        pygame.draw.ellipse(surface, DACHSHUND_BROWN, (x + w + int(4 * scale), y + int(2 * scale), int(16 * scale), int(10 * scale)))
        pygame.draw.ellipse(surface, DACHSHUND_DARK, (x + w - int(8 * scale), y + int(2 * scale), int(10 * scale), int(20 * scale)))
        pygame.draw.circle(surface, WHITE, (x + w + int(4 * scale), y), int(3 * scale))
        pygame.draw.circle(surface, BLACK, (x + w + int(5 * scale), y), int(1.5 * scale))
        pygame.draw.circle(surface, BLACK, (x + w + int(19 * scale), y + int(5 * scale)), int(2.5 * scale))
    else:
        pygame.draw.circle(surface, DACHSHUND_BROWN, (x, y + int(4 * scale)), int(13 * scale))
        pygame.draw.ellipse(surface, DACHSHUND_BROWN, (x - int(20 * scale), y + int(2 * scale), int(16 * scale), int(10 * scale)))
        pygame.draw.ellipse(surface, DACHSHUND_DARK, (x - int(2 * scale), y + int(2 * scale), int(10 * scale), int(20 * scale)))
        pygame.draw.circle(surface, WHITE, (x - int(4 * scale), y), int(3 * scale))
        pygame.draw.circle(surface, BLACK, (x - int(5 * scale), y), int(1.5 * scale))
        pygame.draw.circle(surface, BLACK, (x - int(19 * scale), y + int(5 * scale)), int(2.5 * scale))

def draw_story_illustration(surface, scene_type):
    box = pygame.Rect(170, 45, 460, 220)
    pygame.draw.rect(surface, BLACK, box)
    pygame.draw.rect(surface, WHITE, box, 4)

    if scene_type == "everest_climb":
        pygame.draw.polygon(surface, DARK_BLUE, [(210, 260), (400, 75), (590, 260)])
        pygame.draw.polygon(surface, WHITE, [(345, 130), (400, 75), (455, 130), (425, 145), (400, 125), (375, 145)])
        draw_dachshund(surface, 310, 175, "right", 0.9)

    elif scene_type == "snowstorm":
        pygame.draw.polygon(surface, DARK_BLUE, [(190, 260), (400, 65), (610, 260)])
        pygame.draw.polygon(surface, ICE_BLUE, [(330, 135), (400, 65), (470, 135)])
        draw_dachshund(surface, 365, 110, "right", 0.9)
        for i in range(12):
            lx = 190 + (i * 37) % 410
            ly = 65 + (i * 29) % 180
            pygame.draw.line(surface, WHITE, (lx, ly), (lx + 25, ly + 8), 2)

    elif scene_type == "collapse":
        pygame.draw.polygon(surface, DARK_BLUE, [(180, 260), (350, 90), (350, 260)])
        pygame.draw.polygon(surface, WHITE, [(280, 160), (350, 90), (350, 160)])
        pygame.draw.rect(surface, ICE_BLUE, (380, 155, 45, 30), border_radius=5)
        pygame.draw.rect(surface, WHITE, (430, 185, 35, 25), border_radius=5)
        draw_dachshund(surface, 390, 120, "right", 0.9)

    elif scene_type == "falling":
        pygame.draw.rect(surface, (18, 22, 40), (174, 49, 452, 212))
        pygame.draw.line(surface, ICE_BLUE, (230, 60), (230, 240), 3)
        pygame.draw.line(surface, ICE_BLUE, (570, 60), (570, 240), 3)
        draw_dachshund(surface, 375, 145, "left", 1.0)

    elif scene_type == "landing":
        pygame.draw.ellipse(surface, MOSS_GLOW, (270, 215, 260, 38))
        pygame.draw.circle(surface, MOSS_GLOW, (240, 130), 4)
        pygame.draw.circle(surface, MOSS_GLOW, (540, 110), 5)
        draw_dachshund(surface, 375, 195, "right", 1.0)
