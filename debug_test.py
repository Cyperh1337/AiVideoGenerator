#!/usr/bin/env python3
"""
Debug test for video generation database issue
"""

import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / 'frontend' / '.env')

BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

def test_video_generation_debug():
    """Debug video generation and database storage"""
    
    print("🔍 Debug: Video Generation Database Issue")
    print(f"API Base: {API_BASE}")
    
    # Test 1: Create a video generation request
    video_request = {
        "prompt": "Debug test video generation",
        "checkpoint": "debug_checkpoint.safetensors",
        "width": 512,
        "height": 512,
        "frames": 16,
        "duration_type": "short"
    }
    
    print("\n1. Sending video generation request...")
    response = requests.post(f"{API_BASE}/generate/video", json=video_request)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test 2: Check generation history to see if record was created
    print("\n2. Checking generation history...")
    response = requests.get(f"{API_BASE}/generate/history")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"History records: {len(data)}")
        if data:
            print("Latest record:")
            latest = data[0]
            print(f"  ID: {latest.get('id')}")
            print(f"  Status: {latest.get('status')}")
            print(f"  Prompt: {latest.get('prompt')}")
            
            # Test 3: Try to get status of this record
            video_id = latest.get('id')
            if video_id:
                print(f"\n3. Testing status endpoint with ID: {video_id}")
                response = requests.get(f"{API_BASE}/generate/status/{video_id}")
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.text}")
    
    # Test 4: Test with a completely fake ID
    print("\n4. Testing with fake ID...")
    fake_id = "fake-video-id-12345"
    response = requests.get(f"{API_BASE}/generate/status/{fake_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_video_generation_debug()