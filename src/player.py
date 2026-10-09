# src/player.py
import pygame

class Player:
    def __init__(self, base_speed=5500):
        self.x = 0.0          # Posizione laterale sul tracciato (da -1.5 a 1.5)
        self.y = 0.0          # Altezza da terra (gestione del salto)
        self.speed = 0.0      # Velocità attuale della moto
        self.base_speed = base_speed
        
        # Stati della fisica dinamica
        self.is_jumping = False
        self.jump_velocity = 0
        self.is_flipping = False
        self.flip_angle = 0
        self.last_up_press_time = 0  # Temporizzatore per rilevare il doppio click
        
        # Fisica configurabile (per Livello Spazio)
        self.jump_power = 400
        self.gravity = 15
        
    def handle_input(self, keys):
        """Gestisce gli input continui della tastiera per accelerazione, freno e sterzo"""
        # Accelerazione base costante + spinta manuale (W) o freno (S / Freccia GIÙ)
        self.speed = self.base_speed
        if keys[pygame.K_w]:
            self.speed += 2500
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.speed -= 2500
            
        # Sterzo laterale e calcolo dell'effetto parallasse per lo sfondo del cielo
        sky_turn_offset = 0
        if keys[pygame.K_LEFT]:
            self.x -= 0.04
            sky_turn_offset = 4
        if keys[pygame.K_RIGHT]:
            self.x += 0.04
            sky_turn_offset = -4
            
        # Restrizioni dei bordi esterni della pista per non finire nel vuoto
        self.x = max(-1.5, min(1.5, self.x))
        
        return sky_turn_offset

    def handle_event(self, event):
        """Gestisce gli eventi singoli (pressione pulsanti) per attivare salti e flip"""
        flipped = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                current_time = pygame.time.get_ticks()
                
                # Rilevamento del doppio tap rapido sulla Freccia SU per attivare il Backflip
                if event.key == pygame.K_UP:
                    if current_time - self.last_up_press_time < 400:  # Finestra di 400ms
                        if self.is_jumping and not self.is_flipping:
                            self.is_flipping = True
                            self.flip_angle = 0
                            flipped = True  # Segnala al ciclo di gioco di assegnare i punti bonus
                    self.last_up_press_time = current_time

                # Se la moto si trova a terra, attiva la spinta del salto verticale
                if not self.is_jumping:
                    self.is_jumping = True
                    self.jump_velocity = self.jump_power  # Potenza di stacco verso l'alto
                    
        return flipped

    def update_physics(self):
        """Aggiorna la gravità del salto e la rotazione del flip frame per frame"""
        if self.is_jumping:
            self.y += self.jump_velocity
            self.jump_velocity -= self.gravity  # Effetto costante della forza di gravità
            
            if self.is_flipping:
                self.flip_angle -= 8  # Velocità angolare per compiere la rotazione di ~360°
                
            # Controllo dell'impatto di atterraggio al suolo
            if self.y <= 0:
                self.y = 0
                self.is_jumping = False
                self.is_flipping = False
                self.flip_angle = 0

    def reset_on_collision(self):
        """Azzera i vettori di movimento e rimette in asse la moto dopo un incidente"""
        self.speed = 0
        self.y = 0
        self.is_jumping = False
        self.is_flipping = False
        self.flip_angle = 0