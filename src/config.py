# src/config.py
import pygame

# Inizializzazione temporanea per catturare le info dello schermo nativo
pygame.init()
_info = pygame.display.Info()

# Impostazioni Finestra / Schermo
WIDTH = _info.current_w if _info.current_w > 0 else 1920
HEIGHT = _info.current_h if _info.current_h > 0 else 1080
FPS = 60

# Parametri del Tracciato
SEGMENT_LENGTH = 200

# Palette Colori Standard (Default)
GRASS_LIGHT  = (34, 139, 34)
GRASS_DARK   = (0, 100, 0)
ROAD_LIGHT   = (160, 104, 60)  # Terra chiara
ROAD_DARK    = (139, 90, 43)   # Terra scura
RUMBLE_LIGHT = (255, 255, 255)
RUMBLE_DARK  = (200, 0, 0)
SKY_COLOR    = (135, 206, 235)

# Colori UI
TEXT_COLOR   = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0)
GOLD_COLOR   = (255, 215, 0)
ORANGE_COLOR = (255, 140, 0)
