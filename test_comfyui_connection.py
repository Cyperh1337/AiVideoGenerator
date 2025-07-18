#!/usr/bin/env python3
"""
Test di connessione diretto a ComfyUI
Per debuggare il problema di connessione
"""

import requests
import aiohttp
import asyncio
import json
from datetime import datetime

async def test_comfyui_connection():
    """Test completo di connessione a ComfyUI"""
    
    # Test URLs
    urls_to_test = [
        "http://127.0.0.1:8188",
        "http://localhost:8188",
        "http://192.168.1.100:8188",  # Esempio IP locale
        "http://10.0.0.100:8188",     # Esempio IP locale alternativo
    ]
    
    print("=" * 60)
    print("ComfyUI Connection Test")
    print("=" * 60)
    
    for base_url in urls_to_test:
        print(f"\n🔍 Testing {base_url}")
        print("-" * 40)
        
        # Test 1: Requests library (sync)
        print("1. Testing with requests library...")
        try:
            response = requests.get(f"{base_url}/system_stats", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ SUCCESS: {response.status_code}")
                print(f"   📊 ComfyUI Version: {data.get('system', {}).get('comfyui_version', 'Unknown')}")
                print(f"   🐍 Python Version: {data.get('system', {}).get('python_version', 'Unknown')}")
            else:
                print(f"   ❌ FAIL: HTTP {response.status_code}")
        except requests.exceptions.ConnectionError as e:
            print(f"   ❌ Connection Error: {e}")
        except requests.exceptions.Timeout:
            print(f"   ❌ Timeout Error")
        except Exception as e:
            print(f"   ❌ Other Error: {e}")
        
        # Test 2: aiohttp library (async)
        print("2. Testing with aiohttp library...")
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"{base_url}/system_stats") as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"   ✅ SUCCESS: {response.status}")
                        print(f"   📊 ComfyUI Version: {data.get('system', {}).get('comfyui_version', 'Unknown')}")
                        print(f"   🐍 Python Version: {data.get('system', {}).get('python_version', 'Unknown')}")
                    else:
                        print(f"   ❌ FAIL: HTTP {response.status}")
        except aiohttp.ClientConnectorError as e:
            print(f"   ❌ Connection Error: {e}")
        except asyncio.TimeoutError:
            print(f"   ❌ Timeout Error")
        except Exception as e:
            print(f"   ❌ Other Error: {e}")
        
        # Test 3: Basic ping test
        print("3. Testing basic connectivity...")
        try:
            response = requests.get(f"{base_url}/", timeout=5)
            print(f"   ✅ Basic connection: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Basic connection failed: {e}")
        
        # Test 4: Test object_info endpoint
        print("4. Testing object_info endpoint...")
        try:
            response = requests.get(f"{base_url}/object_info", timeout=10)
            if response.status_code == 200:
                data = response.json()
                checkpoints = []
                loras = []
                
                # Check for checkpoints
                if "CheckpointLoaderSimple" in data:
                    checkpoint_loader = data["CheckpointLoaderSimple"]
                    if "input" in checkpoint_loader and "required" in checkpoint_loader["input"]:
                        if "ckpt_name" in checkpoint_loader["input"]["required"]:
                            checkpoints = checkpoint_loader["input"]["required"]["ckpt_name"][0]
                
                # Check for LoRAs
                if "LoraLoader" in data:
                    lora_loader = data["LoraLoader"]
                    if "input" in lora_loader and "required" in lora_loader["input"]:
                        if "lora_name" in lora_loader["input"]["required"]:
                            loras = lora_loader["input"]["required"]["lora_name"][0]
                
                print(f"   ✅ Object info: {response.status_code}")
                print(f"   📁 Checkpoints found: {len(checkpoints)}")
                print(f"   🎨 LoRAs found: {len(loras)}")
                
                if checkpoints:
                    print(f"   📋 Sample checkpoints: {checkpoints[:3]}")
                if loras:
                    print(f"   📋 Sample LoRAs: {loras[:3]}")
                    
            else:
                print(f"   ❌ Object info failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Object info error: {e}")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_comfyui_connection())