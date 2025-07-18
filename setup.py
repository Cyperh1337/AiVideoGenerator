#!/usr/bin/env python3
"""
ComfyUI Video Generator - Installation Wizard
Auto-installer for Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform
import json
import requests
import shutil
import zipfile
import tarfile
from pathlib import Path
import time

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ComfyUIVideoGeneratorInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.arch = platform.machine().lower()
        self.python_version = sys.version_info
        self.base_dir = Path(__file__).parent
        self.venv_dir = self.base_dir / "venv"
        self.node_installed = False
        self.python_ok = False
        self.mongodb_configured = False
        
    def print_header(self):
        """Print installation header"""
        print(f"""
{Colors.HEADER}{Colors.BOLD}
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║         🎬 ComfyUI Video Generator - Installation Wizard        ║
║                                                                ║
║    Generatore di video automatico con checkpoint e LoRA       ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
{Colors.ENDC}

{Colors.OKCYAN}Sistema rilevato: {self.system.title()} ({self.arch}){Colors.ENDC}
{Colors.OKCYAN}Python: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}{Colors.ENDC}
""")

    def check_python_version(self):
        """Check if Python version is compatible"""
        print(f"{Colors.OKBLUE}🔍 Verifica versione Python...{Colors.ENDC}")
        
        if self.python_version < (3, 8):
            print(f"{Colors.FAIL}❌ Python 3.8+ richiesto. Versione attuale: {self.python_version.major}.{self.python_version.minor}{Colors.ENDC}")
            print(f"{Colors.WARNING}📥 Scarica Python da: https://python.org/downloads/{Colors.ENDC}")
            return False
        
        print(f"{Colors.OKGREEN}✅ Python {self.python_version.major}.{self.python_version.minor} OK{Colors.ENDC}")
        self.python_ok = True
        return True

    def check_node_version(self):
        """Check if Node.js is installed and compatible"""
        print(f"{Colors.OKBLUE}🔍 Verifica Node.js...{Colors.ENDC}")
        
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                major_version = int(version.split('.')[0][1:])  # Remove 'v' prefix
                
                if major_version >= 16:
                    print(f"{Colors.OKGREEN}✅ Node.js {version} OK{Colors.ENDC}")
                    self.node_installed = True
                    return True
                else:
                    print(f"{Colors.FAIL}❌ Node.js 16+ richiesto. Versione attuale: {version}{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}❌ Node.js non trovato{Colors.ENDC}")
        except FileNotFoundError:
            print(f"{Colors.FAIL}❌ Node.js non installato{Colors.ENDC}")
        
        return self.install_nodejs()

    def install_nodejs(self):
        """Install Node.js automatically"""
        print(f"{Colors.WARNING}📥 Installazione Node.js...{Colors.ENDC}")
        
        if self.system == "windows":
            print(f"{Colors.OKBLUE}🔧 Installerò Node.js tramite winget...{Colors.ENDC}")
            try:
                subprocess.run(['winget', 'install', 'OpenJS.NodeJS'], check=True)
                print(f"{Colors.OKGREEN}✅ Node.js installato con successo{Colors.ENDC}")
                return True
            except:
                print(f"{Colors.FAIL}❌ Installazione automatica fallita{Colors.ENDC}")
                print(f"{Colors.WARNING}📥 Scarica manualmente da: https://nodejs.org{Colors.ENDC}")
                return False
        
        elif self.system == "darwin":  # macOS
            print(f"{Colors.OKBLUE}🔧 Installerò Node.js tramite Homebrew...{Colors.ENDC}")
            try:
                subprocess.run(['brew', 'install', 'node'], check=True)
                print(f"{Colors.OKGREEN}✅ Node.js installato con successo{Colors.ENDC}")
                return True
            except:
                print(f"{Colors.FAIL}❌ Homebrew non trovato o installazione fallita{Colors.ENDC}")
                print(f"{Colors.WARNING}📥 Scarica manualmente da: https://nodejs.org{Colors.ENDC}")
                return False
        
        else:  # Linux
            print(f"{Colors.OKBLUE}🔧 Installerò Node.js tramite package manager...{Colors.ENDC}")
            try:
                # Try different package managers
                if shutil.which('apt'):
                    subprocess.run(['sudo', 'apt', 'update'], check=True)
                    subprocess.run(['sudo', 'apt', 'install', '-y', 'nodejs', 'npm'], check=True)
                elif shutil.which('yum'):
                    subprocess.run(['sudo', 'yum', 'install', '-y', 'nodejs', 'npm'], check=True)
                elif shutil.which('dnf'):
                    subprocess.run(['sudo', 'dnf', 'install', '-y', 'nodejs', 'npm'], check=True)
                else:
                    raise Exception("Package manager not found")
                
                print(f"{Colors.OKGREEN}✅ Node.js installato con successo{Colors.ENDC}")
                return True
            except:
                print(f"{Colors.FAIL}❌ Installazione automatica fallita{Colors.ENDC}")
                print(f"{Colors.WARNING}📥 Installa manualmente: sudo apt install nodejs npm{Colors.ENDC}")
                return False

    def check_mongodb(self):
        """Check if MongoDB is available"""
        print(f"{Colors.OKBLUE}🔍 Verifica MongoDB...{Colors.ENDC}")
        
        # Check if MongoDB is running locally
        try:
            import pymongo
            client = pymongo.MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
            client.server_info()
            print(f"{Colors.OKGREEN}✅ MongoDB locale trovato{Colors.ENDC}")
            self.mongodb_configured = True
            return True
        except:
            pass
        
        # Offer MongoDB installation options
        print(f"{Colors.WARNING}⚠️  MongoDB non trovato localmente{Colors.ENDC}")
        print(f"{Colors.OKBLUE}📋 Opzioni disponibili:{Colors.ENDC}")
        print(f"1. Installa MongoDB localmente (raccomandato)")
        print(f"2. Usa MongoDB Atlas (cloud)")
        print(f"3. Configura manualmente dopo")
        
        choice = input(f"{Colors.OKCYAN}Scegli (1-3): {Colors.ENDC}").strip()
        
        if choice == "1":
            return self.install_mongodb_local()
        elif choice == "2":
            return self.setup_mongodb_atlas()
        else:
            print(f"{Colors.WARNING}⚠️  Configurazione MongoDB rimandata{Colors.ENDC}")
            return True

    def install_mongodb_local(self):
        """Install MongoDB locally"""
        print(f"{Colors.OKBLUE}🔧 Installazione MongoDB locale...{Colors.ENDC}")
        
        if self.system == "windows":
            print(f"{Colors.WARNING}📥 Per Windows, scarica MongoDB da: https://www.mongodb.com/try/download/community{Colors.ENDC}")
            print(f"{Colors.OKBLUE}💡 Oppure usa MongoDB Atlas per un setup più semplice{Colors.ENDC}")
            return False
        
        elif self.system == "darwin":  # macOS
            try:
                subprocess.run(['brew', 'tap', 'mongodb/brew'], check=True)
                subprocess.run(['brew', 'install', 'mongodb-community'], check=True)
                subprocess.run(['brew', 'services', 'start', 'mongodb/brew/mongodb-community'], check=True)
                print(f"{Colors.OKGREEN}✅ MongoDB installato e avviato{Colors.ENDC}")
                self.mongodb_configured = True
                return True
            except:
                print(f"{Colors.FAIL}❌ Installazione MongoDB fallita{Colors.ENDC}")
                return False
        
        else:  # Linux
            try:
                if shutil.which('apt'):
                    subprocess.run(['sudo', 'apt', 'update'], check=True)
                    subprocess.run(['sudo', 'apt', 'install', '-y', 'mongodb'], check=True)
                    subprocess.run(['sudo', 'systemctl', 'start', 'mongodb'], check=True)
                    subprocess.run(['sudo', 'systemctl', 'enable', 'mongodb'], check=True)
                else:
                    raise Exception("Package manager not supported")
                
                print(f"{Colors.OKGREEN}✅ MongoDB installato e avviato{Colors.ENDC}")
                self.mongodb_configured = True
                return True
            except:
                print(f"{Colors.FAIL}❌ Installazione MongoDB fallita{Colors.ENDC}")
                return False

    def setup_mongodb_atlas(self):
        """Setup MongoDB Atlas configuration"""
        print(f"{Colors.OKBLUE}🌐 Configurazione MongoDB Atlas{Colors.ENDC}")
        print(f"{Colors.WARNING}1. Vai su https://cloud.mongodb.com{Colors.ENDC}")
        print(f"{Colors.WARNING}2. Crea un account gratuito{Colors.ENDC}")
        print(f"{Colors.WARNING}3. Crea un nuovo cluster{Colors.ENDC}")
        print(f"{Colors.WARNING}4. Ottieni la connection string{Colors.ENDC}")
        
        mongo_url = input(f"{Colors.OKCYAN}Inserisci la MongoDB connection string: {Colors.ENDC}").strip()
        
        if mongo_url:
            # Test connection
            try:
                import pymongo
                client = pymongo.MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
                client.server_info()
                print(f"{Colors.OKGREEN}✅ Connessione MongoDB Atlas testata con successo{Colors.ENDC}")
                
                # Save to env file
                self.save_mongo_url(mongo_url)
                self.mongodb_configured = True
                return True
            except Exception as e:
                print(f"{Colors.FAIL}❌ Connessione fallita: {e}{Colors.ENDC}")
                return False
        
        return False

    def save_mongo_url(self, mongo_url):
        """Save MongoDB URL to environment files"""
        # Backend .env
        backend_env = self.base_dir / "backend" / ".env"
        backend_env.parent.mkdir(exist_ok=True)
        
        env_content = f"""MONGO_URL={mongo_url}
DB_NAME=comfyui_video_generator
"""
        backend_env.write_text(env_content)
        
        # Frontend .env
        frontend_env = self.base_dir / "frontend" / ".env"
        frontend_env.parent.mkdir(exist_ok=True)
        
        frontend_env_content = f"""REACT_APP_BACKEND_URL=http://localhost:8001
"""
        frontend_env.write_text(frontend_env_content)

    def create_virtual_environment(self):
        """Create Python virtual environment"""
        print(f"{Colors.OKBLUE}🔧 Creazione ambiente virtuale Python...{Colors.ENDC}")
        
        try:
            subprocess.run([sys.executable, '-m', 'venv', str(self.venv_dir)], check=True)
            print(f"{Colors.OKGREEN}✅ Ambiente virtuale creato{Colors.ENDC}")
            return True
        except Exception as e:
            print(f"{Colors.FAIL}❌ Errore creazione ambiente virtuale: {e}{Colors.ENDC}")
            return False

    def install_python_dependencies(self):
        """Install Python dependencies"""
        print(f"{Colors.OKBLUE}📦 Installazione dipendenze Python...{Colors.ENDC}")
        
        # Get pip path
        if self.system == "windows":
            pip_path = self.venv_dir / "Scripts" / "pip.exe"
        else:
            pip_path = self.venv_dir / "bin" / "pip"
        
        requirements_file = self.base_dir / "backend" / "requirements.txt"
        
        try:
            subprocess.run([str(pip_path), 'install', '-r', str(requirements_file)], check=True)
            print(f"{Colors.OKGREEN}✅ Dipendenze Python installate{Colors.ENDC}")
            return True
        except Exception as e:
            print(f"{Colors.FAIL}❌ Errore installazione dipendenze: {e}{Colors.ENDC}")
            return False

    def install_node_dependencies(self):
        """Install Node.js dependencies"""
        print(f"{Colors.OKBLUE}📦 Installazione dipendenze Node.js...{Colors.ENDC}")
        
        frontend_dir = self.base_dir / "frontend"
        
        try:
            subprocess.run(['npm', 'install'], cwd=str(frontend_dir), check=True)
            print(f"{Colors.OKGREEN}✅ Dipendenze Node.js installate{Colors.ENDC}")
            return True
        except Exception as e:
            print(f"{Colors.FAIL}❌ Errore installazione dipendenze Node.js: {e}{Colors.ENDC}")
            return False

    def create_startup_scripts(self):
        """Create startup scripts for different platforms"""
        print(f"{Colors.OKBLUE}📝 Creazione script di avvio...{Colors.ENDC}")
        
        # Windows batch script
        if self.system == "windows":
            batch_content = f"""@echo off
echo Starting ComfyUI Video Generator...

REM Start backend
echo Starting backend...
cd /d "{self.base_dir}\\backend"
start "Backend" "{self.venv_dir}\\Scripts\\python.exe" server.py

REM Wait a moment for backend to start
timeout /t 5 /nobreak > nul

REM Start frontend
echo Starting frontend...
cd /d "{self.base_dir}\\frontend"
start "Frontend" npm start

echo.
echo ComfyUI Video Generator avviato!
echo Backend: http://localhost:8001
echo Frontend: http://localhost:3000
echo.
echo Premi un tasto per chiudere...
pause > nul
"""
            
            batch_file = self.base_dir / "start.bat"
            batch_file.write_text(batch_content)
            
            # Create stop script
            stop_content = """@echo off
echo Stopping ComfyUI Video Generator...
taskkill /f /im python.exe /fi "WINDOWTITLE eq Backend*"
taskkill /f /im node.exe /fi "WINDOWTITLE eq Frontend*"
echo Stopped.
pause
"""
            stop_file = self.base_dir / "stop.bat"
            stop_file.write_text(stop_content)
        
        # Unix shell script
        else:
            shell_content = f"""#!/bin/bash
echo "Starting ComfyUI Video Generator..."

# Start backend
echo "Starting backend..."
cd "{self.base_dir}/backend"
source "{self.venv_dir}/bin/activate"
python server.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend
echo "Starting frontend..."
cd "{self.base_dir}/frontend"
npm start &
FRONTEND_PID=$!

echo ""
echo "ComfyUI Video Generator started!"
echo "Backend: http://localhost:8001"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop..."

# Wait for user interrupt
trap "echo 'Stopping...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
"""
            
            shell_file = self.base_dir / "start.sh"
            shell_file.write_text(shell_content)
            shell_file.chmod(0o755)
        
        print(f"{Colors.OKGREEN}✅ Script di avvio creati{Colors.ENDC}")

    def create_user_guide(self):
        """Create user guide"""
        print(f"{Colors.OKBLUE}📖 Creazione guida utente...{Colors.ENDC}")
        
        guide_content = f"""# ComfyUI Video Generator - Guida Utente

## 🚀 Avvio dell'applicazione

### Windows
- Doppio click su `start.bat`
- Oppure apri terminale e esegui: `start.bat`

### macOS/Linux
- Apri terminale nella cartella dell'app
- Esegui: `./start.sh`

## 🎯 Primo utilizzo

1. **Avvia l'applicazione** con i comandi sopra
2. **Apri il browser** e vai su: http://localhost:3000
3. **Verifica ComfyUI**: 
   - Assicurati che ComfyUI sia in esecuzione su http://127.0.0.1:8188
   - Lo status dovrebbe mostrare "connected" (verde)

## 🎬 Generazione video

### Prerequisiti
- ComfyUI installato e in esecuzione
- Checkpoint (.safetensors) nella cartella `models/checkpoints/`
- LoRA (.safetensors) nella cartella `models/loras/` (opzionale)

### Processo di generazione

1. **Inserisci prompt**: Descrivi il video che vuoi generare
2. **Seleziona checkpoint**: Scegli il modello base
3. **Seleziona LoRA**: (Opzionale) Scegli un LoRA per personalizzare lo stile
4. **Configura parametri**:
   - **Tipo video**: 
     - Short (TikTok) - 16 frames
     - Medium - 60 frames  
     - Long (YouTube) - 120 frames
   - **Risoluzione**: Larghezza e altezza (default: 512x512)
   - **Frames**: Numero di frame personalizzato (8-600)
5. **Clicca "Genera Video"**

### Monitoraggio

- **Stato corrente**: Mostra lo stato della generazione in corso
- **Cronologia**: Visualizza tutte le generazioni passate
- **Progress**: Aggiornamento in tempo reale dello stato

## 🔧 Configurazione

### ComfyUI
- **URL**: http://127.0.0.1:8188 (default)
- **API**: Assicurati che l'API sia attiva
- **Modelli**: Posiziona i tuoi file nelle cartelle appropriate

### Database
- **MongoDB**: Configurato automaticamente durante l'installazione
- **Backup**: I dati sono salvati nel database MongoDB

## 🛠️ Risoluzione problemi

### ComfyUI non si connette
1. Verifica che ComfyUI sia in esecuzione
2. Controlla che l'API sia attiva
3. Verifica l'URL: http://127.0.0.1:8188

### Errori di generazione
1. Controlla che i checkpoint siano disponibili
2. Verifica che i parametri siano corretti
3. Controlla i log di ComfyUI

### Problemi di avvio
1. Assicurati che tutte le dipendenze siano installate
2. Verifica che MongoDB sia in esecuzione
3. Controlla i permessi dei file

## 📁 Struttura cartelle

```
comfyui-video-generator/
├── backend/          # Server FastAPI
├── frontend/         # App React
├── venv/            # Ambiente virtuale Python
├── start.bat        # Script avvio Windows
├── start.sh         # Script avvio Unix
└── README.md        # Questa guida
```

## 💡 Suggerimenti

1. **Checkpoint**: Usa modelli ottimizzati per video
2. **LoRA**: Combina diversi LoRA per stili unici
3. **Prompt**: Sii specifico nella descrizione
4. **Durata**: Inizia con video corti per test
5. **Risoluzione**: 512x512 è ottimale per performance

## 🆘 Supporto

Per problemi o domande:
1. Controlla questa guida
2. Verifica i log dell'applicazione
3. Consulta la documentazione di ComfyUI

---

**Buona generazione di video! 🎬**
"""
        
        guide_file = self.base_dir / "README.md"
        guide_file.write_text(guide_content)
        
        print(f"{Colors.OKGREEN}✅ Guida utente creata (README.md){Colors.ENDC}")

    def run_installation(self):
        """Run complete installation process"""
        self.print_header()
        
        print(f"{Colors.OKBLUE}🔍 Verifica requisiti di sistema...{Colors.ENDC}")
        
        # Check system requirements
        if not self.check_python_version():
            print(f"{Colors.FAIL}❌ Installazione interrotta: Python non compatible{Colors.ENDC}")
            return False
        
        if not self.check_node_version():
            print(f"{Colors.FAIL}❌ Installazione interrotta: Node.js non installato{Colors.ENDC}")
            return False
        
        # Check MongoDB
        self.check_mongodb()
        
        # Create virtual environment
        if not self.create_virtual_environment():
            print(f"{Colors.FAIL}❌ Installazione interrotta: Errore ambiente virtuale{Colors.ENDC}")
            return False
        
        # Install dependencies
        if not self.install_python_dependencies():
            print(f"{Colors.FAIL}❌ Installazione interrotta: Errore dipendenze Python{Colors.ENDC}")
            return False
        
        if not self.install_node_dependencies():
            print(f"{Colors.FAIL}❌ Installazione interrotta: Errore dipendenze Node.js{Colors.ENDC}")
            return False
        
        # Create startup scripts
        self.create_startup_scripts()
        
        # Create user guide
        self.create_user_guide()
        
        # Final setup
        if not self.mongodb_configured:
            self.save_mongo_url("mongodb://localhost:27017")
        
        # Success message
        print(f"""
{Colors.OKGREEN}{Colors.BOLD}
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  🎉 INSTALLAZIONE COMPLETATA CON SUCCESSO! 🎉                   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
{Colors.ENDC}

{Colors.OKGREEN}✅ ComfyUI Video Generator installato correttamente{Colors.ENDC}

{Colors.OKBLUE}📋 Prossimi passi:{Colors.ENDC}
1. Assicurati che ComfyUI sia in esecuzione su http://127.0.0.1:8188
2. Avvia l'app con: {"start.bat" if self.system == "windows" else "./start.sh"}
3. Apri il browser su: http://localhost:3000
4. Inizia a generare video!

{Colors.OKCYAN}📖 Leggi README.md per la guida completa{Colors.ENDC}

{Colors.WARNING}⚠️  Ricorda: Serve ComfyUI in esecuzione per generare video{Colors.ENDC}
""")
        
        return True

def main():
    """Main installation function"""
    installer = ComfyUIVideoGeneratorInstaller()
    
    try:
        success = installer.run_installation()
        if success:
            print(f"{Colors.OKGREEN}🚀 Installazione completata! Buon divertimento!{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}❌ Installazione fallita. Controlla gli errori sopra.{Colors.ENDC}")
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️  Installazione interrotta dall'utente{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}❌ Errore imprevisto: {e}{Colors.ENDC}")

if __name__ == "__main__":
    main()