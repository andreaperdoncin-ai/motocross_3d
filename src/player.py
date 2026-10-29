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

        # Caduta nel vuoto (solo Livello Spazio): uscendo dalla pista si sprofonda sotto di essa
        self.can_fall = False
        self.is_falling = False
        self.fall_timer = 0       # Frame trascorsi nel vuoto
        self.is_recovering = False  # Salto di recupero in corso: spinge la moto verso la pista

    # Limiti laterali e parametri della caduta
    ROAD_EDGE = 1.15        # Oltre questo valore di x non c'è più pista sotto le ruote
    SPACE_MAX_X = 2.5       # Nello spazio si può sbandare ben oltre il bordo
    FALL_TERMINAL_SPEED = -30
    FALL_TIME_LIMIT = 120   # 2 secondi a 60 FPS, poi la moto viene recuperata con penalità

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
            
        # Restrizioni dei bordi esterni: nello spazio non ci sono barriere e si può finire nel vuoto
        max_x = self.SPACE_MAX_X if self.can_fall else 1.5
        self.x = max(-max_x, min(max_x, self.x))

        # Nel vuoto la moto non ha aderenza e perde metà della velocità
        if self.is_falling:
            self.speed *= 0.5

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

                # Se la moto si trova a terra (o sta cadendo nel vuoto), attiva la spinta del salto verticale
                if not self.is_jumping:
                    if self.is_falling:
                        # Salto di recupero: si risale e si viene spinti di nuovo sopra la pista
                        self.is_falling = False
                        self.fall_timer = 0
                        self.is_recovering = True
                    self.is_jumping = True
                    self.jump_velocity = self.jump_power  # Potenza di stacco verso l'alto

        return flipped

    def update_physics(self):
        """Aggiorna la gravità del salto e la rotazione del flip frame per frame.
        Restituisce True se la moto è rimasta troppo a lungo nel vuoto ed è stata recuperata."""
        if self.is_falling:
            # Sprofondamento lento nel vuoto, con gravità ridotta e velocità limite
            self.jump_velocity = max(self.FALL_TERMINAL_SPEED, self.jump_velocity - self.gravity * 0.5)
            self.y += self.jump_velocity
            self.fall_timer += 1
            if self.fall_timer >= self.FALL_TIME_LIMIT:
                self.reset_on_collision()
                self.x = 0
                return True
            return False

        # Sulla pista ma oltre il bordo: inizia la caduta
        if self.can_fall and not self.is_jumping and abs(self.x) > self.ROAD_EDGE:
            self.start_falling()
            return False

        if self.is_jumping:
            # Durante il salto di recupero la moto viene riportata verso la pista
            if self.is_recovering and abs(self.x) > 0.8:
                self.x -= 0.03 if self.x > 0 else -0.03

            self.y += self.jump_velocity
            self.jump_velocity -= self.gravity  # Effetto costante della forza di gravità
            
            if self.is_flipping:
                self.flip_angle -= 8  # Velocità angolare per compiere la rotazione di ~360°
                
            # Controllo dell'impatto di atterraggio al suolo (solo in discesa: il salto di recupero parte da sotto la pista)
            if self.y <= 0 and self.jump_velocity < 0:
                if self.can_fall and abs(self.x) > self.ROAD_EDGE:
                    # Si ricade fuori dalla pista: si prosegue nel vuoto mantenendo lo slancio
                    self.start_falling(keep_velocity=True)
                    return False
                self.y = 0
                self.is_jumping = False
                self.is_flipping = False
                self.flip_angle = 0
                self.is_recovering = False
        return False

    def start_falling(self, keep_velocity=False):
        """Fa precipitare la moto nel vuoto sotto la pista"""
        self.is_falling = True
        self.is_jumping = False
        self.is_flipping = False
        self.is_recovering = False
        self.flip_angle = 0
        self.fall_timer = 0
        if not keep_velocity:
            self.jump_velocity = 0

    def reset_on_collision(self):
        """Azzera i vettori di movimento e rimette in asse la moto dopo un incidente"""
        self.speed = 0
        self.y = 0
        self.is_jumping = False
        self.is_flipping = False
        self.flip_angle = 0
        self.is_falling = False
        self.is_recovering = False
        self.fall_timer = 0