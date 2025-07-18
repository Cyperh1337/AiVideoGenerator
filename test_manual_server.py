#!/usr/bin/env python3
"""
Test manuale del server - versione semplificata
"""

import os
import sys
from pathlib import Path

def test_manual_server():
    """Test manuale del server"""
    
    print("=" * 60)
    print("🔍 TEST MANUALE SERVER")
    print("=" * 60)
    
    # Cambia directory
    original_dir = os.getcwd()
    os.chdir("backend")
    
    print(f"📁 Directory corrente: {os.getcwd()}")
    print(f"🐍 Python: {sys.executable}")
    
    # Carica le variabili d'ambiente
    from dotenv import load_dotenv
    load_dotenv('.env')
    
    print(f"🔧 COMFYUI_URL: {os.environ.get('COMFYUI_URL', 'NOT SET')}")
    print(f"🔧 MONGO_URL: {os.environ.get('MONGO_URL', 'NOT SET')}")
    print(f"🔧 DB_NAME: {os.environ.get('DB_NAME', 'NOT SET')}")
    
    # Test import del server
    print("\n🔍 Importando moduli...")
    
    try:
        from fastapi import FastAPI
        print("   ✅ FastAPI imported")
    except Exception as e:
        print(f"   ❌ FastAPI error: {e}")
        return
    
    try:
        import uvicorn
        print("   ✅ Uvicorn imported")
    except Exception as e:
        print(f"   ❌ Uvicorn error: {e}")
        return
    
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        print("   ✅ Motor imported")
    except Exception as e:
        print(f"   ❌ Motor error: {e}")
        return
    
    try:
        import aiohttp
        print("   ✅ aiohttp imported")
    except Exception as e:
        print(f"   ❌ aiohttp error: {e}")
        return
    
    # Test MongoDB connection
    print("\n🔍 Test MongoDB...")
    mongo_url = os.environ.get('MONGO_URL')
    if mongo_url:
        try:
            client = AsyncIOMotorClient(mongo_url)
            print("   ✅ MongoDB client created")
        except Exception as e:
            print(f"   ❌ MongoDB error: {e}")
    else:
        print("   ❌ MONGO_URL not set")
    
    # Test caricamento server.py
    print("\n🔍 Test caricamento server.py...")
    
    try:
        # Leggi il file server.py
        with open("server.py", "r") as f:
            content = f.read()
        
        print(f"   📄 server.py size: {len(content)} characters")
        
        # Controlla se ha la sezione di avvio
        if "if __name__" in content:
            print("   ✅ Ha sezione __main__")
        else:
            print("   ❌ MANCA sezione __main__")
            print("   🔧 Questo potrebbe essere il problema!")
            
        # Controlla se ha uvicorn.run
        if "uvicorn.run" in content:
            print("   ✅ Ha uvicorn.run")
        else:
            print("   ❌ MANCA uvicorn.run")
            print("   🔧 Questo potrebbe essere il problema!")
            
    except Exception as e:
        print(f"   ❌ Errore leggendo server.py: {e}")
    
    # Test di avvio diretto
    print("\n🔍 Test avvio diretto...")
    
    try:
        print("   🔍 Creando app FastAPI...")
        app = FastAPI()
        
        @app.get("/")
        async def root():
            return {"message": "Test server"}
        
        print("   ✅ App FastAPI creata")
        
        print("   🔍 Avviando con uvicorn...")
        print("   ⚠️  Questo dovrebbe avviare il server...")
        
        # Avvia server con uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8001)
        
    except Exception as e:
        print(f"   ❌ Errore avvio diretto: {e}")
    
    os.chdir(original_dir)

if __name__ == "__main__":
    test_manual_server()