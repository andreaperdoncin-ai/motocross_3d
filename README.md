# Motocross 3D

Motocross 3D è un arcade racing game in Python con grafica 3D stilizzata e una pista dinamica generata in base al livello. Il gioco è progettato per essere eseguito in fullscreen usando `pygame` e offre una selezione di moto, gare contro bot e livelli ispirati a diversi biomi.

## Caratteristiche

- Grafica 3D prospettica in stile retro su pista 2.5D
- Tre colori di moto selezionabili: rosso, verde, blu
- Sei livelli con scenari diversi: classico, neve, urbano, deserto, miniera, spiaggia e foresta notturna
- Monete da raccogliere lungo la pista
- Bot rivali e classifica in tempo reale
- Salti e backflip per bonus punti
- Schermata di fine gara con podio 3D e risultati

## Come giocare

1. Avvia il gioco dal file `main.py`.
2. Nella schermata iniziale premi un tasto per accedere alla selezione della moto.
3. Usa le frecce sinistra/destra per scegliere il colore della moto.
4. Premi `INVIO` per iniziare la gara.

### Comandi

- `←` / `→`: sterza a sinistra/destra
- `W`: accelera
- `S` o `↓`: frena
- `SPAZIO` o `↑`: salta
- Doppio `↑` rapido: backflip per bonus punti
- `ESC`: esci dal gioco
- `F1` - `F7`: passa direttamente ai livelli da 1 a 7 (durante la partita)

## Requisiti

- Python 3
- `pygame`

### Ambiente consigliato

Il progetto contiene uno script `motocross_game.sh` che attiva un ambiente virtuale `venv` e avvia il gioco.

## Avvio rapido

Da terminale, posizionati nella cartella del progetto e avvia:

```bash
python3 main.py
```

Oppure esegui lo script di avvio:

```bash
./motocross_game.sh
```

> Assicurati che il virtual environment `venv` sia presente e attivabile se usi lo script.

## Struttura del progetto

- `main.py`: punto di ingresso del gioco
- `motocross_game.sh`: script di avvio rapido
- `assets/`: risorse grafiche e audio
- `src/config.py`: configurazione principale del gioco
- `src/game.py`: logica principale del gioco
- `src/player.py`: gestione del pilota, input e fisica del salto
- `src/track.py`: generazione della pista e segmenti 3D
- `src/ui.py`: interfaccia, HUD e schermate di menu
- `tools/`: script di supporto per la generazione e il ritocco degli asset

## Note

Il gioco utilizza lo schermo in fullscreen e può essere eseguito su display ad alta risoluzione. Se non sono disponibili risorse grafiche o audio, il codice ha fallback per gestire i caricamenti mancanti.

Buon divertimento con Motocross 3D!