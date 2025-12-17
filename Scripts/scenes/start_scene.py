import math
import random

import pygame

import config
from scenes.menu_scene import MenuScene


class _Button:
    def __init__(self, label: str, rect: pygame.Rect):
        self.label = label
        self.rect = rect
        self.hover = 0.0  # 0..1 animation


class StartScene:
    """
    Cute animated start screen shown before the main MenuScene.
    Pages: main (buttons), options, credits.
    """

    def __init__(self, app):
        self.app = app
        self.page = "main"  # main/options/credits

        self._t = 0.0
        self._sparkles = self._make_sparkles(28)
        self._buttons = []
        self._resolution_idx = 0
        self._palette_idx = 0

        # Presets for options
        self._resolutions = [
            (1000, 700),
            (1200, 800),
            (1280, 720),
            (1600, 900),
        ]
        # Default to current
        try:
            cur = (int(config.WIDTH), int(config.HEIGHT))
            if cur in self._resolutions:
                self._resolution_idx = self._resolutions.index(cur)
            else:
                self._resolutions.insert(0, cur)
                self._resolution_idx = 0
        except Exception:
            pass

        self._palettes = [("default", "Default palette"), ("colorblind", "Colorblind-friendly")]
        cur_palette = str(self.app.user_settings.get("palette", "default")).lower()
        self._palette_idx = 1 if cur_palette.startswith("color") else 0

        # Apply palette at startup (ensures consistency)
        self.app.apply_palette(self._palettes[self._palette_idx][0])

    def _make_sparkles(self, n: int):
        rng = random.Random(7)
        out = []
        for _ in range(n):
            out.append(
                {
                    "x": rng.random(),
                    "y": rng.random(),
                    "r": rng.uniform(1.0, 2.8),
                    "s": rng.uniform(0.15, 0.55),  # speed
                    "p": rng.uniform(0.0, math.tau),
                }
            )
        return out

    def _layout(self):
        w, h = self.app.screen.get_size()
        panel_w = min(520, int(w * 0.62))
        panel_h = min(420, int(h * 0.62))
        panel = pygame.Rect((w - panel_w) // 2, (h - panel_h) // 2, panel_w, panel_h)

        btn_w = int(panel_w * 0.72)
        btn_h = 54
        gap = 14
        bx = panel.centerx - btn_w // 2
        by = panel.y + int(panel_h * 0.48)

        self._buttons = [
            _Button("Start Game", pygame.Rect(bx, by + 0 * (btn_h + gap), btn_w, btn_h)),
            _Button("Options", pygame.Rect(bx, by + 1 * (btn_h + gap), btn_w, btn_h)),
            _Button("Credits", pygame.Rect(bx, by + 2 * (btn_h + gap), btn_w, btn_h)),
        ]
        return panel

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.page == "main":
                    self.app.stop()
                else:
                    self.page = "main"
                return

            if self.page == "main":
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self._go_start()
                    return
                if event.key == pygame.K_o:
                    self.page = "options"
                    return
                if event.key == pygame.K_c:
                    self.page = "credits"
                    return

            if self.page == "options":
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self._resolution_idx = (self._resolution_idx - 1) % len(self._resolutions)
                    return
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    self._resolution_idx = (self._resolution_idx + 1) % len(self._resolutions)
                    return
                if event.key in (pygame.K_UP, pygame.K_w):
                    self._palette_idx = (self._palette_idx - 1) % len(self._palettes)
                    self.app.apply_palette(self._palettes[self._palette_idx][0])
                    return
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    self._palette_idx = (self._palette_idx + 1) % len(self._palettes)
                    self.app.apply_palette(self._palettes[self._palette_idx][0])
                    return
                if event.key == pygame.K_RETURN:
                    w, h = self._resolutions[self._resolution_idx]
                    self.app.apply_window_settings(w, h)
                    return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if self.page == "main":
                for b in self._buttons:
                    if b.rect.collidepoint(mx, my):
                        if b.label == "Start Game":
                            self._go_start()
                        elif b.label == "Options":
                            self.page = "options"
                        else:
                            self.page = "credits"
                        return

            elif self.page == "options":
                # Click zones: resolution row and palette row
                w, h = self.app.screen.get_size()
                panel = self._layout()
                left = panel.x + 26
                top = panel.y + int(panel.h * 0.34)

                res_row = pygame.Rect(left, top, panel.w - 52, 48)
                pal_row = pygame.Rect(left, top + 62, panel.w - 52, 48)
                apply_btn = pygame.Rect(panel.centerx - 110, panel.bottom - 74, 220, 46)

                if res_row.collidepoint(mx, my):
                    self._resolution_idx = (self._resolution_idx + 1) % len(self._resolutions)
                    return
                if pal_row.collidepoint(mx, my):
                    self._palette_idx = (self._palette_idx + 1) % len(self._palettes)
                    self.app.apply_palette(self._palettes[self._palette_idx][0])
                    return
                if apply_btn.collidepoint(mx, my):
                    rw, rh = self._resolutions[self._resolution_idx]
                    self.app.apply_window_settings(rw, rh)
                    return

            else:  # credits
                self.page = "main"

    def _go_start(self):
        # Start from the existing MenuScene, seeded with persisted settings.
        initial = dict(self.app.user_settings)
        self.app.set_scene(MenuScene(self.app, initial=initial))

    def update(self, dt_ms):
        self._t += float(dt_ms) / 1000.0

        # Button hover easing
        mx, my = pygame.mouse.get_pos()
        for b in self._buttons:
            target = 1.0 if b.rect.collidepoint(mx, my) and self.page == "main" else 0.0
            b.hover += (target - b.hover) * 0.18

    def draw(self):
        screen = self.app.screen
        w, h = screen.get_size()

        self._layout()

        self._draw_animated_bg(screen, w, h)

        if self.page == "main":
            self._draw_main(screen)
        elif self.page == "options":
            self._draw_options(screen)
        else:
            self._draw_credits(screen)

        pygame.display.flip()

    # -----------------
    # Rendering helpers
    # -----------------
    def _draw_animated_bg(self, screen, w: int, h: int):
        screen.fill(config.BG_COLOR)

        # Soft moving gradient bands
        for i in range(5):
            t = self._t * (0.25 + i * 0.05)
            cx = int(w * (0.15 + 0.18 * i) + math.sin(t + i) * (22 + i * 9))
            cy = int(h * (0.20 + 0.16 * i) + math.cos(t * 1.15 + i) * (18 + i * 7))
            r = int(min(w, h) * (0.45 - i * 0.06))
            col = config.COLORS[i % len(config.COLORS)]
            alpha = 22
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.circle(s, (*col, alpha), (cx, cy), max(10, r))
            screen.blit(s, (0, 0))

        # Sparkles
        for sp in self._sparkles:
            sp["p"] += sp["s"] * 0.02
            x = int((sp["x"] + math.sin(sp["p"]) * 0.004) * w)
            y = int((sp["y"] + math.cos(sp["p"] * 1.7) * 0.004) * h)
            a = int(110 + 90 * (0.5 + 0.5 * math.sin(sp["p"])))
            r = int(sp["r"])
            pygame.draw.circle(screen, (235, 235, 245, a), (x, y), max(1, r))

    def _draw_panel(self, screen, title: str, subtitle: str = ""):
        panel = self._layout()
        # Panel
        card = pygame.Surface((panel.w, panel.h), pygame.SRCALPHA)
        pygame.draw.rect(card, (*config.UI_BG, 215), card.get_rect(), border_radius=18)
        pygame.draw.rect(card, (255, 255, 255, 32), card.get_rect(), width=2, border_radius=18)
        screen.blit(card, (panel.x, panel.y))

        title_font = self.app.menu_title_font
        small = self.app.menu_hint_font

        ty = panel.y + 26
        title_s = title_font.render(title, True, config.TEXT_COLOR)
        screen.blit(title_s, (panel.centerx - title_s.get_width() // 2, ty))
        ty += title_s.get_height() + 10

        if subtitle:
            sub_s = small.render(subtitle, True, (200, 200, 210))
            screen.blit(sub_s, (panel.centerx - sub_s.get_width() // 2, ty))

        return panel

    def _draw_button(self, screen, button: _Button):
        base = pygame.Rect(button.rect)
        lift = int(3 * button.hover)
        base.y -= lift

        col = (255, 255, 255, int(18 + 28 * button.hover))
        s = pygame.Surface((base.w, base.h), pygame.SRCALPHA)
        pygame.draw.rect(s, (*config.UI_BG, 230), s.get_rect(), border_radius=14)
        pygame.draw.rect(s, col, s.get_rect(), width=2, border_radius=14)
        screen.blit(s, (base.x, base.y))

        # Accent dot
        accent = config.COLORS[0]
        pygame.draw.circle(screen, accent, (base.x + 20, base.centery), 6)

        label = self.app.menu_item_font.render(button.label, True, config.TEXT_COLOR)
        screen.blit(label, (base.centerx - label.get_width() // 2, base.centery - label.get_height() // 2))

    def _draw_main(self, screen):
        panel = self._draw_panel(screen, "Kmeans Game", "A mini data-mining visualizer")

        # Cute little orbiting dots logo (no external assets needed)
        cx = panel.centerx
        cy = panel.y + int(panel.h * 0.30)
        pygame.draw.circle(screen, (255, 255, 255, 40), (cx, cy), 58, width=2)
        for i in range(3):
            ang = self._t * (0.9 + i * 0.25) + i * 2.1
            px = int(cx + math.cos(ang) * (40 + i * 7))
            py = int(cy + math.sin(ang) * (26 + i * 6))
            col = config.COLORS[i % len(config.COLORS)]
            pygame.draw.circle(screen, col, (px, py), 10 - i * 2)

        for b in self._buttons:
            self._draw_button(screen, b)

        hint = self.app.menu_hint_font.render("[ENTER] Start  |  [O] Options  |  [C] Credits  |  [ESC] Quit", True, (200, 200, 210))
        screen.blit(hint, (panel.centerx - hint.get_width() // 2, panel.bottom - 32))

    def _draw_options(self, screen):
        panel = self._draw_panel(screen, "Options", "Click a row to change • [ESC] Back")
        font = self.app.menu_item_font
        hint = self.app.menu_hint_font

        left = panel.x + 26
        top = panel.y + int(panel.h * 0.34)
        row_w = panel.w - 52

        # Resolution row
        res = self._resolutions[self._resolution_idx]
        res_label = f"Window size: {res[0]}×{res[1]}  (click to cycle)"
        self._draw_option_row(screen, pygame.Rect(left, top, row_w, 48), res_label, config.COLORS[1])

        # Palette row
        pal_key, pal_label = self._palettes[self._palette_idx]
        pal_text = f"Colors: {pal_label}  (click to toggle)"
        self._draw_option_row(screen, pygame.Rect(left, top + 62, row_w, 48), pal_text, config.COLORS[2])

        note = hint.render("Tip: press [ENTER] to apply size, or click Apply.", True, (200, 200, 210))
        screen.blit(note, (left, top + 130))

        # Apply button
        apply_btn = pygame.Rect(panel.centerx - 110, panel.bottom - 74, 220, 46)
        mx, my = pygame.mouse.get_pos()
        hover = apply_btn.collidepoint(mx, my)
        s = pygame.Surface((apply_btn.w, apply_btn.h), pygame.SRCALPHA)
        pygame.draw.rect(s, (*config.UI_BG, 235), s.get_rect(), border_radius=14)
        pygame.draw.rect(s, (255, 255, 255, 55 if hover else 28), s.get_rect(), width=2, border_radius=14)
        screen.blit(s, (apply_btn.x, apply_btn.y))
        txt = font.render("Apply Window Size", True, config.TEXT_COLOR)
        screen.blit(txt, (apply_btn.centerx - txt.get_width() // 2, apply_btn.centery - txt.get_height() // 2))

    def _draw_option_row(self, screen, rect: pygame.Rect, text: str, accent):
        mx, my = pygame.mouse.get_pos()
        hover = rect.collidepoint(mx, my)
        s = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(s, (*config.UI_BG, 220), s.get_rect(), border_radius=12)
        pygame.draw.rect(s, (255, 255, 255, 42 if hover else 24), s.get_rect(), width=2, border_radius=12)
        screen.blit(s, (rect.x, rect.y))
        pygame.draw.circle(screen, accent, (rect.x + 18, rect.centery), 6)
        label = self.app.menu_item_font.render(text, True, config.TEXT_COLOR)
        screen.blit(label, (rect.x + 34, rect.centery - label.get_height() // 2))

    def _draw_credits(self, screen):
        panel = self._draw_panel(screen, "Credits", "Click anywhere to go back • [ESC] Back")
        font = self.app.menu_item_font
        hint = self.app.menu_hint_font

        lines = [
            ("Created by", "Nour Ltaief"),
            ("Class", "3DNI1"),
            ("Teacher", "Yassine Net"),
            ("Thanks", "For playing and exploring data mining!"),
            ("GitHub", "https://github.com/nerkolt/Kmeans_Game"),
        ]

        y = panel.y + int(panel.h * 0.30)
        for k, v in lines:
            key_s = hint.render(k.upper(), True, (190, 190, 205))
            val_s = font.render(v, True, config.TEXT_COLOR)
            screen.blit(key_s, (panel.x + 30, y))
            screen.blit(val_s, (panel.x + 30, y + key_s.get_height() + 4))
            y += key_s.get_height() + val_s.get_height() + 18

        foot = hint.render("Tip: You can change settings in Options before entering the main menu.", True, (200, 200, 210))
        screen.blit(foot, (panel.centerx - foot.get_width() // 2, panel.bottom - 34))


