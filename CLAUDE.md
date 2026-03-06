# CLAUDE.md

Questo file fornisce indicazioni a Claude Code (claude.ai/code) quando lavora con il codice in questo repository.

## Panoramica del progetto

Applicazione desktop Python a file singolo che rimuove in batch lo spazio bianco eccessivo dal margine inferiore dei file PDF. L'interfaccia è in italiano. Distribuita come eseguibile Windows autonomo tramite PyInstaller.

## Comandi

**Avviare l'applicazione:**
```bash
python remove_white.py
```

**Compilare l'eseguibile Windows:**
```bash
pyinstaller remove_white.spec
```
Output: `dist/remove_white.exe`

**Dipendenze** (nessun requirements.txt — installare manualmente):
```bash
pip install PyMuPDF pyinstaller
```

## Architettura

L'intera applicazione si trova in un unico file: [remove_white.py](remove_white.py) (117 righe).

**Due livelli principali:**

1. **Elaborazione PDF** (`remove_bottom_whitespace_from_pdf`, righe 8–30): Usa PyMuPDF (`fitz`) per aprire ogni pagina PDF, trovare la posizione del blocco di testo più in basso e, se il margine inferiore supera `margin_threshold` (default: 20 punti), ritaglia la pagina con `set_cropbox()`, preservando `spazio_in_fondo` (default: 50 punti) di spazio sotto il contenuto.

2. **GUI tkinter** (righe 87–117): Selettori di cartella input/output, campo per la soglia, barra di avanzamento e pulsante "Processa" che chiama `process_all_pdfs()`. Tale funzione individua tutti i file `.pdf` nella cartella di input, li elabora uno per uno e aggiorna la barra di avanzamento.

## Parametri chiave

| Parametro | Default | Significato |
|---|---|---|
| `margin_threshold` | 20 | Spazio bianco minimo in fondo (punti) per attivare il ritaglio |
| `spazio_in_fondo` | 50 | Spazio da mantenere sotto l'ultimo blocco di testo dopo il ritaglio |

## Branch

- `main` — versione stabile
- `Nuova-Funzionalità` — sviluppo nuove funzionalità (default upstream)
