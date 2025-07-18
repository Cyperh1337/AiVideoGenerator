#!/usr/bin/env python3
"""
Test per verificare se il server backend sta funzionando
"""

import requests
import json
import time

def test_backend_server():
    """Test completo del server backend"""
    
    print("=" * 60)
    print("🔍 TEST SERVER BACKEND")
    print("=" * 60)
    
    backend_url = "http://localhost:8001"
    
    # Test 1: Verifica se il server è in ascolto
    print("\n1. Verifica server in ascolto...")
    try:
        response = requests.get(f"{backend_url}/api/", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Server backend ATTIVO")
            print(f"   📊 Response: {response.json()}")
        else:
            print(f"   ❌ Server backend: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Server backend NON RAGGIUNGIBILE: {e}")
        print("   🔧 Assicurati che il server backend sia in esecuzione")
        return False
    
    # Test 2: Test endpoint ComfyUI status
    print("\n2. Test endpoint ComfyUI status...")
    try:
        response = requests.get(f"{backend_url}/api/comfyui/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Endpoint status: OK")
            print(f"   📊 Status: {data.get('status', 'Unknown')}")
            print(f"   📊 Message: {data.get('message', 'No message')}")
            
            if data.get('status') == 'connected':
                print("   🎉 ComfyUI STATUS: CONNECTED!")
            else:
                print("   ❌ ComfyUI STATUS: NOT CONNECTED")
                print(f"   🔧 Errore: {data}")
        else:
            print(f"   ❌ Endpoint status: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Endpoint status ERROR: {e}")
    
    # Test 3: Test endpoint checkpoints
    print("\n3. Test endpoint checkpoints...")
    try:
        response = requests.get(f"{backend_url}/api/comfyui/checkpoints", timeout=10)
        if response.status_code == 200:
            data = response.json()
            checkpoints = data.get('checkpoints', [])
            print(f"   ✅ Endpoint checkpoints: OK")
            print(f"   📊 Checkpoints found: {len(checkpoints)}")
            if checkpoints:
                print(f"   📋 Sample: {checkpoints[:3]}")
        else:
            print(f"   ❌ Endpoint checkpoints: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Endpoint checkpoints ERROR: {e}")
    
    # Test 4: Test endpoint LoRAs
    print("\n4. Test endpoint LoRAs...")
    try:
        response = requests.get(f"{backend_url}/api/comfyui/loras", timeout=10)
        if response.status_code == 200:
            data = response.json()
            loras = data.get('loras', [])
            print(f"   ✅ Endpoint LoRAs: OK")
            print(f"   📊 LoRAs found: {len(loras)}")
            if loras:
                print(f"   📋 Sample: {loras[:3]}")
        else:
            print(f"   ❌ Endpoint LoRAs: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Endpoint LoRAs ERROR: {e}")
    
    # Test 5: Test endpoint debug
    print("\n5. Test endpoint debug...")
    try:
        response = requests.get(f"{backend_url}/api/comfyui/debug", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Endpoint debug: OK")
            print(f"   📊 ComfyUI URL: {data.get('comfyui_url', 'Unknown')}")
            print(f"   📊 Tests: {len(data.get('tests', []))}")
            
            for test in data.get('tests', []):
                test_name = test.get('test', 'Unknown')
                success = test.get('success', False)
                status = "✅" if success else "❌"
                print(f"      {status} {test_name}")
        else:
            print(f"   ❌ Endpoint debug: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Endpoint debug ERROR: {e}")
    
    # Test 6: Test configurazione
    print("\n6. Test configurazione ComfyUI...")
    try:
        response = requests.get(f"{backend_url}/api/comfyui/config", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Configurazione: OK")
            print(f"   📊 Base URL: {data.get('base_url', 'Unknown')}")
            print(f"   📊 WS URL: {data.get('ws_url', 'Unknown')}")
        else:
            print(f"   ❌ Configurazione: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Configurazione ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 ISTRUZIONI:")
    print("=" * 60)
    print("1. Esegui test_env_loading.py per verificare le variabili d'ambiente")
    print("2. Se tutto è OK, riavvia COMPLETAMENTE il server backend")
    print("3. Controlla la console del server per errori")
    print("4. Verifica che il frontend carichi correttamente")
    print("=" * 60)

if __name__ == "__main__":
    test_backend_server()