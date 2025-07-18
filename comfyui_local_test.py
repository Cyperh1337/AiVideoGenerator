#!/usr/bin/env python3
"""
Test di connessione ComfyUI per installazione locale
Esegui questo file nella tua installazione locale
"""

import requests
import sys
import os
from pathlib import Path

def test_local_comfyui():
    """Test ComfyUI locale"""
    
    print("=" * 60)
    print("🎬 ComfyUI Local Connection Test")
    print("=" * 60)
    
    # URLs da testare
    urls_to_test = [
        "http://127.0.0.1:8188",
        "http://localhost:8188",
    ]
    
    success_url = None
    
    for url in urls_to_test:
        print(f"\n🔍 Testing {url}")
        print("-" * 40)
        
        try:
            # Test system_stats
            response = requests.get(f"{url}/system_stats", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ ComfyUI CONNECTED!")
                print(f"   📊 Version: {data.get('system', {}).get('comfyui_version', 'Unknown')}")
                print(f"   🐍 Python: {data.get('system', {}).get('python_version', 'Unknown')}")
                print(f"   💾 RAM: {data.get('system', {}).get('ram_total', 0) / 1024**3:.1f} GB")
                
                # Test object_info
                obj_response = requests.get(f"{url}/object_info", timeout=10)
                if obj_response.status_code == 200:
                    obj_data = obj_response.json()
                    
                    # Count checkpoints
                    checkpoints = []
                    if "CheckpointLoaderSimple" in obj_data:
                        checkpoint_loader = obj_data["CheckpointLoaderSimple"]
                        if "input" in checkpoint_loader and "required" in checkpoint_loader["input"]:
                            if "ckpt_name" in checkpoint_loader["input"]["required"]:
                                checkpoints = checkpoint_loader["input"]["required"]["ckpt_name"][0]
                    
                    # Count LoRAs
                    loras = []
                    if "LoraLoader" in obj_data:
                        lora_loader = obj_data["LoraLoader"]
                        if "input" in lora_loader and "required" in lora_loader["input"]:
                            if "lora_name" in lora_loader["input"]["required"]:
                                loras = lora_loader["input"]["required"]["lora_name"][0]
                    
                    print(f"   📁 Checkpoints: {len(checkpoints)}")
                    print(f"   🎨 LoRAs: {len(loras)}")
                    
                    if checkpoints:
                        print(f"   📋 Sample checkpoints: {checkpoints[:3]}")
                    if loras:
                        print(f"   📋 Sample LoRAs: {loras[:3]}")
                
                success_url = url
                break
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection refused - ComfyUI not running")
        except requests.exceptions.Timeout:
            print(f"❌ Timeout - ComfyUI not responding")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    
    if success_url:
        print("🎉 SUCCESS! ComfyUI is accessible")
        print(f"✅ Use this URL in your app: {success_url}")
        
        # Check if we're in the app directory
        if Path("backend/server.py").exists():
            print("\n🔧 Fixing backend configuration...")
            try:
                # Update backend .env file
                env_file = Path("backend/.env")
                if env_file.exists():
                    content = env_file.read_text()
                    if "COMFYUI_URL" not in content:
                        content += f"\nCOMFYUI_URL={success_url}\n"
                        env_file.write_text(content)
                        print("✅ Backend .env updated")
                else:
                    env_file.write_text(f"COMFYUI_URL={success_url}\n")
                    print("✅ Backend .env created")
                    
            except Exception as e:
                print(f"❌ Could not update config: {e}")
    else:
        print("❌ FAIL! ComfyUI not accessible")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure ComfyUI is running")
        print("2. Check if it's accessible at http://127.0.0.1:8188")
        print("3. Try: python main.py in ComfyUI directory")
        print("4. Check ComfyUI console for errors")
    
    print("=" * 60)

if __name__ == "__main__":
    test_local_comfyui()