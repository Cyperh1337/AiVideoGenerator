# 🎬 ComfyUI Video Generator - Guida Installazione

## 📋 Requisiti di Sistema

### Windows
- Windows 10/11
- 4GB RAM (8GB raccomandati)
- 2GB spazio libero su disco

### macOS
- macOS 10.15+
- 4GB RAM (8GB raccomandati)
- 2GB spazio libero su disco

### Linux
- Ubuntu 18.04+, CentOS 7+, o distribuzioni equivalenti
- 4GB RAM (8GB raccomandati)
- 2GB spazio libero su disco

## 🚀 Installazione Automatica

### Windows
1. **Scarica** l'app e estrai in una cartella
2. **Doppio click** su `install.bat`
3. **Segui** le istruzioni a schermo
4. **Attendere** il completamento dell'installazione

### macOS/Linux
1. **Scarica** l'app e estrai in una cartella
2. **Apri terminale** nella cartella dell'app
3. **Esegui**: `./install.sh`
4. **Segui** le istruzioni a schermo

## 🔧 Cosa Viene Installato Automaticamente

### Dipendenze Sistema
- **Python 3.8+** (se non presente)
- **Node.js 16+** (se non presente)
- **MongoDB** (opzionale, puoi usare Atlas)

### Dipendenze Python
- FastAPI (server backend)
- MongoDB driver (database)
- Requests (HTTP client)
- Tutte le dipendenze necessarie

### Dipendenze Node.js
- React (frontend)
- Tailwind CSS (styling)
- Axios (HTTP client)
- Tutte le dipendenze necessarie

## 🗂️ Configurazione Database

### Opzione 1: MongoDB Locale (Raccomandato)
- Installazione automatica durante setup
- Configurazione automatica
- Nessuna configurazione aggiuntiva richiesta

### Opzione 2: MongoDB Atlas (Cloud)
1. Vai su [MongoDB Atlas](https://cloud.mongodb.com)
2. Crea account gratuito
3. Crea nuovo cluster
4. Ottieni connection string
5. Inserisci durante l'installazione

## 🎯 Configurazione ComfyUI

### Prerequisiti
1. **ComfyUI installato** sul tuo computer
2. **ComfyUI in esecuzione** su `http://127.0.0.1:8188`
3. **API ComfyUI attiva** (di default è attiva)

### Verifica Configurazione
1. Apri browser e vai su: `http://127.0.0.1:8188`
2. Dovresti vedere l'interfaccia ComfyUI
3. L'API dovrebbe essere accessibile

## 📁 Struttura Cartelle

Dopo l'installazione:
```
comfyui-video-generator/
├── 📁 backend/           # Server FastAPI
│   ├── server.py         # Server principale
│   ├── requirements.txt  # Dipendenze Python
│   └── .env             # Configurazione
├── 📁 frontend/          # App React
│   ├── src/             # Codice sorgente
│   ├── package.json     # Dipendenze Node.js
│   └── .env             # Configurazione
├── 📁 venv/             # Ambiente virtuale Python
├── 🗂️ start.bat         # Avvio Windows
├── 🗂️ start.sh          # Avvio Unix
├── 📖 README.md         # Guida utente
└── 📖 INSTALL_GUIDE.md  # Questa guida
```

## 🚀 Primo Avvio

### 1. Avvia ComfyUI
```bash
# Nella cartella di ComfyUI
python main.py
```

### 2. Avvia Video Generator
**Windows:**
```batch
start.bat
```

**macOS/Linux:**
```bash
./start.sh
```

### 3. Accedi all'App
- Apri browser
- Vai su: `http://localhost:3000`
- Verifica che ComfyUI Status sia "connected" (verde)

## 🎬 Utilizzo

### Preparazione
1. **Checkpoint**: Posiziona i file `.safetensors` in `ComfyUI/models/checkpoints/`
2. **LoRA**: Posiziona i file `.safetensors` in `ComfyUI/models/loras/`

### Generazione Video
1. **Inserisci prompt** descrittivo
2. **Seleziona checkpoint** dal menu a tendina
3. **Seleziona LoRA** (opzionale)
4. **Scegli tipo video**:
   - **Short**: TikTok (16 frames)
   - **Medium**: Standard (60 frames)
   - **Long**: YouTube (120 frames)
5. **Configura parametri** (risoluzione, frames)
6. **Clicca "Genera Video"**

## 🛠️ Risoluzione Problemi

### ComfyUI Non Si Connette
**Sintomo**: Status "error" o "disconnected"
**Soluzione**:
1. Verifica che ComfyUI sia in esecuzione
2. Vai su `http://127.0.0.1:8188` nel browser
3. Riavvia ComfyUI se necessario

### Errore Dipendenze Python
**Sintomo**: Errori durante l'installazione
**Soluzione**:
1. Elimina cartella `venv/`
2. Riesegui installazione
3. Verifica connessione internet

### Errore Dipendenze Node.js
**Sintomo**: Frontend non si avvia
**Soluzione**:
1. Elimina cartella `frontend/node_modules/`
2. Riesegui: `npm install` nella cartella frontend
3. Verifica connessione internet

### Database Non Funziona
**Sintomo**: Errori di connessione database
**Soluzione**:
1. Verifica che MongoDB sia in esecuzione
2. Controlla file `.env` nel backend
3. Usa MongoDB Atlas se problemi persistono

## 📞 Supporto

### Log degli Errori
- **Backend**: Console del terminale backend
- **Frontend**: Console del browser (F12)
- **ComfyUI**: Console ComfyUI

### File di Configurazione
- **Backend**: `backend/.env`
- **Frontend**: `frontend/.env`

### Reinstallazione
1. Elimina cartelle `venv/` e `frontend/node_modules/`
2. Riesegui script di installazione
3. Tutti i dati del database sono preservati

---

## 🎉 Buon Divertimento!

Una volta installato, potrai:
- ✅ Generare video con i tuoi checkpoint preferiti
- ✅ Utilizzare LoRA per stili personalizzati
- ✅ Creare contenuti per TikTok, YouTube e altro
- ✅ Tracciare tutte le tue generazioni
- ✅ Sperimentare con parametri avanzati

**Inizia subito a creare video straordinari! 🎬**