# src/track.py
import math
import random
from src.config import WIDTH, HEIGHT, SEGMENT_LENGTH

class Line:
    def __init__(self, index):
        self.i = index
        self.x = 0  # Curva della strada
        self.y = 0  # Altezza (colline/avvallamenti)
        self.z = self.i * SEGMENT_LENGTH
        
        # Coordinate 2D proiettate sullo schermo
        self.X = 0
        self.Y = 0
        self.W = 0
        self.scale = 0
        self.clip = HEIGHT  # Gestione della visibilità degli sprite dietro le colline
        
        self.curve = 0
        self.sprite = None
        self.spriteX = 0
        self.sprite_h = 0
        self.sprite_collected = False
        
        # Elementi dello scenario
        self.has_tree = False
        self.treeX = 0
        self.has_arch = False
        self.arch_text = "START"
        self.has_container = False
        self.container_color = (0, 0, 0)
        self.has_cave_tunnel = False
        self.cave_tunnel_color = (0, 0, 0)
        self.urban_type = 'tree'
        
    def project(self, relX, camY, camZ, loop_offset):
        """Proietta le coordinate 3D del segmento nello spazio 2D dello schermo"""
        dz = self.z + loop_offset - camZ
        if dz <= 0.1: 
            dz = 0.1
        
        self.scale = 0.84 / dz
        self.X = (1 + self.scale * relX) * WIDTH / 2
        self.Y = (1 - self.scale * (self.y - camY)) * HEIGHT / 2
        self.W = self.scale * 2000 * WIDTH / 2


def generate_track(level, coin_img=None):
    """Genera i segmenti della pista in base al livello e al bioma selezionato"""
    lines = []
    is_level_3 = (level == 3)
    num_segments = 1500 if level == 8 else (1200 if level == 9 else 1000)
    
    for i in range(num_segments):
        line = Line(i)
        
        # 1. Configurazione Altezze e Curve in base al Livello (Bioma)
        if level == 9:
            # Level 9: Spazio (Onde enormi e lunghissime, zero ostacoli)
            line.y = math.sin(i / 25.0) * 3500 + math.cos(i / 15.0) * 800
            if 150 < i < 300: line.curve = 2.0
            if 400 < i < 550: line.curve = -2.5
            if 700 < i < 850: line.curve = 3.0
            if 950 < i < 1100: line.curve = -2.0
            
        elif level == 8:
            # Level 8: Vulcano (Curve aggressive, fiamme e lava, ma salti più morbidi e distanziati)
            line.y = math.sin(i / 25.0) * 1600 + math.cos(i / 12.0) * 500
            if 100 < i < 220: line.curve = 3.5
            if 280 < i < 400: line.curve = -4.0
            if 500 < i < 650: line.curve = 3.8
            if 700 < i < 850: line.curve = -3.5
            if 900 < i < 980: line.curve = 4.0
            
            # Tunnel di lava nella roccia vulcanica
            if 650 < i < 780:
                line.has_cave_tunnel = True
                line.cave_tunnel_color = (50, 10, 5) if (i // 4) % 2 == 0 else (35, 5, 0)
            
        elif level == 7:
            # Level 7: Notte Foresta (Colline fitte e percorsi sinuosi)
            line.y = math.sin(i / 14.0) * 1200 + math.cos(i / 7.0) * 350
            if 80 < i < 200: line.curve = 2.5
            if 250 < i < 400: line.curve = -3.0
            if 600 < i < 750: line.curve = 3.2
            if 800 < i < 950: line.curve = -2.8
            if 1050 < i < 1200: line.curve = 2.0
            
        elif level == 6:
            # Level 6: Spiaggia (Avvallamenti dolci sulla sabbia)
            line.y = math.sin(i / 20.0) * 400 + math.cos(i / 10.0) * 150
            if 150 < i < 280: line.curve = 1.8
            if 350 < i < 480: line.curve = -2.2
            if 600 < i < 750: line.curve = 2.0
            if 800 < i < 920: line.curve = -1.5
            
        elif level == 5:
            # Level 5: Miniera/Caverna (Terreno molto irregolare e accidentato)
            line.y = math.sin(i / 12.0) * 1200 + math.cos(i / 6.0) * 400
            if 120 < i < 220: line.curve = 3.0
            if 300 < i < 420: line.curve = -3.5
            if 550 < i < 680: line.curve = 2.8
            if 800 < i < 950: line.curve = -3.2
            if 1100 < i < 1250: line.curve = 3.5
            if 1300 < i < 1420: line.curve = -2.0
            
            # Tunnel della galleria sotterranea di roccia
            if 700 < i < 850:
                line.has_cave_tunnel = True
                line.cave_tunnel_color = (35, 35, 40) if (i // 4) % 2 == 0 else (25, 25, 30)
                
        elif is_level_3:
            # Level 3: Urbano/Industriale (Rampe artificiali sommate al terreno di base)
            line.y = math.sin(i / 15.0) * 500
            for ramp_start in (200, 380, 600):
                if ramp_start < i < ramp_start + 40:
                    line.y += math.sin((i - ramp_start) / 40.0 * math.pi) * 1400
                
            if 100 < i < 200: line.curve = 2.0
            if 300 < i < 400: line.curve = -2.5
            if 550 < i < 600: line.curve = 2.2
            if 700 < i < 800: line.curve = -2.0
            
            # Tunnel di Container
            if 750 < i < 850:
                line.has_container = True
                line.container_color = (180, 40, 40) if (i // 5) % 2 == 0 else (140, 30, 30)
                
        else:
            # Livelli Standard (1, 2, 4): Colline classiche pronunciate
            line.y = math.sin(i / 15.0) * 1800
            if 100 < i < 250: line.curve = 2.0
            if 350 < i < 500: line.curve = -2.5
            if 650 < i < 800: line.curve = 2.2
            if 950 < i < 1100: line.curve = -2.0
            if 1250 < i < 1400: line.curve = 2.5

        # --- RETTILINEO D'ONORE PER L'ARCO DI AMEDEO ---
        # Appiattiamo il terreno e raddrizziamo le curve progressivamente tra i segmenti 440 e 560.
        # Questo crea una pista d'atterraggio visiva perfetta per vedere l'arco da grandissima distanza!
        if level in [1, 2, 3, 4, 6, 7, 8, 9] and (440 <= i <= 560):
            distanza = abs(i - 500)
            if distanza <= 12:
                # Zona dell'arco: rettilineo assoluto e zero colline
                line.y = 0
                line.curve = 0
            else:
                # Raccordo fluido per evitare gradini geometrici o sobbalzi nella pista
                fattore = (distanza - 12) / 48.0
                line.y = line.y * fattore
                line.curve = line.curve * fattore

        # --- RACCORDO DEL TRAGUARDO ---
        # La quota sfuma a zero all'inizio e alla fine della pista, così l'ultimo segmento
        # si ricollega al primo senza il "muro" che compariva a ogni cambio giro.
        dist_traguardo = min(i, num_segments - 1 - i)
        if dist_traguardo < 60:
            t = dist_traguardo / 60.0
            line.y = line.y * t * t * (3 - 2 * t)

        # 2. Posizionamento Monete
        if i > 20 and i % 20 == 0:
            line.sprite = coin_img
            line.spriteX = random.choice([-0.8, -0.4, 0, 0.4, 0.8])
            if level == 9 or random.random() < 0.25:
                line.sprite_h = 3500 if level != 9 else random.randint(2000, 6000) # Nello spazio monete molto in alto
                
        # 3. Ostacoli ed Elementi di Contorno Laterali
        tree_frequency = 4 if level == 7 else (5 if level == 8 else 8)
        if i % tree_frequency == 0 and not line.has_container and not line.has_cave_tunnel and not (500 <= i <= 504) and level != 9:
            line.has_tree = True
            line.treeX = random.choice([-1.5, 1.5, -2.0, 2.0]) if level == 7 else random.choice([-1.5, 1.5])
            if is_level_3:
                line.urban_type = random.choice(['car', 'car', 'truck', 'house', 'tree'])
            elif level == 4:
                line.urban_type = random.choice(['baobab', 'baobab', 'hut', 'animal'])
            elif level == 5:
                line.urban_type = random.choice(['crystal_purple', 'crystal_cyan', 'crystal_green', 'stalagmite', 'minecart'])
            elif level == 6:
                line.urban_type = random.choice(['palm', 'palm', 'umbrella', 'sunbed', 'sandcastle'])
            elif level == 7:
                line.urban_type = 'pine'
            elif level == 8:
                line.urban_type = random.choice(['lava_rock', 'lava_rock', 'lava_geyser', 'dead_tree'])
                
        # 4. Traguardo e Archi Celebravitivi
        if i == 80:
            line.has_arch = True
            line.arch_text = "START"
            
       # Arco speciale "AMEDEO" a metà pista: ne mettiamo 6 di fila per creare un tunnel spettacolare!
        if level in [1, 2, 3, 4, 6, 7, 8, 9] and (500 <= i <= 505):
            line.has_arch = True
            line.arch_text = "AMEDEO"
            
        # Pulizia di sicurezza: eliminiamo eventuali alberi/ostacoli nati dentro la galleria di Amedeo
        if level in [1, 2, 3, 4, 6, 7, 8, 9] and (495 <= i <= 510):
            line.has_tree = False
            
        lines.append(line)
        
    track_length = len(lines) * SEGMENT_LENGTH
    return lines, track_length