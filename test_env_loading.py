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
    env_file = Path("backend/.env")
    
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
    
    # Simula esattamente quello che fa il server
    ROOT_DIR = Path("backend")
    dotenv_path = ROOT_DIR / '.env'
    
    print(f"   🔍 Caricando da: {dotenv_path}")
    result = load_dotenv(dotenv_path)
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
    
    # Test 4: Test con COMFYUI_URL
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
    
    # Test 5: Test esatto del codice server
    print("\n5. Test esatto del codice server...")
    
    # Simula l'import del server
    print("   🔍 Simulando import server...")
    
    # Aggiungi il path del backend
    backend_path = Path("backend").resolve()
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    
    # Cambia directory come fa il server
    original_dir = os.getcwd()
    os.chdir("backend")
    
    try:
        # Carica .env come fa il server
        from pathlib import Path
        from dotenv import load_dotenv
        
        ROOT_DIR = Path(__file__).parent
        load_dotenv(ROOT_DIR / '.env')
        
        # Verifica le variabili
        comfyui_base_url = os.environ.get('COMFYUI_URL', 'http://127.0.0.1:8188')
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME')
        
        print(f"   🔍 COMFYUI_BASE_URL: {comfyui_base_url}")
        print(f"   🔍 MONGO_URL: {mongo_url}")
        print(f"   🔍 DB_NAME: {db_name}")
        
        # Test connessione
        import aiohttp
        import asyncio
        
        async def test_server_connection():
            try:
                timeout = aiohttp.ClientTimeout(total=5)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(f"{comfyui_base_url}/system_stats") as response:
                        if response.status == 200:
                            data = await response.json()
                            print(f"   ✅ Server connection: SUCCESS")
                            print(f"   📊 Version: {data.get('system', {}).get('comfyui_version', 'Unknown')}")
                            return True
                        else:
                            print(f"   ❌ Server connection: HTTP {response.status}")
                            return False
            except Exception as e:
                print(f"   ❌ Server connection: {e}")
                return False
        
        server_ok = asyncio.run(test_server_connection())
        
    except Exception as e:
        print(f"   ❌ Server test error: {e}")
        server_ok = False
    finally:
        os.chdir(original_dir)
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNOSI:")
    print("=" * 60)
    
    if server_ok:
        print("✅ TUTTO OK! Il server dovrebbe funzionare")
        print("\n🔧 Se l'app ancora non funziona:")
        print("   1. Riavvia COMPLETAMENTE il server backend")
        print("   2. Controlla la console del server per errori")
        print("   3. Verifica che il server usi il file .env corretto")
    else:
        print("❌ CI SONO ANCORA PROBLEMI")
        print("\n🔧 Possibili soluzioni:")
        print("   1. Il server non sta caricando il file .env")
        print("   2. Il server non sta usando la variabile COMFYUI_URL")
        print("   3. Problema nel codice del server")
    
    print("=" * 60)

if __name__ == "__main__":
    test_env_loading()