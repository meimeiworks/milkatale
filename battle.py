import pygame
import random

BLACK = (10, 10, 16)
WHITE = (245, 245, 250)
YELLOW = (255, 225, 60)
ICE_BLUE = (130, 210, 255)
PURPLE_SOUL = (175, 95, 245)

class BattleSystem:
    def __init__(self):
        self.active = False
        self.enemy_type = "leopard"
        self.enemy_name = "Снежный барс"
        self.enemy_hp = 30
        self.enemy_max_hp = 30
        self.sparable = False
        self.phase = "MENU"
        self.btn_index = 0
        self.sub_index = 0
        self.message = ""
        self.end_text = ""
        self.box = pygame.Rect(275, 215, 250, 145)
        self.soul = pygame.Rect(392, 280, 16, 16)
        self.bullets = []
        self.dodge_timer = 0
        self.invuln = 0
        self.ate_hrumki = False

    def start(self, enemy_type):
        self.active = True
        self.enemy_type = enemy_type
        self.sparable = False
        self.phase = "MENU"
        self.btn_index = 0
        self.sub_index = 0
        self.bullets = []
        self.invuln = 0
        self.ate_hrumki = False
        if enemy_type == "leopard":
            self.enemy_name, self.enemy_hp, self.enemy_max_hp = "Снежный барс", 30, 30
            self.message = "* Снежный барс преградил тропу!"
        else:
            self.enemy_name, self.enemy_hp, self.enemy_max_hp = "Пухлый мопс", 24, 24
            self.message = "* Из сугроба выскочил Пухлый мопс!"

    def start_enemy_turn(self):
        self.phase = "DODGE"
        self.dodge_timer = 200
        self.soul.center = self.box.center
        self.bullets = []
        if self.enemy_type == "leopard":
            for i in range(8):
                bx = random.randint(self.box.left + 12, self.box.right - 22)
                self.bullets.append({"rect": pygame.Rect(bx, self.box.top - i * 34, 10, 10), "vx": 0, "vy": 2.3, "kind": "snow"})
        else:
            for i in range(6):
                side = -1 if i % 2 == 0 else 1
                bx = self.box.right + i * 44 if side == -1 else self.box.left - i * 44
                by = random.randint(self.box.top + 15, self.box.bottom - 25)
                self.bullets.append({"rect": pygame.Rect(bx, by, 16, 8), "vx": side * 2.4, "vy": 0, "kind": "bone"})
    def handle_input(self, event, stats):
        if event.type != pygame.KEYDOWN:
            return None
        if self.phase == "MENU":
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.btn_index = (self.btn_index - 1) % 4
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.btn_index = (self.btn_index + 1) % 4
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_z):
                if self.btn_index == 0:
                    self.ate_hrumki = False
                    dmg = 10 + stats["lv"] * 4
                    self.enemy_hp -= dmg
                    if self.enemy_hp <= 0:
                        self.enemy_hp = 0
                        key = "leopard_kills" if self.enemy_type == "leopard" else "pug_kills"
                        gain = 15 if self.enemy_type == "leopard" else 12
                        stats[key] += 1
                        stats["exp"] += gain
                        stats["gold"] += 15
                        while stats["exp"] >= stats["lv"] * 20:
                            stats["exp"] -= stats["lv"] * 20
                            stats["lv"] += 1
                            stats["max_hp"] += 4
                            stats["hp"] = stats["max_hp"]
                        self.end_text = f"* Победа! +{gain} ОП, +15G (УР {stats['lv']}). Б:{stats['leopard_kills']}/10 М:{stats['pug_kills']}/5"
                        self.phase = "END_MSG"
                    else:
                        self.message = f"* Удар на {dmg} урона! ({self.enemy_hp}/{self.enemy_max_hp} ОЗ)"
                        self.start_enemy_turn()
                elif self.btn_index == 1:
                    self.phase, self.sub_index = "ACT_MENU", 0
                elif self.btn_index == 2:
                    self.phase, self.sub_index = "ITEM_MENU", 0
                elif self.btn_index == 3:
                    if self.sparable:
                        stats["spares"] += 1
                        stats["gold"] += 10
                        self.end_text = f"* Пощада ({self.enemy_name})! Получено +10G."
                        self.phase = "END_MSG"
                    else:
                        self.message = "* Враг не готов. Попробуйте ДЕЙСТВИЕ!"
        elif self.phase == "ACT_MENU":
            if event.key in (pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s):
                self.sub_index = 1 - self.sub_index
            elif event.key in (pygame.K_ESCAPE, pygame.K_x):
                self.phase = "MENU"
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_z):
                self.ate_hrumki = False
                if self.sub_index == 0:
                    self.message = "* Снежный барс (АТК 4). Любит похвалу." if self.enemy_type == "leopard" else "* Пухлый мопс (АТК 3). Хочет играть."
                else:
                    self.sparable = True
                    self.message = "* Вы погладили барса. Он замурчал!" if self.enemy_type == "leopard" else "* Вы почесали мопса. Он виляет хвостом!"
                self.start_enemy_turn()
        elif self.phase == "ITEM_MENU":
            if event.key in (pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s):
                self.sub_index = 1 - self.sub_index
            elif event.key in (pygame.K_ESCAPE, pygame.K_x):
                self.phase = "MENU"
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_z):
                if self.sub_index == 0:
                    if stats["hrumki"] > 0:
                        stats["hrumki"] -= 1
                        stats["hp"] = min(stats["max_hp"], stats["hp"] + 10)
                        self.ate_hrumki = True
                        self.message = "* Вы съели Хрумки! +10 ОЗ. (Запейте Газявой для комбо!)"
                        self.start_enemy_turn()
                    else:
                        self.message = "* Хрумки закончились!"
                        self.phase = "MENU"
                else:
                    if stats["gazyava"] > 0:
                        stats["gazyava"] -= 1
                        heal = 30 if self.ate_hrumki else 10
                        stats["hp"] = min(stats["max_hp"], stats["hp"] + heal)
                        self.message = f"* КОМБО! Хрумки + Газява восстановили +{heal} ОЗ!" if self.ate_hrumki else "* Вы выпили Газяву! Восстановлено +10 ОЗ."
                        self.ate_hrumki = False
                        self.start_enemy_turn()
                    else:
                        self.message = "* Газява закончилась!"
                        self.phase = "MENU"
        elif self.phase == "END_MSG" and event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_z):
            self.active = False
            return "FINISHED"
        return None

    def update(self, stats):
        if not self.active or self.phase != "DODGE":
            return None
        if self.invuln > 0:
            self.invuln -= 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.soul.x -= 4
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.soul.x += 4
        if keys[pygame.K_UP] or keys[pygame.K_w]: self.soul.y -= 4
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: self.soul.y += 4
        self.soul.clamp_ip(self.box.inflate(-8, -8))
        for b in self.bullets:
            b["rect"].x += b["vx"]
            b["rect"].y += b["vy"]
            if self.soul.colliderect(b["rect"]) and self.invuln == 0:
                stats["hp"] = max(0, stats["hp"] - 2)
                self.invuln = 35
                if stats["hp"] <= 0:
                    stats["hp"] = stats["max_hp"]
                    self.active = False
                    return "DEFEAT"
        self.dodge_timer -= 1
        if self.dodge_timer <= 0:
            self.phase = "MENU"
            self.message = f"* {self.enemy_name} готов к пощаде!" if self.sparable else f"* {self.enemy_name} готовится к атаке."
        return None

    def draw(self, surface, font, small_font, player_name, stats):
        surface.fill(BLACK)
        cx, cy = 400, 125
        if self.enemy_type == "leopard":
            pygame.draw.ellipse(surface, (215, 225, 240), (cx - 45, cy - 20, 90, 50))
            pygame.draw.circle(surface, (215, 225, 240), (cx, cy - 32), 24)
            pygame.draw.circle(surface, ICE_BLUE, (cx - 8, cy - 34), 4)
            pygame.draw.circle(surface, ICE_BLUE, (cx + 8, cy - 34), 4)
        else:
            pygame.draw.rect(surface, (210, 180, 130), (cx - 38, cy - 18, 76, 46), border_radius=14)
            pygame.draw.circle(surface, (210, 180, 130), (cx, cy - 28), 23)
            pygame.draw.circle(surface, WHITE, (cx - 9, cy - 32), 4)
            pygame.draw.circle(surface, WHITE, (cx + 9, cy - 32), 4)
        n_surf = font.render(f"{self.enemy_name} ({self.enemy_hp}/{self.enemy_max_hp} ОЗ)", True, YELLOW if self.sparable else WHITE)
        surface.blit(n_surf, (400 - n_surf.get_width() // 2, 22))
        if self.phase == "DODGE":
            pygame.draw.rect(surface, WHITE, self.box, 4)
            if self.invuln % 4 < 2:
                pygame.draw.rect(surface, PURPLE_SOUL, self.soul, border_radius=4)
            for b in self.bullets:
                pygame.draw.rect(surface, ICE_BLUE if b["kind"] == "snow" else WHITE, b["rect"], border_radius=3)
        else:
            pygame.draw.rect(surface, WHITE, (65, 205, 670, 155), 4)
            if self.phase == "ACT_MENU":
                a2 = "Погладить" if self.enemy_type == "leopard" else "Почесать за ухом"
                surface.blit(font.render(("> * Осмотреть" if self.sub_index == 0 else "  * Осмотреть"), True, YELLOW if self.sub_index == 0 else WHITE), (95, 235))
                surface.blit(font.render((f"> * {a2}" if self.sub_index == 1 else f"  * {a2}"), True, YELLOW if self.sub_index == 1 else WHITE), (95, 280))
            elif self.phase == "ITEM_MENU":
                i1 = f"Хрумки ({stats['hrumki']} шт.) — +10 ОЗ"
                i2 = f"Газява ({stats['gazyava']} шт.) — +10 ОЗ (или +30 ОЗ после Хрумок!)"
                surface.blit(small_font.render((f"> * {i1}" if self.sub_index == 0 else f"  * {i1}"), True, YELLOW if self.sub_index == 0 else WHITE), (95, 235))
                surface.blit(small_font.render((f"> * {i2}" if self.sub_index == 1 else f"  * {i2}"), True, YELLOW if self.sub_index == 1 else WHITE), (95, 280))
            elif self.phase == "END_MSG":
                surface.blit(small_font.render(self.end_text, True, YELLOW), (90, 250))
                surface.blit(small_font.render("[Enter — продолжить]", True, WHITE), (90, 305))
            else:
                surface.blit(small_font.render(self.message, True, WHITE), (90, 240))
        surface.blit(small_font.render(f"{player_name}   УР {stats['lv']}   ОЗ {stats['hp']}/{stats['max_hp']}   ЗОЛОТО: {stats['gold']}G", True, WHITE), (70, 378))
        for i, label in enumerate(["БИТВА", "ДЕЙСТВИЕ", "ВЕЩИ", "ПОЩАДА"]):
            rect = pygame.Rect(70 + i * 172, 415, 152, 46)
            col = YELLOW if (self.phase == "MENU" and self.btn_index == i) else (255, 140, 40)
            pygame.draw.rect(surface, col, rect, 3)
            txt = font.render(label, True, col)
            surface.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))
