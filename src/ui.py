# src/ui.py
import pygame
from src.config import WIDTH, HEIGHT, SKY_COLOR, GRASS_DARK, TEXT_COLOR

class UIManager:
    def __init__(self):
        # Inizializzazione Font di Sistema a varie scale
        self.font = pygame.font.SysFont(None, 48)
        self.score_font = pygame.font.SysFont(None, 72)
        self.bravo_font = pygame.font.SysFont(None, 120, bold=True)
        self.leaderboard_title_font = pygame.font.SysFont(None, 36, bold=True)
        self.leaderboard_font = pygame.font.SysFont(None, 32, bold=True)
        
        # Dizionario per memorizzare le mini-icone della classifica in tempo reale
        self.leaderboard_icons = {}

    def init_leaderboard_icons(self, bike_assets):
        """Genera e memorizza le icone in miniatura (retro della moto) per la classifica"""
        for color in ['red', 'green', 'blue']:
            back_img = bike_assets[color]['back']
            self.leaderboard_icons[color] = pygame.transform.smoothscale(back_img, (40, 56))

    def draw_splash(self, screen, bike_side_img):
        """Disegna la schermata di avvio del gioco (Splash Screen)"""
        screen.fill(SKY_COLOR)
        
        # Sfondo erba decorativo inferiore
        pygame.draw.rect(screen, GRASS_DARK, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
        
        # Disegna la moto al centro
        screen.blit(bike_side_img, (WIDTH // 2 - bike_side_img.get_width() // 2, HEIGHT // 2 - bike_side_img.get_height() // 2 - 50))
        
        # Titolo Principale con effetto Ombra portante
        title = self.font.render("MOTOCROSS 3D", True, (255, 215, 0))
        title_shadow = self.font.render("MOTOCROSS 3D", True, (0, 0, 0))
        screen.blit(title_shadow, (WIDTH // 2 - title.get_width() // 2 + 3, 153))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
        
        # Prompt di avvio lampeggiante o fisso
        prompt = self.font.render("Premi un tasto per iniziare", True, TEXT_COLOR)
        prompt_shadow = self.font.render("Premi un tasto per iniziare", True, (0, 0, 0))
        screen.blit(prompt_shadow, (WIDTH // 2 - prompt.get_width() // 2 + 3, HEIGHT - 147))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT - 150))

    def draw_select_bike(self, screen, selected_idx, bike_assets):
        """Disegna la schermata di selezione del colore della moto"""
        # Sostituito il fill nero con lo sfondo iniziale (Cielo azzurro)
        screen.fill(SKY_COLOR)
        
        # Sfondo erba decorativo inferiore (Prato verde)
        pygame.draw.rect(screen, GRASS_DARK, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
        
        title = self.font.render("SCEGLI LA TUA MOTO", True, (255, 215, 0))
        title_shadow = self.font.render("SCEGLI LA TUA MOTO", True, (0, 0, 0))
        screen.blit(title_shadow, (WIDTH // 2 - title.get_width() // 2 + 3, 103))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        bw, bh = 320, 240
        red_side = pygame.transform.smoothscale(bike_assets['red']['side'], (bw, bh))
        green_side = pygame.transform.smoothscale(bike_assets['green']['side'], (bw, bh))
        blue_side = pygame.transform.smoothscale(bike_assets['blue']['side'], (bw, bh))
        
        # Evidenzia la moto attualmente selezionata con un rettangolo dorato di sfondo
        y_box = HEIGHT // 2 - bh // 2 - 20
        if selected_idx == 0:
            pygame.draw.rect(screen, (60, 20, 20), (WIDTH // 4 - bw // 2 - 20, y_box, bw + 40, bh + 80), border_radius=15)
            pygame.draw.rect(screen, (255, 215, 0), (WIDTH // 4 - bw // 2 - 20, y_box, bw + 40, bh + 80), width=3, border_radius=15)
        elif selected_idx == 1:
            pygame.draw.rect(screen, (20, 50, 20), (WIDTH // 2 - bw // 2 - 20, y_box, bw + 40, bh + 80), border_radius=15)
            pygame.draw.rect(screen, (255, 215, 0), (WIDTH // 2 - bw // 2 - 20, y_box, bw + 40, bh + 80), width=3, border_radius=15)
        elif selected_idx == 2:
            pygame.draw.rect(screen, (20, 20, 60), (3 * WIDTH // 4 - bw // 2 - 20, y_box, bw + 40, bh + 80), border_radius=15)
            pygame.draw.rect(screen, (255, 215, 0), (3 * WIDTH // 4 - bw // 2 - 20, y_box, bw + 40, bh + 80), width=3, border_radius=15)
            
        screen.blit(red_side, (WIDTH // 4 - bw // 2, HEIGHT // 2 - bh // 2))
        screen.blit(green_side, (WIDTH // 2 - bw // 2, HEIGHT // 2 - bh // 2))
        screen.blit(blue_side, (3 * WIDTH // 4 - bw // 2, HEIGHT // 2 - bh // 2))
        
        y_pos = HEIGHT // 2 + bh // 2 + 10
        t1 = self.font.render("ROSSA", True, (255, 50, 50))
        t2 = self.font.render("VERDE", True, (50, 255, 50))
        t3 = self.font.render("BLU", True, (50, 100, 255))
        
        screen.blit(t1, (WIDTH // 4 - t1.get_width() // 2, y_pos))
        screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, y_pos))
        screen.blit(t3, (3 * WIDTH // 4 - t3.get_width() // 2, y_pos))
        
        prompt = self.font.render("Frecce: Muovi - INVIO: Scegli", True, TEXT_COLOR)
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT - 70))

    def draw_hud(self, screen, lap, max_laps, score, bravo_timer, collected_coins=0, total_coins=0, falling=False, lost_timer=0):
        """Disegna le informazioni di gioco in tempo reale (Giri, Punti e scritte d'azione)"""
        # Testo principale Giri e Punteggio nell'angolo in alto a sinistra
        ui_text = f"Giro: {lap}/{max_laps}   Punteggio: {score}"
        score_surf = self.score_font.render(ui_text, True, (255, 255, 255))
        score_shadow = self.score_font.render(ui_text, True, (0, 0, 0))
        screen.blit(score_shadow, (22, 22))
        screen.blit(score_surf, (20, 20))
        
        # --- NUOVO: Contatore Monete Dorato ---
        coin_text = f"Monete: {collected_coins} / {total_coins}"
        coin_surf = self.font.render(coin_text, True, (255, 215, 0))
        coin_shadow = self.font.render(coin_text, True, (0, 0, 0))
        screen.blit(coin_shadow, (22, 82))
        screen.blit(coin_surf, (20, 80))
        
        # Scritta lampeggiante "BRAVO! +10" in seguito a un flip andato a segno
        if bravo_timer > 0:
            color = (255, 215, 0) if (bravo_timer // 8) % 2 == 0 else (255, 140, 0)
            bravo_text = self.bravo_font.render("FLIP +10", True, color)
            bravo_shadow = self.bravo_font.render("FLIP +10", True, (0, 0, 0))
            
            bx = WIDTH // 2 - bravo_text.get_width() // 2
            by = HEIGHT // 4
            screen.blit(bravo_shadow, (bx + 5, by + 5))
            screen.blit(bravo_text, (bx, by))

        # Caduta nel vuoto (Livello Spazio): invito lampeggiante a saltare per tornare in pista
        if falling:
            color = (0, 255, 255) if (pygame.time.get_ticks() // 150) % 2 == 0 else (255, 255, 255)
            self._draw_center_message(screen, "SALTA!", color, HEIGHT // 3)
        elif lost_timer > 0:
            self._draw_center_message(screen, "PERSO NELLO SPAZIO! -10", (255, 60, 60), HEIGHT // 3)

    def _draw_center_message(self, screen, text, color, y):
        """Scritta grande centrata con ombra"""
        surf = self.bravo_font.render(text, True, color)
        shadow = self.bravo_font.render(text, True, (0, 0, 0))
        x = WIDTH // 2 - surf.get_width() // 2
        screen.blit(shadow, (x + 5, y + 5))
        screen.blit(surf, (x, y))

    def draw_live_leaderboard(self, screen, participants):
        """Disegna il widget trasparente della classifica live in alto a destra"""
        card_w, card_h = 320, 240
        card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        
        # Sfondo scuro semitrasparente con bordi arrotondati e cornice dorata lucida
        pygame.draw.rect(card, (20, 20, 20, 205), (0, 0, card_w, card_h), border_radius=15)
        pygame.draw.rect(card, (255, 215, 0, 160), (0, 0, card_w, card_h), width=2, border_radius=15)
        
        title_surf = self.leaderboard_title_font.render("CLASSIFICA", True, (255, 215, 0))
        card.blit(title_surf, (card_w // 2 - title_surf.get_width() // 2, 15))
        pygame.draw.line(card, (255, 215, 0, 100), (20, 50), (card_w - 20, 50), 1)
        
        start_y = 60
        row_h = 56
        for rank, p in enumerate(participants, 1):
            # Posizione (1°, 2°, 3°)
            rank_str = f"{rank}°"
            rank_color = (255, 215, 0) if rank == 1 else (200, 200, 200)
            rank_surf = self.leaderboard_font.render(rank_str, True, rank_color)
            card.blit(rank_surf, (20, start_y + (rank - 1) * row_h + 15))
            
            # Icona mini-moto associata
            icon_img = self.leaderboard_icons.get(p['color'])
            if icon_img:
                card.blit(icon_img, (65, start_y + (rank - 1) * row_h))
                
            # Nome Pilota evidenziato in giallo lucido per il giocatore umano
            name_color = (255, 255, 0) if p['is_player'] else TEXT_COLOR
            name_str = p['name']
            if p['is_player']:
                name_str += " (TU)"
            name_surf = self.leaderboard_font.render(name_str, True, name_color)
            card.blit(name_surf, (120, start_y + (rank - 1) * row_h + 15))
            
        screen.blit(card, (WIDTH - card_w - 20, 20))

    def draw_race_end(self, screen, level, final_standings, player_final_rank, collected_coins=0, total_coins=0):
        """Disegna l'intera interfaccia di fine gara con i risultati, la tabella e il podio 3D"""
        screen.fill((15, 15, 25))
        
        # Grande titolo superiore
        title_text = f"RISULTATI LIVELLO {level}"
        title_font = pygame.font.SysFont(None, 90, bold=True)
        title_surf = title_font.render(title_text, True, (255, 215, 0))
        title_shadow = title_font.render(title_text, True, (0, 0, 0))
        screen.blit(title_shadow, (WIDTH // 2 - title_surf.get_width() // 2 + 5, 65))
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 60))
        
        # Mostra le monete raccolte
        coin_font = pygame.font.SysFont(None, 60, bold=True)
        coin_text = f"Monete Raccolte: {collected_coins} / {total_coins}"
        coin_surf = coin_font.render(coin_text, True, (255, 215, 0))
        coin_shadow = coin_font.render(coin_text, True, (0, 0, 0))
        screen.blit(coin_shadow, (WIDTH // 2 - coin_surf.get_width() // 2 + 3, 143))
        screen.blit(coin_surf, (WIDTH // 2 - coin_surf.get_width() // 2, 140))
        
        # --- TABELLA RIASSUNTIVA A SINISTRA ---
        panel_w, panel_h = 550, 360
        panel_x = WIDTH // 2 - panel_w - 50
        panel_y = HEIGHT // 2 - panel_h // 2 - 40
        
        pygame.draw.rect(screen, (30, 30, 45), (panel_x, panel_y, panel_w, panel_h), border_radius=20)
        pygame.draw.rect(screen, (255, 215, 0), (panel_x, panel_y, panel_w, panel_h), width=4, border_radius=20)
        
        row_h = 95
        start_y = panel_y + 35
        for rank, p in enumerate(final_standings, 1):
            if p['is_player']:
                row_bg_color = (70, 55, 25) if rank <= 2 else (70, 25, 25)
                pygame.draw.rect(screen, row_bg_color, (panel_x + 15, start_y + (rank - 1) * row_h - 10, panel_w - 30, row_h - 10), border_radius=12)
                pygame.draw.rect(screen, (255, 215, 0), (panel_x + 15, start_y + (rank - 1) * row_h - 10, panel_w - 30, row_h - 10), width=2, border_radius=12)
            
            rank_str = f"{rank}°"
            rank_color = (255, 215, 0) if rank == 1 else ((220, 220, 220) if rank == 2 else (200, 120, 70))
            rank_f = pygame.font.SysFont(None, 48, bold=True)
            rank_surf = rank_f.render(rank_str, True, rank_color)
            screen.blit(rank_surf, (panel_x + 40, start_y + (rank - 1) * row_h + 15))
            
            icon_img = self.leaderboard_icons.get(p['color'])
            if icon_img:
                scaled_icon = pygame.transform.smoothscale(icon_img, (45, 63))
                screen.blit(scaled_icon, (panel_x + 130, start_y + (rank - 1) * row_h - 5))
            
            name_str = p['name']
            if p['is_player']:
                name_str += " (TU)"
            name_color = (255, 255, 0) if p['is_player'] else TEXT_COLOR
            name_f = pygame.font.SysFont(None, 40, bold=True)
            name_surf = name_f.render(name_str, True, name_color)
            screen.blit(name_surf, (panel_x + 210, start_y + (rank - 1) * row_h + 15))

        # --- DISEGNO DEL PODIO 3D A DESTRA ---
        podium_x = WIDTH // 2 + 100
        podium_y = HEIGHT // 2 + 100
        col_w = 120
        h1, h2, h3 = 180, 120, 70
        
        # Blocchi del Podio (2° Sinistra, 1° Centro, 3° Destra)
        pygame.draw.rect(screen, (40, 40, 55), (podium_x, podium_y - h2, col_w, h2), border_radius=8)
        pygame.draw.rect(screen, (192, 192, 192), (podium_x, podium_y - h2, col_w, h2), width=3, border_radius=8)
        
        pygame.draw.rect(screen, (50, 50, 70), (podium_x + col_w + 20, podium_y - h1, col_w, h1), border_radius=8)
        pygame.draw.rect(screen, (255, 215, 0), (podium_x + col_w + 20, podium_y - h1, col_w, h1), width=4, border_radius=8)
        
        pygame.draw.rect(screen, (30, 30, 45), (podium_x + 2 * col_w + 40, podium_y - h3, col_w, h3), border_radius=8)
        pygame.draw.rect(screen, (205, 127, 50), (podium_x + 2 * col_w + 40, podium_y - h3, col_w, h3), width=3, border_radius=8)
        
        font_num = pygame.font.SysFont(None, 64, bold=True)
        screen.blit(font_num.render("2", True, (192, 192, 192)), (podium_x + col_w // 2 - 15, podium_y - h2 + 20))
        screen.blit(font_num.render("1", True, (255, 215, 0)), (podium_x + col_w + 20 + col_w // 2 - 15, podium_y - h1 + 25))
        screen.blit(font_num.render("3", True, (205, 127, 50)), (podium_x + 2 * col_w + 40 + col_w // 2 - 15, podium_y - h3 + 15))
        
        # Posizionamento delle icone sopra i relativi blocchi del podio
        for rank, p in enumerate(final_standings, 1):
            icon_img = self.leaderboard_icons.get(p['color'])
            if icon_img:
                scaled_icon = pygame.transform.smoothscale(icon_img, (75, 105))
                if rank == 1:
                    screen.blit(scaled_icon, (podium_x + col_w + 20 + col_w // 2 - 37, podium_y - h1 - 100))
                elif rank == 2:
                    screen.blit(scaled_icon, (podium_x + col_w // 2 - 37, podium_y - h2 - 100))
                elif rank == 3:
                    screen.blit(scaled_icon, (podium_x + 2 * col_w + 40 + col_w // 2 - 37, podium_y - h3 - 100))
                    
        # --- MESSAGGI DI NOTIFICA E PROGRESSO ---
        msg_font = pygame.font.SysFont(None, 56, bold=True)
        prompt_font = pygame.font.SysFont(None, 44, bold=True)
        
        if player_final_rank <= 2:
            if level < 9:
                msg_text = f"COMPLIMENTI! TI SEI QUALIFICATO PER IL LIVELLO {level + 1}!"
                msg_color = (50, 255, 50)
                next_level_name = "Neve" if level == 1 else "Città" if level == 2 else "Africa" if level == 3 else "Miniera" if level == 4 else "Mare" if level == 5 else "Notte Foresta" if level == 6 else "Vulcano" if level == 7 else "Spazio"
                prompt_text = f"Premi SPAZIO o INVIO per iniziare il LIVELLO {level + 1} ({next_level_name})"
            else:
                msg_text = "CAMPIONE DEL MONDO E DELLO SPAZIO! HAI COMPLETATO IL GIOCO!"
                msg_color = (255, 215, 0)
                prompt_text = "Premi SPAZIO o INVIO per vedere i Titoli di Coda"
        else:
            msg_text = "PECCATO! NON TI SEI QUALIFICATO (Richiesto 1° o 2° posto)"
            msg_color = (255, 60, 60)
            prompt_text = "Premi SPAZIO o INVIO per Riprovare questo Livello"
            
        msg_surf = msg_font.render(msg_text, True, msg_color)
        msg_shadow = msg_font.render(msg_text, True, (0, 0, 0))
        screen.blit(msg_shadow, (WIDTH // 2 - msg_surf.get_width() // 2 + 3, panel_y + panel_h + 38))
        screen.blit(msg_surf, (WIDTH // 2 - msg_surf.get_width() // 2, panel_y + panel_h + 35))
        
        prompt_surf = prompt_font.render(prompt_text, True, (230, 230, 230))
        prompt_shadow = prompt_font.render(prompt_text, True, (0, 0, 0))
        screen.blit(prompt_shadow, (WIDTH // 2 - prompt_surf.get_width() // 2 + 2, panel_y + panel_h + 102))
        screen.blit(prompt_surf, (WIDTH // 2 - prompt_surf.get_width() // 2, panel_y + panel_h + 100))

    def draw_game_over(self, screen, score):
        """Disegna una schermata di Game Over rapida di fallback"""
        screen.fill((10, 10, 15))
        title = self.font.render("GARA TERMINATA!", True, (255, 215, 0))
        score_msg = self.font.render(f"Punteggio: {score}", True, TEXT_COLOR)
        prompt = self.font.render("Premi ESC per uscire o QUALSIASI TASTO per chiudere", True, (150, 150, 150))
        
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(score_msg, (WIDTH // 2 - score_msg.get_width() // 2, HEIGHT // 2))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 100))

    def draw_credits(self, screen, bg_space, bike_side, credits_y, score):
        """Disegna la schermata finale con testo scorrevole e moto che vola"""
        screen.blit(bg_space, (0, 0))
        
        # Moto che vola verso l'alto
        # La facciamo salire mentre i crediti scorrono
        bike_y = HEIGHT // 2 + min(0, credits_y - HEIGHT) * 1.5
        if bike_y > -400:
            rotated_bike = pygame.transform.rotozoom(bike_side, 45, 0.6)
            bx = WIDTH // 2 - rotated_bike.get_width() // 2
            screen.blit(rotated_bike, (bx, int(bike_y)))
            # Scia di fuoco
            pygame.draw.circle(screen, (255, 100, 0), (bx + 50, int(bike_y) + rotated_bike.get_height() - 20), 40)
            pygame.draw.circle(screen, (255, 200, 0), (bx + 30, int(bike_y) + rotated_bike.get_height() + 10), 25)

        # Testo di scorrimento stile Star Wars
        texts = [
            "EPISODIO FINALE",
            "IL TRIONFO DI AMEDEO",
            "",
            "Amedeo ha superato ogni ostacolo.",
            "Dalle cime innevate...",
            "Ai crateri vulcanici...",
            "Fino alle profondita' del cosmo!",
            "",
            f"PUNTEGGIO FINALE: {score}",
            "",
            "GRAZIE PER AVER GIOCATO!",
            "",
            "",
            "Premi SPAZIO per tornare al menu"
        ]
        
        font = pygame.font.SysFont(None, 72, bold=True)
        for i, line in enumerate(texts):
            if not line: continue
            surf = font.render(line, True, (255, 215, 0))
            shadow = font.render(line, True, (0, 0, 0))
            y_pos = credits_y + i * 80
            
            if -100 < y_pos < HEIGHT:
                # Piccolo effetto di trasparenza per farlo svanire in alto
                alpha = min(255, int((y_pos + 100) / 200 * 255))
                surf.set_alpha(alpha)
                shadow.set_alpha(alpha)
                screen.blit(shadow, (WIDTH // 2 - surf.get_width() // 2 + 4, int(y_pos) + 4))
                screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, int(y_pos)))