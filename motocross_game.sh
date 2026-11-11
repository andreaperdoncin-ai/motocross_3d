#!/bin/bash
# Script di avvio rapido per il gioco "Motocross 3D" di Amedeo

# Forza l'uscita in caso di errori imprevisti
set -e

# Determina il percorso assoluto della cartella del gioco
PROJECT_DIR="$HOME/pythonprojects/motocross_3d"

# Spostati nella cartella del progetto
if [ -d "$PROJECT_DIR" ]; then
    cd "$PROJECT_DIR"
else
    echo "❌ Errore: La cartella del progetto non esiste in $PROJECT_DIR"
    exit 1
fi

# Controlla se l'ambiente virtuale è presente e lo attiva
if [ -f ".venv/bin/activate" ]; then
    echo "📦 Attivazione dell'ambiente virtuale (venv)..."
    source .venv/bin/activate
else
    echo "❌ Errore: Ambiente virtuale non trovato. Esegui prima la configurazione."
    exit 1
fi

# Avvia il punto di ingresso principale del gioco
echo "🏍️ Avvio di Motocross 3D in corso... Divertiti Amedeo!"
python3 main.py

# Disattiva l'ambiente virtuale in modo pulito una volta chiuso il gioco
deactivate
