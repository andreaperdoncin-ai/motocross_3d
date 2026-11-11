# 🏍️ Motocross 3D - Il Trionfo di Amedeo 🏍️

Motocross 3D è un entusiasmante *arcade racing game* in Python ispirato ai classici giochi di corse retro in pseudo-3D. Sfreccia attraverso piste dinamiche, salta ostacoli, fai acrobazie, raccogli monete d'oro e batti i rivali per qualificarti al livello successivo! Riuscirai a completare tutti i 9 mondi e conquistare l'universo?

## ✨ Caratteristiche Principali

- **Grafica Pseudo-3D (Painter's Algorithm):** Un motore grafico super fluido a 60 FPS che simula un ambiente 3D prospettico mozzafiato.
- **Scegli la tua Moto:** Seleziona la tua moto e il tuo pilota tra 3 colorazioni: Rossa, Verde o Blu.
- **9 Biomi Esclusivi:** 
  1. 🌲 **Classico:** Colline e prati verdi.
  2. ❄️ **Neve:** Montagne ghiacciate scivolose.
  3. 🏙️ **Città Industriale:** Container, case e auto.
  4. 🏜️ **Deserto Africano:** Baobab e animali esotici.
  5. ⛏️ **Caverna di Cristalli:** Stalagmiti, vagonetti e tunnel di roccia.
  6. 🏖️ **Spiaggia:** Sabbia dorata, palme e ombrelloni.
  7. 🌌 **Foresta Notturna:** Un fitto bosco illuminato dalle stelle.
  8. 🌋 **Vulcano:** Lava, geyser, rocce incandescenti e tunnel infuocati.
  9. 🚀 **Spazio Profondo:** Pista neon arcobaleno, gravità lunare (salti lunghissimi e lenti) e assenza di ostacoli (3 giri). Attenzione: la pista non ha bordi! Se esci finisci nel vuoto: salta subito per tornare in pista, altrimenti perdi 10 punti.
- **Fisica Dinamica:** Accelera, frena, sterza e, soprattutto, **salta**! Sfrutta le rampe per prendere il volo.
- **Acrobazie (Backflip):** Esegui un rapido doppio click sulla Freccia Su durante un salto per effettuare un Backflip e guadagnare punti extra.
- **Competizione IA:** Gareggia contro due bot rivali (colori rimanenti) che proveranno a soffiarti i primi due posti.
- **Arco "AMEDEO":** A metà di ogni pista, sfreccia sotto il maestoso e colorato arco di Amedeo!
- **Finale Epico:** Supera il livello spaziale per goderti i titoli di coda (Star Wars style) con la tua moto personalizzata che vola nello spazio!

## 🎮 Come Giocare

1. Avvia il gioco eseguendo `main.py` (o lo script `motocross_game.sh`).
2. Nella schermata iniziale premi un tasto qualsiasi.
3. Usa le frecce `←` / `→` per scegliere la tua moto, poi premi `INVIO`.
4. Arriva **1° o 2°** per qualificarti al livello successivo!

### Comandi di Gioco

- `←` / `→`: Sterza a Sinistra / Destra
- `W`: Accelera al massimo (Turbo)
- `S` o `↓`: Frena
- `SPAZIO` o `↑`: Salta (quando sei a terra)
- **Doppio click rapido su `↑`**: Backflip (quando sei in aria)
- `ESC`: Esci dal gioco
- `F1` - `F9`: Tasti sviluppatore per saltare direttamente a un livello specifico (Es. F9 per lo Spazio)

## 🛠️ Requisiti e Installazione

Il gioco richiede **Python 3** (testato con Python 3.15) e la libreria **pygame-ce** (Pygame Community Edition), indicata in `requirements.txt`.

```bash
# Crea e attiva l'ambiente virtuale nella cartella del progetto
python3 -m venv .venv
source .venv/bin/activate

# Installa le dipendenze
pip install -r requirements.txt

# Avvia il gioco
./motocross_game.sh
```

*Lo script `motocross_game.sh` attiva da solo l'ambiente `.venv` e avvia `main.py`. In alternativa, con l'ambiente attivo, puoi eseguire direttamente `python3 main.py`.*

## 📁 Struttura del Progetto

- `main.py`: Entry-point principale del gioco.
- `src/`: Contiene la logica e i moduli del gioco.
  - `config.py`: Variabili costanti e configurazioni del display.
  - `game.py`: Loop principale, rendering 3D, stati del gioco e audio.
  - `player.py`: Fisica della moto, gestione dei salti, input e backflip.
  - `track.py`: Generatore matematico dei circuiti e posizionamento ostacoli.
  - `ui.py`: Interfaccia grafica (HUD), Menu, Podio e Titoli di coda.
- `assets/`: Immagini (moto, monete, sfondi), script generatori e suoni.
- `tools/`: Script Python secondari usati per generare programmaticamente gli sfondi e gli asset.

---
*Progetto creato e perfezionato in collaborazione con l'IA, dedicato al grande campione Amedeo!* 🏆