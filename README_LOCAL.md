# 🚀 ComfyUI Video Generator - Setup Locale

## 🔧 Problema di Connessione ComfyUI

Se hai problemi di connessione con ComfyUI, segui questi passi:

### 1. Test di Connessione

Esegui il test di connessione nella directory della tua app:

```bash
python comfyui_local_test.py
```

### 2. Verifica ComfyUI

Assicurati che ComfyUI sia:
- ✅ **In esecuzione** sulla porta 8188
- ✅ **Accessibile** via browser su http://127.0.0.1:8188
- ✅ **API attiva** (di default è attiva)

### 3. Configurazione Backend

Il backend deve usare l'URL corretto. Controlla `backend/.env`:

```env
COMFYUI_URL=http://127.0.0.1:8188
MONGO_URL=mongodb://localhost:27017
DB_NAME=comfyui_video_generator
```

### 4. Riavvia l'App

Dopo aver configurato:

```bash
# Ferma l'app se in esecuzione
# Poi riavvia

# Windows
start.bat

# macOS/Linux
./start.sh
```

### 5. Verifica Configurazione

Nell'app web:
1. Vai su http://localhost:3000
2. Clicca "⚙️ Configura ComfyUI"
3. Inserisci l'URL corretto
4. Clicca "Salva"

## 🐛 Debug Avanzato

### Controlla Backend

```bash
cd backend
python server.py
```

Dovresti vedere:
- Server avviato su http://0.0.0.0:8001
- Nessun errore di connessione

### Controlla Frontend

```bash
cd frontend
npm start
```

Dovresti vedere:
- App avviata su http://localhost:3000
- ComfyUI Status: "connected" (verde)

### Controlla Logs

Se ci sono errori, controlla:
- **Backend**: Console del terminale backend
- **Frontend**: Console browser (F12)
- **ComfyUI**: Console ComfyUI

## 🔄 Risoluzione Problemi

### ComfyUI non si connette

1. **Verifica ComfyUI**:
   ```bash
   # In browser
   http://127.0.0.1:8188
   ```

2. **Verifica API**:
   ```bash
   # In browser
   http://127.0.0.1:8188/system_stats
   ```

3. **Test manuale**:
   ```bash
   curl http://127.0.0.1:8188/system_stats
   ```

### App non funziona

1. **Reinstalla dipendenze**:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd frontend
   npm install
   ```

2. **Controlla MongoDB**:
   ```bash
   # Verifica che MongoDB sia in esecuzione
   mongod --version
   ```

3. **Riavvia tutto**:
   ```bash
   # Ferma tutto
   # Poi riavvia con start.bat o start.sh
   ```

## 🎯 Checklist Finale

- [ ] ComfyUI in esecuzione e accessibile
- [ ] Backend configurato con URL corretto
- [ ] MongoDB in esecuzione
- [ ] App avviata con start.bat/start.sh
- [ ] Status "connected" nell'interfaccia web
- [ ] Checkpoint e LoRA visibili nelle dropdown

Se tutto è ✅, l'app dovrebbe funzionare perfettamente!

---

**Per supporto: controlla i file di log e assicurati che tutti i servizi siano in esecuzione.**