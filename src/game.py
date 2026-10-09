# src/game.py
import sys
import math
import random
import pygame

from src.config import (
    WIDTH, HEIGHT, FPS, SEGMENT_LENGTH,
    GRASS_LIGHT, GRASS_DARK, ROAD_LIGHT, ROAD_DARK,
    SKY_COLOR
)
from src.track import generate_track
from src.player import Player
from src.ui import UIManager

class Game:
    def __init__(self):
        # Inizializzazione Sottosistemi Grafici e Audio
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Motocross 3D")
        self.clock = pygame.time.Clock()
        
        # Inizializzazione Manager e Moduli Esterni
        self.ui = UIManager()
        self.player_bike = Player(base_speed=7500)
        
        # Stato Iniziale e Variabili di Progresso
        self.level = 1
        self.state = "SPLASH"
        self.pos = 0 
        self.lap = 1
        self.max_laps = 2
        self.setup_level_physics()
        self.score = 0
        self.bravo_timer = 0
        self.sky_offset_x = 0
        
        # Configurazione Pilota e Bot
        self.player_color = 'red'
        self.selected_bike_index = 0
        self.available_colors = ['red', 'green', 'blue']
        self.bots = []
        self.final_standings = []
        self.player_final_rank = 3
        
        # Caricamento e preparazione delle risorse statiche
        self.load_assets()
        
        # Generazione della prima pista di default (Livello 1)
        self.lines, self.track_length = generate_track(self.level, self.coin_img)
        self.total_coins = sum(1 for line in self.lines if line.sprite == self.coin_img) # Conta quante ne ha generate
        self.collected_coins = 0 # Inizializza il contatore a zero
        
        # Inizializzazione icone HUD della Classifica
        self.ui.init_leaderboard_icons(self.bike_assets)

    def setup_level_physics(self):
        if self.level == 9:
            self.max_laps = 3
            self.player_bike.jump_power = 150
            self.player_bike.gravity = 2
        else:
            self.max_laps = 2
            self.player_bike.jump_power = 400
            self.player_bike.gravity = 15

    def load_image(self, path, scale_to=None, color_key="auto"):
        """Utility robusta per caricare immagini con trasparenza nativa e fallback"""
        try:
            img = pygame.image.load(path).convert_alpha()
            if color_key == "auto":
                color_key = img.get_at((0, 0))
            if color_key is not None:
                temp = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                img.set_colorkey(color_key)
                temp.blit(img, (0, 0))
                img = temp
            if scale_to:
                img = pygame.transform.scale(img, scale_to)
            return img
        except Exception as e:
            print(f"Avviso: Errore nel caricamento dell'asset {path}: {e}")
            surf = pygame.Surface(scale_to if scale_to else (100, 100), pygame.SRCALPHA)
            if "bike" in path:
                pygame.draw.rect(surf, (200, 0, 0), (surf.get_width()//4, surf.get_height()//2, surf.get_width()//2, surf.get_height()//2))
            elif "coin" in path:
                pygame.draw.circle(surf, (255, 215, 0), (surf.get_width()//2, surf.get_height()//2), surf.get_width()//2)
            return surf

    def load_assets(self):
        """Carica in memoria tutte le immagini dei biomi, le moto e i file audio"""
        self.bike_assets = {
            'red': {
                'side': self.load_image("assets/bike_red.png", (800, 600), "auto"),
                'back': self.load_image("assets/bike_back_view_red.png", (250, 350), "auto")
            },
            'green': {
                'side': self.load_image("assets/bike_green.png", (800, 600), "auto"),
                'back': self.load_image("assets/bike_back_view_green.png", (250, 350), "auto")
            },
            'blue': {
                'side': self.load_image("assets/bike_blue.png", (800, 600), "auto"),
                'back': self.load_image("assets/bike_back_view_blue.png", (250, 350), "auto")
            }
        }
        
        self.bike_back_img = self.load_image("assets/bike_back_view.png", (250, 350), "auto")
        self.bike_side_img = self.load_image("assets/bike.png", (800, 600), "auto")
        self.coin_img = self.load_image("assets/coin.png", (160, 160), None)
        
        self.bg_mountains_img = self.load_image("assets/bg_mountains.png", (WIDTH, HEIGHT), None)
        self.bg_mountains_snow_img = self.load_image("assets/bg_mountains_snow.png", (WIDTH, HEIGHT), None)
        self.bg_city_img = self.load_image("assets/bg_city.png", (WIDTH, HEIGHT), None)
        self.bg_africa_img = self.load_image("assets/bg_africa.png", (WIDTH, HEIGHT), None)
        self.bg_cave_img = self.load_image("assets/bg_cave.png", (WIDTH, HEIGHT), None)
        self.bg_beach_img = self.load_image("assets/bg_beach.png", (WIDTH, HEIGHT), None)
        self.bg_night_img = self.load_image("assets/bg_night.png", (WIDTH, HEIGHT), None)
        self.bg_volcano_img = self.load_image("assets/bg_volcano.png", (WIDTH, HEIGHT), None)
        self.bg_space_img = self.load_image("assets/bg_space.png", (WIDTH, HEIGHT), None)
        
        self.arch_text_imgs = {}
        arch_font = pygame.font.SysFont(None, 200, bold=True)
        for text, color in [("START", (255, 0, 0)), ("AMEDEO", (255, 215, 0))]:
            base_text = arch_font.render(text, True, color)
            text_img = pygame.Surface((base_text.get_width() + 10, base_text.get_height() + 10), pygame.SRCALPHA)
            for dx, dy in [(-4,-4), (-4,4), (4,-4), (4,4), (0,-5), (0,5), (-5,0), (5,0)]:
                outline = arch_font.render(text, True, (255, 255, 255))
                text_img.blit(outline, (5 + dx, 5 + dy))
            text_img.blit(base_text, (5, 5))
            self.arch_text_imgs[text] = text_img
            
        try:
            self.engine_sound = pygame.mixer.Sound("assets/bg_music.wav")
            self.coin_sound = pygame.mixer.Sound("assets/coin.wav")
            self.engine_sound.set_volume(0.4)
            self.coin_sound.set_volume(0.8)
        except Exception as e:
            print("Avviso Audio non disponibile:", e)
            self.engine_sound = None
            self.coin_sound = None

    def draw_quad(self, color, x1, y1, w1, x2, y2, w2):
        """Traccia poligoni quadrangolari per simulare l'effetto prospettico stradale 3D"""
        if y1 <= y2: 
            return
        pygame.draw.polygon(self.screen, color, [
            (x1 - w1, y1), (x2 - w2, y2), (x2 + w2, y2), (x1 + w1, y1)
        ])

    def init_bots(self):
        """Inizializza le IA rivali scalando velocità e griglia di partenza per il livello corretto"""
        colors = list(self.available_colors)
        if self.player_color in colors:
            colors.remove(self.player_color)
            
        self.bots = []
        is_l3 = (self.level == 3)
        bots_start_pos = [2000, 4000] if is_l3 else [3000, 6000]
        
        if is_l3:             speed_boost = -100
        elif self.level == 2: speed_boost = 20
        elif self.level == 4: speed_boost = 30
        elif self.level == 5: speed_boost = 40
        elif self.level == 8: speed_boost = 50
        else:                 speed_boost = 0
            
        self.bots.append({
            'pos': self.pos + bots_start_pos[0], 
            'speed': 7100 + speed_boost,
            'color': colors[0],
            'x': -0.6,
            'lap': 1
        })
        self.bots.append({
            'pos': self.pos + bots_start_pos[1], 
            'speed': 7300 + speed_boost,
            'color': colors[1],
            'x': 0.6,
            'lap': 1
        })

    def run(self):
        """Loop di gioco principale infinito a tempo costante (60 FPS)"""
        running = True
        while running:
            
            # --- 1. GESTIONE EVENTI INPUT SINGOLI ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        
                    if self.state == "SPLASH":
                        self.state = "SELECT_BIKE"
                    elif self.state == "SELECT_BIKE":
                        if event.key == pygame.K_LEFT:
                            self.selected_bike_index = (self.selected_bike_index - 1) % 3
                        elif event.key == pygame.K_RIGHT:
                            self.selected_bike_index = (self.selected_bike_index + 1) % 3
                        elif event.key == pygame.K_RETURN:
                            self.player_color = self.available_colors[self.selected_bike_index]
                            self.state = "PLAYING"
                            self.setup_level_physics()
                            self.lap = 1
                            self.pos = 0
                            self.score = 0
                            self.player_bike.x = 0
                            self.player_bike.y = 0
                            
                            # Rigenera la pista per far riapparire tutte le monete nuove
                            self.lines, self.track_length = generate_track(self.level, self.coin_img)
                            self.total_coins = sum(1 for line in self.lines if line.sprite == self.coin_img)
                            self.collected_coins = 0
                            
                            # Riecco i bot rivali e il suono del motore!
                            self.init_bots()
                            if getattr(self, 'engine_sound', None):
                                self.engine_sound.play(loops=-1)
                                
                    elif self.state == "PLAYING":
                        old_level = self.level
                        if event.key == pygame.K_F1: self.level = 1
                        elif event.key == pygame.K_F2: self.level = 2
                        elif event.key == pygame.K_F3: self.level = 3
                        elif event.key == pygame.K_F4: self.level = 4
                        elif event.key == pygame.K_F5: self.level = 5
                        elif event.key == pygame.K_F6: self.level = 6
                        elif event.key == pygame.K_F7: self.level = 7
                        elif event.key == pygame.K_F8: self.level = 8
                        elif event.key == pygame.K_F9: self.level = 9
                        
                        if self.level != old_level:
                            self.setup_level_physics()
                            self.lines, self.track_length = generate_track(self.level, self.coin_img)
                            self.total_coins = sum(1 for line in self.lines if line.sprite == self.coin_img)
                            self.collected_coins = 0
                            self.init_bots()
                            
                    elif self.state in ("RACE_END", "GAMEOVER"):
                        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            if self.player_final_rank <= 2:
                                if self.level < 9:
                                    self.level += 1
                                    self.setup_level_physics()
                                    self.state = "PLAYING"
                                else:
                                    self.state = "CREDITS"
                            else:
                                self.state = "PLAYING"
                                
                            if self.state != "CREDITS":
                                self.lap = 1
                                self.pos = 0
                                self.lines, self.track_length = generate_track(self.level, self.coin_img)
                                self.total_coins = sum(1 for line in self.lines if line.sprite == self.coin_img)
                                self.collected_coins = 0
                                self.init_bots()
                                if self.state == "PLAYING" and self.engine_sound:
                                    self.engine_sound.play(loops=-1)
                                
                    elif self.state == "CREDITS":
                        if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                            self.level = 1
                            self.setup_level_physics()
                            self.state = "SPLASH"
                            
                if self.state == "PLAYING":
                    did_flip = self.player_bike.handle_event(event)
                    if did_flip:
                        self.score += 10
                        self.bravo_timer = 90

            # --- 2. GESTIONE DEI RENDERING DEGLI SCHERMI DI INTERFACCIA ---
            if self.state == "SPLASH":
                self.ui.draw_splash(self.screen, self.bike_side_img)
                pygame.display.flip()
                self.clock.tick(FPS)
                continue
                
            elif self.state == "SELECT_BIKE":
                self.ui.draw_select_bike(self.screen, self.selected_bike_index, self.bike_assets)
                pygame.display.flip()
                self.clock.tick(FPS)
                continue
                
            elif self.state == "GAMEOVER":
                self.ui.draw_game_over(self.screen, self.score)
                pygame.display.flip()
                self.clock.tick(FPS)
                continue
                
            elif self.state == "RACE_END":
                self.ui.draw_race_end(self.screen, self.level, self.final_standings, self.player_final_rank, self.collected_coins, self.total_coins)
                pygame.display.flip()
                self.clock.tick(FPS)
                continue
                
            elif self.state == "CREDITS":
                # We need to maintain a credits_y variable, so let's use self.credits_y
                if not hasattr(self, 'credits_y'):
                    self.credits_y = HEIGHT
                self.credits_y -= 100 / FPS
                bike_side_img = self.bike_assets.get(self.player_color, {}).get('side', self.bike_side_img)
                self.ui.draw_credits(self.screen, self.bg_space_img, bike_side_img, self.credits_y, self.score)
                pygame.display.flip()
                self.clock.tick(FPS)
                continue

            # --- 3. LOGICA DI FISICA CONTINUA (STATO: PLAYING) ---
            keys = pygame.key.get_pressed()
            
            sky_turn = self.player_bike.handle_input(keys)
            self.sky_offset_x += sky_turn
            
            self.speed = self.player_bike.speed
            self.player_bike.update_physics()

            check_idx = (int(self.pos / SEGMENT_LENGTH) + 1) % len(self.lines)
            check_line = self.lines[check_idx]
            if check_line.has_tree:
                if abs(self.player_bike.x - check_line.treeX) < 0.4 and self.player_bike.y < 1200:
                    self.player_bike.reset_on_collision()
                    self.speed = 0
                    self.pos -= 150 

            for bot in self.bots:
                bot['pos'] += bot['speed'] * (1 / FPS)
                if bot['pos'] >= self.track_length:
                    bot['pos'] -= self.track_length
                    bot['lap'] = bot.get('lap', 1) + 1
                elif bot['pos'] < 0:
                    bot['pos'] += self.track_length
                    bot['lap'] = max(1, bot.get('lap', 1) - 1)

            self.pos += self.speed * (1 / FPS)
            while self.pos >= self.track_length:
                self.pos -= self.track_length
                self.lap += 1
                if self.lap > self.max_laps:
                    self.lap = self.max_laps
                    self.state = "RACE_END"
                    if self.engine_sound:
                        self.engine_sound.stop()
                    
                    participants = []
                    participants.append({
                        'name': 'TU', 'color': self.player_color,
                        'dist': self.max_laps * self.track_length + self.pos, 'is_player': True
                    })
                    for b in self.bots:
                        b_lap = b.get('lap', 1)
                        b_dist = (b_lap - 1) * self.track_length + b['pos']
                        c_name = {'red':'ROSSA','green':'VERDE','blue':'BLU'}.get(b['color'], b['color'].upper())
                        participants.append({
                            'name': c_name, 'color': b['color'], 'dist': b_dist, 'is_player': False
                        })
                    participants.sort(key=lambda x: x['dist'], reverse=True)
                    self.final_standings = participants
                    
                    for r, p in enumerate(participants, 1):
                        if p['is_player']:
                            self.player_final_rank = r

            # --- 4. RENDERIZZAZIONE DEL MONDO PSEUDO-3D ---
            if self.level == 1:   current_sky_color = SKY_COLOR
            elif self.level == 2: current_sky_color = (0, 71, 171)
            elif self.level == 4: current_sky_color = (255, 140, 0)
            elif self.level == 5: current_sky_color = (15, 10, 25)
            elif self.level == 6: current_sky_color = (110, 195, 255)
            elif self.level == 7: current_sky_color = (5, 5, 20)
            elif self.level == 8: current_sky_color = (80, 20, 5)
            elif self.level == 9: current_sky_color = (5, 5, 10)
            else:                 current_sky_color = (135, 206, 235)
            self.screen.fill(current_sky_color)
            
            startPos = int(self.pos / SEGMENT_LENGTH)
            current_line = self.lines[startPos % len(self.lines)]
            self.sky_offset_x -= current_line.curve * self.speed * 0.0003
            self.sky_offset_x = self.sky_offset_x % WIDTH
            
            bg_x = int(self.sky_offset_x)
            if self.level == 1:   current_bg = self.bg_mountains_img
            elif self.level == 2: current_bg = self.bg_mountains_snow_img
            elif self.level == 4: current_bg = self.bg_africa_img
            elif self.level == 5: current_bg = self.bg_cave_img
            elif self.level == 6: current_bg = self.bg_beach_img
            elif self.level == 7: current_bg = self.bg_night_img
            elif self.level == 8: current_bg = self.bg_volcano_img
            elif self.level == 9: current_bg = self.bg_space_img
            else:                 current_bg = self.bg_city_img
            self.screen.blit(current_bg, (bg_x, 0))
            self.screen.blit(current_bg, (bg_x - WIDTH, 0))
            
            percent = (self.pos % SEGMENT_LENGTH) / SEGMENT_LENGTH
            
            curr_y = self.lines[startPos % len(self.lines)].y
            next_y = self.lines[(startPos + 1) % len(self.lines)].y
            camY = curr_y + (next_y - curr_y) * percent
            camH = 1500 + camY
            camX = self.player_bike.x * 2000
            
            coin_line = self.lines[(startPos + 2) % len(self.lines)]
            if coin_line.sprite is not None and not coin_line.sprite_collected:
                height_ok = (self.player_bike.y > 1500) if coin_line.sprite_h > 0 else (self.player_bike.y < 3000)
                if abs(coin_line.spriteX - self.player_bike.x) < 0.4 and height_ok:
                    coin_line.sprite_collected = True
                    self.score += 10
                    self.collected_coins += 1
                    if self.coin_sound:
                        self.coin_sound.play()

            x, dx = 0, 0
            for n in range(302):
                idx = (startPos + n) % len(self.lines)
                l = self.lines[idx]
                l.x = x
                x += dx
                dx += l.curve
                loop_offset = self.track_length if (startPos + n) >= len(self.lines) else 0
                l.project(l.x - camX, camH, self.pos, loop_offset)
                
            maxy = HEIGHT
            for n in range(1, 300):
                idx = (startPos + n) % len(self.lines)
                prev_idx = (startPos + n - 1) % len(self.lines)
                l = self.lines[idx]
                p = self.lines[prev_idx]
                
                l.clip = maxy
                if l.Y >= maxy: 
                    continue
                
                color_idx = (idx // 3) % 2
                
                if self.level == 1:
                    grass, road = GRASS_LIGHT if color_idx else GRASS_DARK, ROAD_LIGHT if color_idx else ROAD_DARK
                elif self.level == 2:
                    grass, road = (255, 255, 255) if color_idx else (240, 240, 240), (220, 220, 220) if color_idx else (150, 150, 150)
                elif self.level == 4:
                    grass, road = (218, 165, 32) if color_idx else (184, 134, 11), (139, 69, 19) if color_idx else (101, 67, 33)
                elif self.level == 5:
                    if getattr(l, 'has_cave_tunnel', False):
                        grass, road = (8, 8, 12) if color_idx else (4, 4, 6), (45, 35, 25) if color_idx else (35, 25, 15)
                    else:
                        grass, road = (40, 40, 45) if color_idx else (25, 25, 30), (110, 85, 60) if color_idx else (85, 65, 45)
                elif self.level == 6:
                    grass, road = (244, 224, 172) if color_idx else (238, 214, 156), (220, 195, 140) if color_idx else (205, 180, 125)
                elif self.level == 7:
                    grass, road = (10, 30, 15) if color_idx else (5, 20, 10), (35, 30, 40) if color_idx else (25, 20, 30)
                elif self.level == 8:
                    if getattr(l, 'has_cave_tunnel', False):
                        grass, road = (30, 5, 0) if color_idx else (20, 3, 0), (60, 20, 5) if color_idx else (45, 15, 3)
                    else:
                        grass, road = (25, 25, 25) if color_idx else (15, 15, 15), (50, 35, 20) if color_idx else (40, 25, 15)
                elif self.level == 9:
                    colors_neon = [(255, 50, 50), (255, 150, 0), (255, 220, 0), (50, 200, 50), (0, 180, 255), (180, 50, 255)]
                    c = colors_neon[(idx // 2) % 6]
                    c_dark = (max(0, c[0]-50), max(0, c[1]-50), max(0, c[2]-50))
                    grass, road = (5, 5, 10), c if color_idx else c_dark
                else:
                    grass, road = (169, 169, 169) if color_idx else (150, 150, 150), (100, 100, 100) if color_idx else (80, 80, 80)
                
                pygame.draw.rect(self.screen, grass, (0, l.Y, WIDTH, max(1, p.Y - l.Y)))
                
                if self.level == 3:
                    sea = (28, 107, 160) if color_idx else (20, 90, 140)
                    pygame.draw.polygon(self.screen, sea, [(0, p.Y), (p.X - p.W - 50 * p.scale * 2000, p.Y), (l.X - l.W - 50 * l.scale * 2000, l.Y), (0, l.Y)])
                elif self.level == 6:
                    sea = (0, 180, 210) if color_idx else (0, 160, 190)
                    if (idx // 120) % 2 == 0:
                        pygame.draw.polygon(self.screen, sea, [(0, p.Y), (p.X - p.W - 40 * p.scale * 2000, p.Y), (l.X - l.W - 40 * l.scale * 2000, l.Y), (0, l.Y)])
                    else:
                        pygame.draw.polygon(self.screen, sea, [(WIDTH, p.Y), (p.X + p.W + 40 * p.scale * 2000, p.Y), (l.X + l.W + 40 * l.scale * 2000, l.Y), (WIDTH, l.Y)])
                
                if self.level in [2, 3, 4, 5, 6, 7, 8, 9]:
                    if self.level == 2:   rumble = (255, 0, 0) if color_idx else (200, 0, 0)
                    elif self.level == 4: rumble = (210, 180, 140) if color_idx else (160, 82, 45)
                    elif self.level == 5: rumble = (186, 85, 211) if color_idx else (0, 255, 255)
                    elif self.level == 6: rumble = (255, 255, 255) if color_idx else (0, 191, 255)
                    elif self.level == 7: rumble = (200, 200, 200) if color_idx else (80, 80, 80)
                    elif self.level == 8: rumble = (255, 80, 0) if color_idx else (180, 40, 0)
                    elif self.level == 9: rumble = (255, 255, 255) if color_idx else (100, 100, 100)
                    else:                 rumble = (255, 255, 255) if color_idx else (255, 0, 0)
                    self.draw_quad(rumble, p.X, p.Y, p.W * 1.15, l.X, l.Y, l.W * 1.15)
                    
                self.draw_quad(road, p.X, p.Y, p.W, l.X, l.Y, l.W)
                maxy = l.Y

            # --- 5. RENDER DEGLI SPRITE IN TECNICA PAINTER'S ALGORITHM ---
            for n in range(299, 0, -1):
                idx = (startPos + n) % len(self.lines)
                l = self.lines[idx]
                
                if getattr(l, 'has_cave_tunnel', False) and n > 1:
                    p_line = self.lines[(idx - 1) % len(self.lines)]
                    if l.Y < l.clip:
                        c_col = l.cave_tunnel_color
                        c_col_d = (max(0, c_col[0]-12), max(0, c_col[1]-12), max(0, c_col[2]-12))
                        sx1 = (1 + l.scale * (l.x - 2400 - camX)) * WIDTH / 2
                        sx2 = (1 + l.scale * (l.x + 2400 - camX)) * WIDTH / 2
                        sy_top = l.Y - l.scale * 2200 * HEIGHT / 2
                        px1 = (1 + p_line.scale * (p_line.x - 2400 - camX)) * WIDTH / 2
                        px2 = (1 + p_line.scale * (p_line.x + 2400 - camX)) * WIDTH / 2
                        py_top = p_line.Y - p_line.scale * 2200 * HEIGHT / 2
                        pygame.draw.polygon(self.screen, c_col, [(px1, p_line.Y), (px1, py_top), (sx1, sy_top), (sx1, l.Y)])
                        pygame.draw.polygon(self.screen, c_col, [(px2, p_line.Y), (px2, py_top), (sx2, sy_top), (sx2, l.Y)])
                        pygame.draw.polygon(self.screen, c_col_d, [(px1, py_top), (px2, py_top), (sx2, sy_top), (sx1, sy_top)])

                if getattr(l, 'has_container', False) and n > 1:
                    p_line = self.lines[(idx - 1) % len(self.lines)]
                    if l.Y < l.clip:
                        c_col = l.container_color
                        c_col_d = (max(0, c_col[0]-40), max(0, c_col[1]-40), max(0, c_col[2]-40))
                        sx1 = (1 + l.scale * (l.x - 3000 - camX)) * WIDTH / 2
                        sx2 = (1 + l.scale * (l.x + 3000 - camX)) * WIDTH / 2
                        sy_top = l.Y - l.scale * 2500 * HEIGHT / 2
                        px1 = (1 + p_line.scale * (p_line.x - 3000 - camX)) * WIDTH / 2
                        px2 = (1 + p_line.scale * (p_line.x + 3000 - camX)) * WIDTH / 2
                        py_top = p_line.Y - p_line.scale * 2500 * HEIGHT / 2
                        pygame.draw.polygon(self.screen, c_col, [(px1, p_line.Y), (px1, py_top), (sx1, sy_top), (sx1, l.Y)])
                        pygame.draw.polygon(self.screen, c_col, [(px2, p_line.Y), (px2, py_top), (sx2, sy_top), (sx2, l.Y)])
                        pygame.draw.polygon(self.screen, c_col_d, [(px1, py_top), (px2, py_top), (sx2, sy_top), (sx1, sy_top)])

                if l.has_tree and l.Y < l.clip:
                    t_world_x = l.x + l.treeX * 2000
                    treeX = (1 + l.scale * (t_world_x - camX)) * WIDTH / 2
                    sc = l.scale * 800
                    
                    if self.level == 6:
                        u_type = getattr(l, 'urban_type', 'palm')
                        if u_type == 'palm':
                            tw, th = int(400 * sc), int(1300 * sc)
                            if tw > 0 and th > 0:
                                pygame.draw.polygon(self.screen, (139, 90, 43), [(treeX - tw//3, l.Y), (treeX + tw//3, l.Y), (treeX + tw//6 - tw//12, l.Y - th), (treeX - tw//6 - tw//12, l.Y - th)])
                                for angle in [-40, -15, 15, 40]:
                                    rad = math.radians(angle)
                                    fx = treeX - tw//12 + int(math.sin(rad) * 600 * sc)
                                    fy = l.Y - th - int(math.cos(rad) * 200 * sc)
                                    pygame.draw.ellipse(self.screen, (34, 139, 34), (min(treeX, fx), min(l.Y - th, fy), abs(treeX - fx) + 20, 80 * sc))
                        elif u_type == 'umbrella':
                            uw, uh = int(900 * sc), int(1100 * sc)
                            if uw > 0 and uh > 0:
                                pygame.draw.rect(self.screen, (200, 200, 200), (treeX - int(15*sc), l.Y - uh, int(30*sc), uh))
                                red_d, yel_d = [], []
                                for step in range(17):
                                    ang = math.radians(180 + (180 / 16) * step)
                                    red_d.append((treeX + int(math.cos(ang) * (uw // 2)), l.Y - uh + int(math.sin(ang) * (150 * sc))))
                                    yel_d.append((treeX + int(math.cos(ang) * (uw // 3)), l.Y - uh + int(math.sin(ang) * (100 * sc))))
                                pygame.draw.polygon(self.screen, (255, 60, 60), red_d)
                                pygame.draw.polygon(self.screen, (255, 230, 50), yel_d)
                        elif u_type == 'sunbed':
                            lw, lh = int(800 * sc), int(250 * sc)
                            if lw > 0 and lh > 0:
                                pygame.draw.rect(self.screen, (230, 230, 230), (treeX - lw//2, l.Y - lh, lw, lh), border_radius=int(10*sc))
                                pygame.draw.rect(self.screen, (0, 191, 255), (treeX - lw//2 + int(10*sc), l.Y - lh + int(10*sc), lw - int(20*sc), lh - int(20*sc)), border_radius=int(6*sc))
                                pygame.draw.polygon(self.screen, (0, 170, 230), [(treeX - lw//2 + int(10*sc), l.Y - lh), (treeX - lw//2 + int(150*sc), l.Y - lh - int(120*sc)), (treeX - lw//2 + int(170*sc), l.Y - lh)])
                        elif u_type == 'sandcastle':
                            sw, sh = int(700 * sc), int(600 * sc)
                            if sw > 0 and sh > 0:
                                pygame.draw.rect(self.screen, (225, 195, 130), (treeX - sw//6, l.Y - sh, sw//3, sh))
                                pygame.draw.rect(self.screen, (215, 185, 120), (treeX - sw//2, l.Y - int(sh*0.6), sw//4, int(sh*0.6)))
                                pygame.draw.rect(self.screen, (215, 185, 120), (treeX + sw//4, l.Y - int(sh*0.6), sw//4, int(sh*0.6)))
                                pygame.draw.rect(self.screen, (190, 160, 100), (treeX - sw//6, l.Y - sh - int(40*sc), sw//12, int(40*sc)))
                                pygame.draw.rect(self.screen, (190, 160, 100), (treeX + sw//12 - sw//24, l.Y - sh - int(40*sc), sw//12, int(40*sc)))
                                pygame.draw.rect(self.screen, (50, 50, 50), (treeX - int(5*sc), l.Y - sh - int(160*sc), int(10*sc), int(160*sc)))
                                pygame.draw.polygon(self.screen, (255, 50, 50), [(treeX + int(5*sc), l.Y - sh - int(160*sc)), (treeX + int(120*sc), l.Y - sh - int(120*sc)), (treeX + int(5*sc), l.Y - sh - int(80*sc))])
                                
                    elif self.level == 5:
                        u_type = getattr(l, 'urban_type', 'crystal_purple')
                        if u_type.startswith('crystal_'):
                            c_theme = u_type.split('_')[1]
                            c_dark, c_light = ((139, 0, 139), (224, 86, 253)) if c_theme == 'purple' else (((0, 139, 139), (0, 255, 255)) if c_theme == 'cyan' else ((0, 100, 0), (50, 255, 50)))
                            ch, cw = 1000 * sc, 200 * sc
                            if ch > 0 and cw > 0:
                                pygame.draw.polygon(self.screen, c_dark, [(treeX, l.Y - ch), (treeX - cw, l.Y - ch//2), (treeX, l.Y)])
                                pygame.draw.polygon(self.screen, c_light, [(treeX, l.Y - ch), (treeX + cw, l.Y - ch//2), (treeX, l.Y)])
                            ch_l, cw_l = 700 * sc, 150 * sc
                            if ch_l > 0 and cw_l > 0:
                                pygame.draw.polygon(self.screen, c_dark, [(treeX - 100 * sc - cw_l, l.Y - ch_l), (treeX - cw_l * 2, l.Y - ch_l//2), (treeX, l.Y)])
                                pygame.draw.polygon(self.screen, c_light, [(treeX - 100 * sc - cw_l, l.Y - ch_l), (treeX - 50 * sc, l.Y - ch_l//2), (treeX, l.Y)])
                            ch_r, cw_r = 750 * sc, 160 * sc
                            if ch_r > 0 and cw_r > 0:
                                pygame.draw.polygon(self.screen, c_dark, [(treeX + 100 * sc + cw_r, l.Y - ch_r), (treeX + 50 * sc, l.Y - ch_r//2), (treeX, l.Y)])
                                pygame.draw.polygon(self.screen, c_light, [(treeX + 100 * sc + cw_r, l.Y - ch_r), (treeX + cw_r * 2, l.Y - ch_r//2), (treeX, l.Y)])
                        elif u_type == 'stalagmite':
                            sh, sw = 1200 * sc, 400 * sc
                            if sh > 0 and sw > 0:
                                pygame.draw.polygon(self.screen, (80, 80, 85), [(treeX, l.Y - sh), (treeX - sw, l.Y), (treeX + sw, l.Y)])
                                pygame.draw.polygon(self.screen, (110, 110, 115), [(treeX, l.Y - sh), (treeX, l.Y), (treeX + sw, l.Y)])
                                pygame.draw.polygon(self.screen, (60, 60, 65), [(treeX - sw//2, l.Y - sh//3), (treeX - sw * 1.2, l.Y), (treeX, l.Y)])
                        elif u_type == 'minecart':
                            mw, mh, ty = 900 * sc, 500 * sc, l.Y - 120 * sc
                            gems_c = [(255, 0, 0), (0, 255, 255), (186, 85, 211), (50, 255, 50), (255, 215, 0)]
                            for k in range(5):
                                pygame.draw.ellipse(self.screen, gems_c[k % len(gems_c)], (treeX - mw//3 + k * (mw//5) - int(60*sc), ty - mh + (10 if k % 2 == 0 else -10) * sc, int(120*sc), int(120*sc)))
                            if mw > 0 and mh > 0:
                                pygame.draw.rect(self.screen, (101, 67, 33), (treeX - mw//2, ty - mh, mw, mh), border_radius=max(1, int(10*sc)))
                                pygame.draw.rect(self.screen, (60, 60, 60), (treeX - mw//2, ty - mh, mw, mh), max(1, int(30 * sc)), border_radius=max(1, int(10*sc)))
                                pygame.draw.circle(self.screen, (50, 50, 50), (int(treeX - mw//3), int(l.Y - 80 * sc)), int(140 * sc))
                                pygame.draw.circle(self.screen, (150, 150, 150), (int(treeX - mw//3), int(l.Y - 80 * sc)), int(70 * sc))
                                pygame.draw.circle(self.screen, (50, 50, 50), (int(treeX + mw//3), int(l.Y - 80 * sc)), int(140 * sc))
                                pygame.draw.circle(self.screen, (150, 150, 150), (int(treeX + mw//3), int(l.Y - 80 * sc)), int(70 * sc))
                                
                    elif self.level == 4:
                        u_type = getattr(l, 'urban_type', 'baobab')
                        if u_type == 'baobab':
                            tw, th = int(800 * sc), int(1400 * sc)
                            if tw > 0 and th > 0:
                                pygame.draw.rect(self.screen, (101, 67, 33), (treeX - tw//4, l.Y - th, tw//2, th))
                                pygame.draw.ellipse(self.screen, (34, 139, 34), (treeX - tw, l.Y - th - th//4, tw*2, th//2))
                        elif u_type == 'hut':
                            hw, hh = int(1000 * sc), int(800 * sc)
                            if hw > 0 and hh > 0:
                                pygame.draw.rect(self.screen, (210, 180, 140), (treeX - hw//2, l.Y - hh//2, hw, hh//2))
                                pygame.draw.polygon(self.screen, (218, 165, 32), [(treeX - hw//2 - int(50*sc), l.Y - hh//2), (treeX + hw//2 + int(50*sc), l.Y - hh//2), (treeX, l.Y - hh)])
                                pygame.draw.rect(self.screen, (101, 67, 33), (treeX - hw//6, l.Y - hh//3, hw//3, hh//3))
                        elif u_type == 'animal':
                            aw, ah = int(600 * sc), int(1000 * sc)
                            if aw > 0 and ah > 0:
                                pygame.draw.rect(self.screen, (255, 200, 50), (treeX - aw//3, l.Y - ah//2, aw//8, ah//2))
                                pygame.draw.rect(self.screen, (255, 200, 50), (treeX + aw//4, l.Y - ah//2, aw//8, ah//2))
                                pygame.draw.rect(self.screen, (255, 200, 50), (treeX - aw//2, l.Y - ah, aw, ah//2))
                                pygame.draw.rect(self.screen, (255, 200, 50), (treeX + aw//4, l.Y - int(ah*1.5), aw//4, ah))
                                pygame.draw.rect(self.screen, (255, 200, 50), (treeX + aw//4, l.Y - int(ah*1.5), int(aw/1.5), aw//3))
                                
                    elif self.level == 3:
                        u_type = getattr(l, 'urban_type', 'tree')
                        if u_type == 'car':
                            cw, ch = int(1200 * sc), int(500 * sc)
                            if cw > 0 and ch > 0:
                                pygame.draw.rect(self.screen, (150, 150, 150), (treeX - cw//4, l.Y - int(ch*1.5), cw//2, int(ch*0.7)))
                                pygame.draw.rect(self.screen, (200, 50, 50) if idx % 2 == 0 else (50, 50, 200), (treeX - cw//2, l.Y - ch, cw, ch))
                        elif u_type == 'truck':
                            cw, ch = int(1600 * sc), int(1000 * sc)
                            if cw > 0 and ch > 0:
                                pygame.draw.rect(self.screen, (220, 220, 220), (treeX - cw//2, l.Y - ch, cw, ch))
                                pygame.draw.rect(self.screen, (50, 100, 200), (treeX + cw//2, l.Y - int(ch*0.6), cw//4, int(ch*0.6)))
                        elif u_type == 'house':
                            hw, hh = int(1200 * sc), int(1200 * sc)
                            if hw > 0 and hh > 0:
                                pygame.draw.rect(self.screen, (220, 180, 140) if idx % 2 == 0 else (180, 200, 220), (treeX - hw//2, l.Y - hh, hw, hh))
                                pygame.draw.polygon(self.screen, (150, 50, 50), [(treeX - hw//2 - hw//4, l.Y - hh), (treeX + hw//2 + hw//4, l.Y - hh), (treeX, l.Y - hh - hw//2)])
                        else:
                            tw, th = int(600 * sc), int(1200 * sc)
                            if tw > 0 and th > 0:
                                pygame.draw.rect(self.screen, (101, 67, 33), (treeX - tw//6, l.Y - th, tw//3, th))
                                pygame.draw.polygon(self.screen, (34, 139, 34), [(treeX, l.Y - th * 1.5), (treeX - tw//2, l.Y - th//2), (treeX + tw//2, l.Y - th//2)])
                                
                    elif self.level == 7:
                        u_type = getattr(l, 'urban_type', 'pine')
                        if u_type == 'pine':
                            tw, th = int(700 * sc), int(1600 * sc)
                            if tw > 0 and th > 0:
                                pygame.draw.rect(self.screen, (40, 20, 10), (treeX - tw//8, l.Y - th, tw//4, th))
                                pygame.draw.polygon(self.screen, (10, 50, 20), [(treeX, l.Y - th * 1.5), (treeX - tw//2, l.Y - th//2), (treeX + tw//2, l.Y - th//2)])
                                pygame.draw.polygon(self.screen, (5, 40, 15), [(treeX, l.Y - th * 1.1), (treeX - tw//2.2, l.Y - th//4), (treeX + tw//2.2, l.Y - th//4)])
                                
                    elif self.level == 8:
                        u_type = getattr(l, 'urban_type', 'lava_rock')
                        if u_type == 'lava_rock':
                            rw, rh = int(600 * sc), int(500 * sc)
                            if rw > 0 and rh > 0:
                                # Roccia vulcanica scura e frastagliata
                                pygame.draw.polygon(self.screen, (40, 30, 25), [
                                    (treeX - rw//2, l.Y),
                                    (treeX - rw//3, l.Y - rh),
                                    (treeX, l.Y - rh * 1.2),
                                    (treeX + rw//4, l.Y - rh * 0.9),
                                    (treeX + rw//2, l.Y)
                                ])
                                # Venature di lava incandescente
                                pygame.draw.line(self.screen, (255, 80, 0), (int(treeX - rw//4), int(l.Y - rh * 0.3)), (int(treeX), int(l.Y - rh * 0.8)), max(1, int(3 * sc)))
                                pygame.draw.line(self.screen, (255, 120, 0), (int(treeX + rw//6), int(l.Y - rh * 0.2)), (int(treeX + rw//4), int(l.Y - rh * 0.7)), max(1, int(2 * sc)))
                        elif u_type == 'lava_geyser':
                            gw, gh = int(300 * sc), int(1200 * sc)
                            if gw > 0 and gh > 0:
                                # Base del geyser
                                pygame.draw.ellipse(self.screen, (60, 30, 10), (treeX - gw, l.Y - gw//2, gw * 2, gw))
                                # Colonna di lava/fuoco
                                pygame.draw.polygon(self.screen, (255, 100, 0), [
                                    (treeX - gw//3, l.Y - gw//4),
                                    (treeX - gw//6, l.Y - gh),
                                    (treeX + gw//6, l.Y - gh),
                                    (treeX + gw//3, l.Y - gw//4)
                                ])
                                # Nucleo più chiaro
                                pygame.draw.polygon(self.screen, (255, 200, 50), [
                                    (treeX - gw//6, l.Y - gw//4),
                                    (treeX - gw//10, l.Y - gh * 0.8),
                                    (treeX + gw//10, l.Y - gh * 0.8),
                                    (treeX + gw//6, l.Y - gw//4)
                                ])
                        elif u_type == 'dead_tree':
                            tw, th = int(400 * sc), int(1000 * sc)
                            if tw > 0 and th > 0:
                                # Tronco morto carbonizzato
                                pygame.draw.rect(self.screen, (30, 20, 15), (treeX - tw//8, l.Y - th, tw//4, th))
                                # Rami secchi
                                pygame.draw.line(self.screen, (35, 25, 15), (int(treeX), int(l.Y - th * 0.8)), (int(treeX - tw//2), int(l.Y - th * 1.1)), max(1, int(4 * sc)))
                                pygame.draw.line(self.screen, (35, 25, 15), (int(treeX), int(l.Y - th * 0.6)), (int(treeX + tw//2.5), int(l.Y - th * 0.9)), max(1, int(3 * sc)))
                                pygame.draw.line(self.screen, (30, 20, 12), (int(treeX), int(l.Y - th * 0.5)), (int(treeX - tw//3), int(l.Y - th * 0.7)), max(1, int(2 * sc)))
                                
                    else:
                        tw, th = int(600 * sc), int(1200 * sc)
                        if tw > 0 and th > 0:
                            pygame.draw.rect(self.screen, (101, 67, 33), (treeX - tw//6, l.Y - th, tw//3, th))
                            t_color = (34, 139, 34) if self.level == 1 else (240, 248, 255)
                            pygame.draw.polygon(self.screen, t_color, [(treeX, l.Y - th * 1.5), (treeX - tw//2, l.Y - th//2), (treeX + tw//2, l.Y - th//2)])

                # Disegno delle Moto dei Bot Rivali
                for bot in self.bots:
                    if int(bot['pos'] / SEGMENT_LENGTH) % len(self.lines) == idx:
                        b_seg = int(bot['pos'] / SEGMENT_LENGTH) % len(self.lines)
                        p1 = self.lines[b_seg]
                        p2 = self.lines[(b_seg + 1) % len(self.lines)]
                        b_pct = (bot['pos'] % SEGMENT_LENGTH) / SEGMENT_LENGTH
                        bot_scale = p1.scale + (p2.scale - p1.scale) * b_pct
                        bot_Y = p1.Y + (p2.Y - p1.Y) * b_pct
                        
                        if bot_Y < p1.clip:
                            bx1 = (1 + p1.scale * (p1.x + bot['x'] * 2000 - camX)) * WIDTH / 2
                            bx2 = (1 + p2.scale * (p2.x + bot['x'] * 2000 - camX)) * WIDTH / 2
                            bot_X = bx1 + (bx2 - bx1) * b_pct
                            bot_img = self.bike_assets.get(bot['color'], {}).get('back')
                            if bot_img:
                                # Calcoliamo bw e bh scalando la dimensione reale dell'immagine
                                bw = int(bot_img.get_width() * bot_scale * 1500)
                                bh = int(bot_img.get_height() * bot_scale * 1500)
                                
                                # Limite massimo per evitare distorsioni se troppo vicini
                                if bw > int(WIDTH * 2):
                                    aspect = bh / bw
                                    bw = int(WIDTH * 2)
                                    bh = int(bw * aspect)
                                    
                                if bw > 0 and bh > 0:
                                    scaled_b = pygame.transform.scale(bot_img, (bw, bh))
                                    self.screen.blit(scaled_b, (bot_X - bw/2, bot_Y - bh))

                if l.sprite is not None and not l.sprite_collected and l.Y < l.clip:
                    spriteX = (1 + l.scale * (l.x + l.spriteX * 2000 - camX)) * WIDTH / 2
                    spriteY = l.Y - l.scale * l.sprite_h * HEIGHT / 2
                    sw = int(l.sprite.get_width() * l.scale * 1500)
                    sh = int(l.sprite.get_height() * l.scale * 1500)
                    if sw > 0 and sh > 0:
                        scaled_s = pygame.transform.scale(l.sprite, (sw, sh))
                        self.screen.blit(scaled_s, (spriteX - sw/2, spriteY - sh))

                if getattr(l, 'has_arch', False) and l.Y < l.clip:
                    for col in range(10):
                        for row in range(8):
                            if not ((col == 0 or col == 9) and row < 6) and not (row >= 6): 
                                continue
                            if getattr(l, 'arch_text', 'START') == 'AMEDEO':
                                rainbow = [(255, 50, 50), (255, 150, 0), (255, 220, 0), (50, 200, 50), (0, 180, 255), (180, 50, 255)]
                                color = rainbow[(col + row) % len(rainbow)]
                            else:
                                color = (0, 0, 0) if (col + row) % 2 == 0 else (255, 255, 255)
                                
                            sx1 = (1 + l.scale * (l.x - 2500 + col * 500 - camX)) * WIDTH / 2
                            sx2 = (1 + l.scale * (l.x - 2500 + col * 500 + 500 - camX)) * WIDTH / 2
                            sy_b = l.Y - l.scale * (row * 500) * HEIGHT / 2
                            sy_t = l.Y - l.scale * (row * 500 + 500) * HEIGHT / 2
                            rw, rh = sx2 - sx1, sy_b - sy_t
                            if rw > 0 and rh > 0:
                                pygame.draw.rect(self.screen, color, (sx1, sy_t, rw + 1, rh + 1))
                                
                    cx = (1 + l.scale * (l.x - camX)) * WIDTH / 2
                    cy = l.Y - l.scale * 2700 * HEIGHT / 2  # Abbassato nel vano dell'arco per non farlo sparire in alto
                    text_sw = int(l.scale * 2200 * WIDTH / 2) # Ottimizzato per renderlo leggibile e proporzionato
                    if 0 < text_sw < WIDTH * 5:
                        txt_type = getattr(l, 'arch_text', 'START')
                        t_img = self.arch_text_imgs.get(txt_type, self.arch_text_imgs['START'])
                        text_sh = int(text_sw * t_img.get_height() / t_img.get_width())
                        if text_sh > 0:
                            scaled_t = pygame.transform.scale(t_img, (text_sw, text_sh))
                            self.screen.blit(scaled_t, (cx - text_sw/2, cy - text_sh/2))

            # --- 6. DISEGNO DEL GIOCATORE UMANO ---
            tilt = 25 if keys[pygame.K_LEFT] else (-25 if keys[pygame.K_RIGHT] else 0)
            bike_base_img = self.bike_assets.get(self.player_color, {}).get('back', self.bike_back_img)
            
            if self.player_bike.is_flipping:
                bike_render_img = pygame.transform.rotate(bike_base_img, self.player_bike.flip_angle)
            elif tilt != 0:
                bike_render_img = pygame.transform.rotate(bike_base_img, tilt)
            else:
                bike_render_img = bike_base_img
                
            bw, bh = bike_render_img.get_width(), bike_render_img.get_height()
            screen_bike_y = HEIGHT - bh - 60 - (self.player_bike.y * 0.15)
            self.screen.blit(bike_render_img, (WIDTH / 2 - bw / 2, screen_bike_y))

            # --- 7. APPLICAZIONE INTERFACCIA HUD E LEADERBOARD LIVE ---
            self.ui.draw_hud(self.screen, self.lap, self.max_laps, self.score, self.bravo_timer, self.collected_coins, self.total_coins)
            if self.bravo_timer > 0:
                self.bravo_timer -= 1
                
            live_list = []
            live_list.append({'name': 'TU', 'color': self.player_color, 'dist': (self.lap - 1) * self.track_length + self.pos, 'is_player': True})
            for bot in self.bots:
                b_dist = (bot.get('lap', 1) - 1) * self.track_length + bot['pos']
                c_name = {'red':'ROSSA','green':'VERDE','blue':'BLU'}.get(bot['color'], bot['color'].upper())
                live_list.append({'name': c_name, 'color': bot['color'], 'dist': b_dist, 'is_player': False})
            live_list.sort(key=lambda x: x['dist'], reverse=True)
            self.ui.draw_live_leaderboard(self.screen, live_list)

            pygame.display.flip()
            self.clock.tick(FPS)

        if self.engine_sound:
            self.engine_sound.stop()
        pygame.quit()