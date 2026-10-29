# TODO - Motocross 3D

Spunta le voci man mano che vengono completate (`- [ ]` → `- [x]`).

## 1. Lavoro in sospeso
- [ ] Provare in gioco le correzioni non ancora committate (F3, F5, F7, F9): passaggio dal traguardo senza "muro", soffitto delle gallerie senza buchi oltre i dossi, nuove rampe del livello 3, colline più morbide nei livelli 7 e 9
- [ ] Committare `src/game.py` e `src/track.py`

## 2. Nuova funzionalità: "caduta nel vuoto" nel livello Spazio (9)
Idea: nello spazio la pista non ha bordi. Se esci dalla pista, la moto non resta bloccata ma inizia a sprofondare sotto la pista; con un salto torni su.
- [x] Nel livello 9 togliere il blocco laterale in `Player.handle_input` (oggi `x` resta tra -1.5 e 1.5). La strada occupa `|x| <= 1.0`, il bordo colorato arriva a circa 1.15
- [x] Aggiungere a `Player` lo stato `is_falling`: quando la moto è a terra e `|x| > 1.15`, `y` diventa negativa e scende con la gravità lunare (in `update_physics` oggi `y <= 0` conta sempre come atterraggio)
- [x] Rallentare la moto mentre cade (es. `speed` dimezzata) così la caduta ha un costo
- [x] Permettere il salto durante la caduta (`handle_event` oggi salta solo se `not is_jumping`). Il salto di recupero riporta la moto in quota e la spinge verso il centro (`x` verso ±1.0), così atterra di nuovo sulla pista
- [x] Limite di profondità o di tempo (es. 2 secondi): se il giocatore non salta, la moto viene rimessa al centro della pista con una penalità (perdita di velocità o di punti) e un messaggio tipo "PERSO NELLO SPAZIO!"
- [x] Grafica: la moto si abbassa sullo schermo (`screen_bike_y` usa già `-y * 0.15`, quindi con `y` negativa scende da sola), si rimpicciolisce e ruota lentamente. *(fatto: si abbassa, si rimpicciolisce e ruota; da valutare se disegnarla anche dietro il bordo della pista)*
- [x] Mentre cade, la moto non deve raccogliere le monete a terra (`height_ok` in `game.py` oggi accetta qualunque `y < 3000`)
- [ ] (Opzionale) Aggiungere alcuni "buchi" nella pista del livello 9 (segmenti senza strada, segnalati dal colore), in cui si cade se si è a terra: costringono a saltare al momento giusto
- [x] Aggiornare il README con la nuova meccanica

## 3. Bug e incoerenze
- [ ] **Titoli di coda:** `self.credits_y` non viene mai azzerato, quindi alla seconda vittoria i titoli partono già fuori dallo schermo. Va reimpostato quando si entra nello stato `CREDITS`
- [ ] **Curve oltre la fine della pista:** diverse curve sono definite oltre `num_segments` e non esistono mai: livelli 1, 2, 4 (1250-1400), livello 5 (1100-1420), livello 7 (1050-1200). Al contrario il livello 8 ha 1500 segmenti ma nessuna curva dopo 980, quindi l'ultimo terzo è dritto
- [ ] **Stato `GAMEOVER` mai usato:** viene disegnato e gestito, ma nessuna parte del codice lo attiva. Va collegato a qualcosa o rimosso
- [ ] **Urto vicino alla partenza:** dopo un incidente `self.pos -= 150` può diventare negativo, senza correggere il giro. Va bloccato a 0 (o va gestito il giro)
- [ ] **Cambio livello con F1-F9:** rigenera pista e bot ma non azzera `pos` e `lap`
- [ ] **Neve "scivolosa":** il README la promette per il livello 2, ma la fisica è identica agli altri livelli. Va implementata (inerzia laterale) o tolta dal README
- [ ] **Rampe:** il README dice "sfrutta le rampe per prendere il volo", ma il salto parte solo col tasto e il terreno non dà nessuna spinta. Si potrebbe calcolare una spinta verticale dalla pendenza in cima ai dossi
- [ ] **Audio:** `engine_sound` carica in realtà `bg_music.wav`, mentre `assets/engine.wav` non viene mai usato. Va rinominato o va aggiunto un vero suono del motore con pitch legato alla velocità
- [ ] `main.py` intercetta tutte le eccezioni e stampa solo il messaggio: va aggiunto `traceback.print_exc()` per poter fare debug

## 4. Miglioramenti di gameplay
- [ ] Tasto **Pausa** (P)
- [ ] **Bot più vivi:** oggi hanno velocità costante, non sterzano, non urtano gli ostacoli e non interagiscono con il giocatore. Si possono aggiungere piccole variazioni di velocità, un "rubber band" (rallentano se sono molto avanti) e la collisione con il giocatore
- [ ] **Backflip rischioso:** se si atterra a metà rotazione la moto cade (rischio e ricompensa). Valutare più punti per i flip completi
- [ ] **Record:** salvare in un file JSON il punteggio massimo e il miglior tempo per livello, da mostrare a fine gara
- [ ] Mostrare il tempo di gara e il tempo sul giro nell'HUD
- [ ] Conto alla rovescia 3-2-1 alla partenza
- [ ] Nel livello 5 (caverna) manca l'arco AMEDEO: verificare se è voluto

## 5. Qualità del codice e prestazioni
- [ ] **Configurazione dei biomi:** colori del cielo, sfondi, colori di erba, strada e bordo sono sparsi in lunghe catene `if/elif` dentro `run()`. Raccoglierli in un dizionario `BIOMES` per livello (in `config.py` o in un nuovo `biomes.py`)
- [ ] **Spezzare `run()`** (circa 600 righe): `handle_events()`, `update()`, `render_road()`, `render_sprites()`, `render_player()`. Il disegno degli elementi di scenario (palme, cristalli, case...) può andare in un modulo `scenery.py` con una funzione per tipo
- [ ] Rendere la fisica indipendente dagli FPS (usare il `dt` di `clock.tick()`): oggi salti e sterzo dipendono dai fotogrammi
- [ ] **Prestazioni:** `pygame.transform.scale` viene chiamato ogni frame per ogni moneta e moto visibile. Si può mettere in cache per fasce di dimensione. In `ui.py` i font di `draw_race_end` e `draw_credits` vengono ricreati a ogni frame: crearli una sola volta in `__init__`
- [ ] Eliminare i `getattr(l, 'has_cave_tunnel', False)` e simili: gli attributi sono già definiti in `Line.__init__`
- [ ] `config.py` chiama `pygame.init()` all'import: spostare la lettura della risoluzione in `Game.__init__`
- [ ] Le dimensioni della moto e dell'HUD sono in pixel fissi: scalarle in base a `HEIGHT`, così il gioco appare uguale su schermi diversi

## 6. Repository e documentazione
- [ ] Togliere `src/__pycache__/*.pyc` da git (`git rm --cached`) e creare un `.gitignore` con `__pycache__/` e `venv/`
- [ ] README: la cartella si chiama `tools/`, non `scratch/`
- [ ] `motocross_game.sh`: usare la cartella dello script (`$(dirname "$0")`) invece del percorso fisso `~/pythonprojects/motocross_3d`
- [ ] Aggiungere un `requirements.txt` (`pygame`)
