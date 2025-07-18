# 🎬 ComfyUI Video Generator - Guida Utilizzo Completa

## 🚀 Avvio Rapido

### 1. Prerequisiti
- ✅ ComfyUI installato e funzionante
- ✅ Video Generator installato
- ✅ Checkpoint (.safetensors) disponibili
- ✅ LoRA (.safetensors) disponibili (opzionale)

### 2. Avvio Sistema
```bash
# 1. Avvia ComfyUI
cd /path/to/ComfyUI
python main.py

# 2. Avvia Video Generator
cd /path/to/comfyui-video-generator
./start.sh  # o start.bat su Windows
```

### 3. Accesso
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **ComfyUI**: http://127.0.0.1:8188

## 🎯 Interfaccia Utente

### Dashboard Principale
```
╔════════════════════════════════════════════════════════════════╗
║                    ComfyUI Video Generator                     ║
║               Crea video straordinari con i tuoi              ║
║                checkpoint e LoRA personalizzati                ║
║                                                                ║
║  ComfyUI Status: [🟢 connected] [🔴 disconnected] [🟡 error]  ║
╚════════════════════════════════════════════════════════════════╝
```

### Pannello di Generazione
- **Prompt**: Textarea per descrizione video
- **Checkpoint**: Dropdown con modelli disponibili
- **LoRA**: Dropdown con LoRA disponibili (opzionale)
- **Tipo Video**: Buttons per Short/Medium/Long
- **Parametri**: Controlli per risoluzione e frames
- **Pulsante Genera**: Avvia generazione

### Pannello Status
- **Generazione Corrente**: Stato della generazione in corso
- **Cronologia**: Elenco generazioni passate
- **Progress**: Indicatori di avanzamento

## 🎬 Processo di Generazione

### Fase 1: Preparazione
1. **Inserisci Prompt Descrittivo**
   ```
   Esempio: "Una montagna maestosa al tramonto, 
   cielo arancione e viola, stile cinematografico, 
   movimento fluido delle nuvole"
   ```

2. **Seleziona Checkpoint**
   - Scegli dal menu a tendina
   - Modelli specializzati per video sono preferibili
   - Esempi: `animatediff_v2.safetensors`, `realisticVision_v4.safetensors`

3. **Seleziona LoRA (Opzionale)**
   - Aggiungi stile personalizzato
   - Esempi: `cinematic_style.safetensors`, `animation_helper.safetensors`

### Fase 2: Configurazione

#### Tipi di Video
- **Short (TikTok)**: 16 frames, ~1-2 secondi
- **Medium**: 60 frames, ~4-5 secondi  
- **Long (YouTube)**: 120 frames, ~8-10 secondi

#### Parametri Avanzati
- **Larghezza**: 256-1024px (512px raccomandato)
- **Altezza**: 256-1024px (512px raccomandato)
- **Frames**: 8-600 (personalizzabile con slider)

### Fase 3: Generazione
1. **Clicca "Genera Video"**
2. **Monitoraggio Stato**:
   - `pending`: In coda
   - `processing`: Generazione in corso
   - `completed`: Completato
   - `failed`: Errore

3. **Polling Automatico**: Aggiornamento ogni 3 secondi

## 🎨 Strategie Creative

### Prompt Efficaci
```
✅ Buoni esempi:
- "Un gatto nero che cammina lentamente in un giardino fiorito, movimento fluido, luce dorata"
- "Cascata che scorre tra rocce, gocce d'acqua scintillanti, atmosfera misteriosa"
- "Strada cittadina di notte, luci al neon colorate, pioggia che riflette i colori"

❌ Evitare:
- Prompt troppo lunghi e complessi
- Descrizioni contraddittorie
- Troppi dettagli non essenziali
```

### Combinazioni Checkpoint + LoRA
```
🎬 Per video cinematografici:
- Checkpoint: `realisticVision_v4.safetensors`
- LoRA: `cinematic_lighting.safetensors`

🎨 Per stile artistico:
- Checkpoint: `dreamlike_diffusion.safetensors`
- LoRA: `oil_painting_style.safetensors`

⚡ Per animazioni:
- Checkpoint: `animatediff_v2.safetensors`
- LoRA: `motion_enhancement.safetensors`
```

### Parametri Ottimali

#### Per Contenuti Social
```
TikTok/Instagram Reels:
- Tipo: Short
- Risoluzione: 512x512 o 512x768
- Frames: 16-24
- Stile: Dinamico, colori vivaci

YouTube Shorts:
- Tipo: Medium
- Risoluzione: 512x768 o 512x1024
- Frames: 60-90
- Stile: Narrativo, transizioni fluide
```

#### Per Contenuti Professionali
```
YouTube Standard:
- Tipo: Long
- Risoluzione: 768x432 o 1024x576
- Frames: 120-240
- Stile: Cinematografico, dettagliato

Presentazioni:
- Tipo: Medium
- Risoluzione: 1024x576
- Frames: 60-120
- Stile: Pulito, professionale
```

## 📊 Monitoraggio e Gestione

### Stati di Generazione
- 🟡 **Pending**: In coda ComfyUI
- 🔵 **Processing**: Generazione attiva
- 🟢 **Completed**: Pronto per download
- 🔴 **Failed**: Errore (verificare logs)

### Cronologia
- **Filtri**: Per stato, data, tipo
- **Dettagli**: Prompt, parametri, timestamp
- **Azioni**: Visualizza, rigenera, elimina

### Performance
- **Tempo Generazione**: Varia per complessità
- **Coda**: Gestione automatica ordine
- **Memoria**: Monitoraggio utilizzo GPU

## 🔧 Ottimizzazione

### Per Velocità
1. **Riduci Frames**: Meno frames = più veloce
2. **Risoluzione Minore**: 512x512 è ottimale
3. **Prompt Semplici**: Evita complessità eccessive
4. **Batch Processing**: Una generazione alla volta

### Per Qualità
1. **Checkpoint Specializzati**: Usa modelli per video
2. **LoRA Complementari**: Combina stili compatibili
3. **Prompt Dettagliati**: Descrizioni precise
4. **Parametri Bilanciati**: Equilibrio qualità/velocità

## 🛠️ Risoluzione Problemi

### Errori Comuni

#### ComfyUI Disconnesso
```
Sintomo: Status "error" o "disconnected"
Causa: ComfyUI non in esecuzione
Soluzione: Avvia ComfyUI su 127.0.0.1:8188
```

#### Generazione Fallita
```
Sintomo: Status "failed"
Causa: Errore workflow o parametri
Soluzione: 
- Verifica checkpoint esistente
- Controlla parametri
- Vedi logs ComfyUI
```

#### Lista Modelli Vuota
```
Sintomo: Dropdown vuoti
Causa: Cartelle modelli vuote
Soluzione:
- Aggiungi .safetensors in models/checkpoints/
- Aggiungi .safetensors in models/loras/
- Riavvia ComfyUI
```

### Debug Avanzato

#### Logs Backend
```bash
# Nel terminale backend
tail -f logs/backend.log
```

#### Logs Frontend
```javascript
// Console browser (F12)
console.log("Check network tab for API errors")
```

#### Logs ComfyUI
```bash
# Console ComfyUI
# Errori workflow visibili qui
```

## 🎯 Casi d'Uso Specifici

### Content Creator
```
Obiettivo: Video per social media
Strategia:
- Prompt accattivanti
- Durata breve (Short/Medium)
- Stili trendy
- Variazioni multiple
```

### Designer
```
Obiettivo: Materiale per presentazioni
Strategia:
- Stile professionale
- Durata media (Medium)
- Qualità alta
- Consistenza visiva
```

### Artista
```
Obiettivo: Opere creative
Strategia:
- Sperimentazione LoRA
- Prompt artistici
- Durata variabile
- Stili unici
```

## 📈 Workflow Avanzati

### Batch Generation
1. Prepara lista prompt
2. Configura parametri base
3. Genera sequenzialmente
4. Monitora attraverso cronologia

### Style Transfer
1. Usa checkpoint base neutro
2. Applica LoRA per stile
3. Testa combinazioni diverse
4. Salva configurazioni vincenti

### Progressive Enhancement
1. Inizia con bassa risoluzione
2. Test prompt e parametri
3. Incrementa qualità gradualmente
4. Ottimizza per risultato finale

---

## 🎉 Conclusione

Con questa guida puoi:
- ✅ Padroneggiare l'interfaccia
- ✅ Creare video di qualità professionale
- ✅ Ottimizzare per diversi scopi
- ✅ Risolvere problemi comuni
- ✅ Sperimentare con stili avanzati

**Inizia a creare i tuoi video straordinari! 🚀**

---

*Per supporto aggiuntivo, consulta README.md o INSTALL_GUIDE.md*