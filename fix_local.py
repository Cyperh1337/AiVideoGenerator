#!/usr/bin/env python3
"""
Fix per l'app locale - trova e risolve il problema
"""

import os
import requests
from pathlib import Path
import json

def fix_local_app():
    """Trova e risolve il problema della connessione locale"""
    
    print("=" * 60)
    print("🔧 FIXING LOCAL APP")
    print("=" * 60)
    
    # Step 1: Verifica ComfyUI
    print("\n1. Verifica ComfyUI...")
    comfyui_working = False
    comfyui_url = None
    
    for url in ["http://127.0.0.1:8188", "http://localhost:8188"]:
        try:
            response = requests.get(f"{url}/system_stats", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ ComfyUI trovato: {url}")
                comfyui_working = True
                comfyui_url = url
                break
        except:
            pass
    
    if not comfyui_working:
        print("   ❌ ComfyUI NON TROVATO!")
        print("   🔧 Assicurati che ComfyUI sia in esecuzione")
        print("   🔧 Prova: python main.py nella directory ComfyUI")
        return False
    
    # Step 2: Controlla struttura directory
    print("\n2. Verifica struttura directory...")
    required_files = [
        "backend/server.py",
        "frontend/src/App.js",
        "backend/requirements.txt",
        "frontend/package.json"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} MISSING")
    
    # Step 3: Controlla/Crea file .env
    print("\n3. Configura file .env...")
    env_file = Path("backend/.env")
    
    env_content = f"""COMFYUI_URL={comfyui_url}
MONGO_URL=mongodb://localhost:27017
DB_NAME=comfyui_video_generator
"""
    
    try:
        env_file.write_text(env_content)
        print(f"   ✅ File .env creato/aggiornato")
        print(f"   📄 Content:\n{env_content}")
    except Exception as e:
        print(f"   ❌ Errore creando .env: {e}")
    
    # Step 4: Controlla/Crea file frontend .env
    print("\n4. Configura frontend .env...")
    frontend_env_file = Path("frontend/.env")
    
    frontend_env_content = """REACT_APP_BACKEND_URL=http://localhost:8001
"""
    
    try:
        frontend_env_file.write_text(frontend_env_content)
        print(f"   ✅ Frontend .env creato/aggiornato")
    except Exception as e:
        print(f"   ❌ Errore creando frontend .env: {e}")
    
    # Step 5: Testa connessione dal backend
    print("\n5. Test connessione backend...")
    try:
        # Simula il caricamento delle env vars
        os.environ['COMFYUI_URL'] = comfyui_url
        os.environ['MONGO_URL'] = 'mongodb://localhost:27017'
        os.environ['DB_NAME'] = 'comfyui_video_generator'
        
        # Test esatto come fa il server
        import aiohttp
        import asyncio
        
        async def test_backend():
            try:
                timeout = aiohttp.ClientTimeout(total=5)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(f"{comfyui_url}/system_stats") as response:
                        if response.status == 200:
                            data = await response.json()
                            print(f"   ✅ Backend connection: SUCCESS")
                            print(f"   📊 ComfyUI Version: {data.get('system', {}).get('comfyui_version', 'Unknown')}")
                            return True
                        else:
                            print(f"   ❌ Backend connection: HTTP {response.status}")
                            return False
            except Exception as e:
                print(f"   ❌ Backend connection: {e}")
                return False
        
        backend_ok = asyncio.run(test_backend())
        
    except Exception as e:
        print(f"   ❌ Backend test error: {e}")
        backend_ok = False
    
    # Step 6: Istruzioni finali
    print("\n" + "=" * 60)
    print("🎯 RISULTATO:")
    print("=" * 60)
    
    if comfyui_working and backend_ok:
        print("✅ TUTTO OK! L'app dovrebbe funzionare")
        print("\n🚀 Avvia l'app:")
        print("   Windows: start.bat")
        print("   macOS/Linux: ./start.sh")
        print("\n🌐 Poi vai su: http://localhost:3000")
    else:
        print("❌ CI SONO ANCORA PROBLEMI")
        if not comfyui_working:
            print("   🔧 Problema: ComfyUI non accessibile")
        if not backend_ok:
            print("   🔧 Problema: Backend non si connette")
    
    print("=" * 60)
    
    return comfyui_working and backend_ok

if __name__ == "__main__":
    fix_local_app()