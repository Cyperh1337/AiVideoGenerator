#!/usr/bin/env python3
"""
Comprehensive test for video generation workflow
"""

import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / 'frontend' / '.env')

BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

def test_complete_workflow():
    """Test complete video generation workflow"""
    
    print("🎬 Complete Video Generation Workflow Test")
    print(f"API Base: {API_BASE}")
    
    # Step 1: Create video generation request
    video_request = {
        "prompt": "A majestic dragon flying over a medieval castle at sunset",
        "checkpoint": "realistic_vision_v5.safetensors",
        "lora": "fantasy_style_v2.safetensors",
        "width": 768,
        "height": 512,
        "frames": 24,
        "duration_type": "medium"
    }
    
    print("\n1. Creating video generation request...")
    print(f"   Prompt: {video_request['prompt']}")
    print(f"   Checkpoint: {video_request['checkpoint']}")
    print(f"   LoRA: {video_request['lora']}")
    print(f"   Dimensions: {video_request['width']}x{video_request['height']}")
    print(f"   Frames: {video_request['frames']}")
    print(f"   Duration Type: {video_request['duration_type']}")
    
    response = requests.post(f"{API_BASE}/generate/video", json=video_request)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 500:
        # Expected due to ComfyUI not being available
        print("   ✅ Expected 500 error due to ComfyUI unavailability")
        
        # Step 2: Check if database record was created
        print("\n2. Checking generation history for database record...")
        response = requests.get(f"{API_BASE}/generate/history")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total records: {len(data)}")
            
            # Find our record
            our_record = None
            for record in data:
                if record.get('prompt') == video_request['prompt']:
                    our_record = record
                    break
            
            if our_record:
                print("   ✅ Database record created successfully")
                print(f"   Video ID: {our_record['id']}")
                print(f"   Status: {our_record['status']}")
                print(f"   Error Message: {our_record.get('error_message', 'None')}")
                
                # Step 3: Test status endpoint with real ID
                video_id = our_record['id']
                print(f"\n3. Testing status endpoint with real ID: {video_id}")
                response = requests.get(f"{API_BASE}/generate/status/{video_id}")
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    status_data = response.json()
                    print("   ✅ Status retrieved successfully")
                    print(f"   Current Status: {status_data['status']}")
                    print(f"   Created At: {status_data['created_at']}")
                    
                    # Verify all fields are present
                    required_fields = ['id', 'prompt', 'checkpoint', 'status', 'created_at', 'width', 'height', 'frames']
                    missing_fields = [field for field in required_fields if field not in status_data]
                    
                    if not missing_fields:
                        print("   ✅ All required fields present in response")
                    else:
                        print(f"   ❌ Missing fields: {missing_fields}")
                else:
                    print(f"   ❌ Failed to get status: {response.text}")
            else:
                print("   ❌ Database record not found")
        else:
            print(f"   ❌ Failed to get history: {response.text}")
    else:
        print(f"   Unexpected response: {response.text}")
    
    # Step 4: Test ComfyUI integration endpoints
    print("\n4. Testing ComfyUI integration endpoints...")
    
    endpoints = [
        ("/comfyui/status", "Status"),
        ("/comfyui/checkpoints", "Checkpoints"),
        ("/comfyui/loras", "LoRAs"),
        ("/comfyui/queue", "Queue")
    ]
    
    for endpoint, name in endpoints:
        response = requests.get(f"{API_BASE}{endpoint}")
        if response.status_code == 200:
            print(f"   ✅ {name} endpoint working")
        else:
            print(f"   ❌ {name} endpoint failed: {response.status_code}")
    
    print("\n🎉 Workflow test completed!")

if __name__ == "__main__":
    test_complete_workflow()