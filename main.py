# main.py
import sys
import pygame
from src.game import Game

def main():
    try:
        # Inizializza e avvia il motore di regia del gioco
        game = Game()
        game.run()
    except Exception as e:
        print(f"Errore critico durante l'esecuzione del gioco: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()