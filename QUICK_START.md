# 🚀 ComfyUI Video Generator - Avvio Rapido

## ⚡ Avvio Automatico

### Windows
```batch
# Doppio click su:
start.bat
```

### macOS/Linux
```bash
# Nel terminale:
./start.sh
```

## 🔧 Avvio Manuale (se automatico non funziona)

### 1. Avvia Backend
```bash
# Terminale 1
cd backend
python server.py
```

### 2. Avvia Frontend
```bash
# Terminale 2 (nuovo)
cd frontend
npm start
```

### 3. Accedi all'App
- **URL**: http://localhost:3000
- **Verifica**: ComfyUI Status deve essere "connected"

## 📋 Prerequisiti

### ComfyUI
- ✅ ComfyUI installato
- ✅ ComfyUI in esecuzione su: http://127.0.0.1:8188
- ✅ Checkpoint (.safetensors) in `models/checkpoints/`
- ✅ LoRA (.safetensors) in `models/loras/` (opzionale)

### Sistema
- ✅ Python 3.8+
- ✅ Node.js 16+
- ✅ MongoDB (locale o Atlas)

## 🛠️ Risoluzione Problemi

### Backend Non Si Avvia
```bash
# Verifica dipendenze
cd backend
pip install -r requirements.txt
```

### Frontend Non Si Avvia
```bash
# Verifica dipendenze
cd frontend
npm install
```

### ComfyUI Non Si Connette
1. Avvia ComfyUI: `python main.py`
2. Verifica URL: http://127.0.0.1:8188
3. Controlla che l'API sia attiva

## 🎯 Primo Utilizzo

1. **Avvia ComfyUI** (http://127.0.0.1:8188)
2. **Avvia Video Generator** (start.bat o start.sh)
3. **Apri browser** (http://localhost:3000)
4. **Verifica connessione** (Status: connected)
5. **Inizia a generare video!**

## 📞 Supporto

### Log Errori
- **Backend**: Console terminale backend
- **Frontend**: Console browser (F12)
- **ComfyUI**: Console ComfyUI

### File Configurazione
- **Backend**: `backend/.env`
- **Frontend**: `frontend/.env`

---

**Buona generazione di video! 🎬**