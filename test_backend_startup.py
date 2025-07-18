#!/usr/bin/env python3
"""
Script per testare l'avvio del server backend
"""

import os
import sys
import subprocess
from pathlib import Path
import time

def test_backend_startup():
    """Test avvio server backend"""
    
    print("=" * 60)
    print("🔍 TEST AVVIO SERVER BACKEND")
    print("=" * 60)
    
    # Test 1: Verifica struttura directory
    print("\n1. Verifica struttura directory...")
    
    required_files = [
        "backend/server.py",
        "backend/requirements.txt",
        "backend/.env"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} MISSING")
            return False
    
    # Test 2: Verifica dipendenze Python
    print("\n2. Verifica dipendenze Python...")
    
    try:
        # Controlla se le dipendenze sono installate
        import fastapi
        import uvicorn
        import motor
        import aiohttp
        import dotenv
        print("   ✅ Dipendenze principali installate")
    except ImportError as e:
        print(f"   ❌ Dipendenze mancanti: {e}")
        print("   🔧 Esegui: pip install -r backend/requirements.txt")
        return False
    
    # Test 3: Test caricamento server.py
    print("\n3. Test caricamento server.py...")
    
    try:
        # Cambia directory
        original_dir = os.getcwd()
        os.chdir("backend")
        
        # Aggiungi path
        backend_path = Path(".").resolve()
        if str(backend_path) not in sys.path:
            sys.path.insert(0, str(backend_path))
        
        # Test import
        print("   🔍 Importando server.py...")
        
        # Controlla se ci sono errori di sintassi
        with open("server.py", "r") as f:
            code = f.read()
            try:
                compile(code, "server.py", "exec")
                print("   ✅ server.py sintassi OK")
            except SyntaxError as e:
                print(f"   ❌ Errore sintassi in server.py: {e}")
                return False
        
        os.chdir(original_dir)
        
    except Exception as e:
        print(f"   ❌ Errore caricamento server.py: {e}")
        os.chdir(original_dir)
        return False
    
    # Test 4: Test avvio server
    print("\n4. Test avvio server...")
    
    print("   🔍 Tentativo di avvio server...")
    print("   ⚠️  Questo potrebbe richiedere alcuni secondi...")
    
    try:
        # Avvia server in background
        os.chdir("backend")
        
        # Comando per avviare il server
        cmd = [sys.executable, "server.py"]
        
        print(f"   🔍 Comando: {' '.join(cmd)}")
        print("   🔍 Directory: backend/")
        
        # Prova ad avviare
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Aspetta un po' per vedere se si avvia
        time.sleep(3)
        
        # Controlla se il processo è ancora in esecuzione
        if process.poll() is None:
            print("   ✅ Server avviato con successo!")
            
            # Termina il processo
            process.terminate()
            process.wait()
            
            print("   ✅ Server terminato correttamente")
            
        else:
            print("   ❌ Server si è fermato immediatamente")
            
            # Leggi output/errori
            stdout, stderr = process.communicate()
            
            if stdout:
                print(f"   📄 Output:\n{stdout}")
            if stderr:
                print(f"   📄 Errori:\n{stderr}")
            
            return False
        
        os.chdir(original_dir)
        
    except Exception as e:
        print(f"   ❌ Errore avvio server: {e}")
        os.chdir(original_dir)
        return False
    
    print("\n" + "=" * 60)
    print("🎯 RISULTATO:")
    print("=" * 60)
    print("✅ Il server dovrebbe avviarsi correttamente")
    print("\n🚀 Per avviare il server:")
    print("   1. Apri terminale nella directory principale")
    print("   2. Esegui: cd backend")
    print("   3. Esegui: python server.py")
    print("   4. Verifica che dica 'Uvicorn running on http://0.0.0.0:8001'")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_backend_startup()