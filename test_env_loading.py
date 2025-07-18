#!/usr/bin/env python3
"""
Test per verificare se il server Python carica le variabili d'ambiente
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def test_env_loading():
    """Test caricamento variabili d'ambiente"""
    
    print("=" * 60)
    print("🔍 TEST CARICAMENTO VARIABILI D'AMBIENTE")
    print("=" * 60)
    
    # Test 1: Verifica file .env
    print("\n1. Verifica file .env...")
    env_file = Path("backend") / ".env"
    
    if env_file.exists():
        print(f"   ✅ File .env trovato: {env_file}")
        content = env_file.read_text()
        print(f"   📄 Contenuto:")
        for line in content.split('\n'):
            if line.strip():
                print(f"      {line}")
    else:
        print(f"   ❌ File .env NON TROVATO")
        return False
    
    # Test 2: Carica variabili d'ambiente
    print("\n2. Caricamento variabili d'ambiente...")
    
    # Carica il file .env
    result = load_dotenv(env_file)
    print(f"   🔍 load_dotenv result: {result}")
    
    # Test 3: Verifica variabili caricate
    print("\n3. Verifica variabili caricate...")
    
    vars_to_check = ['COMFYUI_URL', 'MONGO_URL', 'DB_NAME']
    
    for var in vars_to_check:
        value = os.environ.get(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: NOT SET")
    
    # Test 4: Test connessione con COMFYUI_URL
    print("\n4. Test connessione con COMFYUI_URL...")
    
    comfyui_url = os.environ.get('COMFYUI_URL', 'http://127.0.0.1:8188')
    print(f"   🔍 URL da usare: {comfyui_url}")
    
    try:
        import requests
        response = requests.get(f"{comfyui_url}/system_stats", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Connessione OK con {comfyui_url}")
        else:
            print(f"   ❌ Connessione FAIL: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connessione ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNOSI:")
    print("=" * 60)
    print("✅ Test completato - ora controlla perché il server non si avvia")
    print("=" * 60)

if __name__ == "__main__":
    test_env_loading()