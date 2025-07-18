#!/usr/bin/env python3
"""
Debug script - Testa ESATTAMENTE il codice che usa l'app
"""

import os
import sys
import asyncio
import aiohttp
import requests
from pathlib import Path

# Simula l'ambiente dell'app
COMFYUI_BASE_URL = os.environ.get('COMFYUI_URL', 'http://127.0.0.1:8188')

async def test_like_app():
    """Test esatto come fa l'app"""
    
    print("=" * 60)
    print("🐛 DEBUG: Test esatto del codice dell'app")
    print("=" * 60)
    
    print(f"🔍 COMFYUI_BASE_URL: {COMFYUI_BASE_URL}")
    print(f"🔍 Environment COMFYUI_URL: {os.environ.get('COMFYUI_URL', 'NOT SET')}")
    
    # Test 1: Copia esatta della funzione get_comfyui_status
    print("\n1. Test funzione get_comfyui_status()...")
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"{COMFYUI_BASE_URL}/system_stats") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ Status: connected")
                    print(f"   📊 Data: {str(data)[:100]}...")
                else:
                    print(f"   ❌ Status: disconnected (HTTP {response.status})")
    except asyncio.TimeoutError:
        print(f"   ❌ Status: error (Connection timeout)")
    except aiohttp.ClientConnectorError as e:
        print(f"   ❌ Status: error (Connection refused: {str(e)})")
    except Exception as e:
        print(f"   ❌ Status: error ({str(e)})")
    
    # Test 2: Copia esatta della funzione get_available_checkpoints
    print("\n2. Test funzione get_available_checkpoints()...")
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"{COMFYUI_BASE_URL}/object_info") as response:
                if response.status == 200:
                    data = await response.json()
                    checkpoints = []
                    
                    # Extract checkpoint models
                    if "CheckpointLoaderSimple" in data:
                        checkpoint_loader = data["CheckpointLoaderSimple"]
                        if "input" in checkpoint_loader and "required" in checkpoint_loader["input"]:
                            if "ckpt_name" in checkpoint_loader["input"]["required"]:
                                checkpoints = checkpoint_loader["input"]["required"]["ckpt_name"][0]
                    
                    print(f"   ✅ Checkpoints: {len(checkpoints)}")
                    if checkpoints:
                        print(f"   📋 Sample: {checkpoints[:3]}")
                else:
                    print(f"   ❌ Checkpoints: HTTP {response.status}")
    except Exception as e:
        print(f"   ❌ Checkpoints: Error {str(e)}")
    
    # Test 3: Test diretto con requests
    print("\n3. Test con requests (per confronto)...")
    try:
        response = requests.get(f"{COMFYUI_BASE_URL}/system_stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Requests: SUCCESS")
            print(f"   📊 ComfyUI Version: {data.get('system', {}).get('comfyui_version', 'Unknown')}")
        else:
            print(f"   ❌ Requests: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Requests: Error {str(e)}")
    
    # Test 4: Test variabili d'ambiente
    print("\n4. Test configurazione environment...")
    print(f"   🔍 COMFYUI_URL env var: {os.environ.get('COMFYUI_URL', 'NOT SET')}")
    print(f"   🔍 MONGO_URL env var: {os.environ.get('MONGO_URL', 'NOT SET')}")
    print(f"   🔍 DB_NAME env var: {os.environ.get('DB_NAME', 'NOT SET')}")
    
    # Test 5: Test file .env
    print("\n5. Test file .env...")
    env_file = Path("backend/.env")
    if env_file.exists():
        print(f"   ✅ File .env exists: {env_file}")
        content = env_file.read_text()
        print(f"   📄 Content:\n{content}")
    else:
        print(f"   ❌ File .env NOT FOUND: {env_file}")
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNOSI:")
    print("=" * 60)
    
    # Test finale con curl per verifica
    print("\n6. Test finale con curl...")
    os.system(f"curl -s -m 5 {COMFYUI_BASE_URL}/system_stats | head -c 200")

if __name__ == "__main__":
    asyncio.run(test_like_app())