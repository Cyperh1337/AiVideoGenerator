from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import aiohttp
import asyncio
import json
import websockets
import base64
from contextlib import asynccontextmanager

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# ComfyUI Configuration
COMFYUI_BASE_URL = os.environ.get('COMFYUI_URL', 'http://127.0.0.1:8188')
COMFYUI_WS_URL = os.environ.get('COMFYUI_WS_URL', 'ws://127.0.0.1:8188/ws')

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logging.info("Starting ComfyUI Video Generator backend...")
    yield
    # Shutdown
    logging.info("Shutting down ComfyUI Video Generator backend...")
    client.close()

# Create the main app with lifespan
app = FastAPI(lifespan=lifespan)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class VideoGenerationRequest(BaseModel):
    prompt: str
    checkpoint: str
    lora: Optional[str] = None
    width: int = 512
    height: int = 512
    frames: int = 16
    duration_type: str = "short"  # short, medium, long
    
class VideoGeneration(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prompt: str
    checkpoint: str
    lora: Optional[str] = None
    width: int
    height: int
    frames: int
    duration_type: str
    status: str = "pending"  # pending, processing, completed, failed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    result_path: Optional[str] = None
    error_message: Optional[str] = None
    comfyui_prompt_id: Optional[str] = None

class ComfyUIService:
    @staticmethod
    async def get_available_checkpoints():
        """Get available checkpoints from ComfyUI"""
        try:
            timeout = aiohttp.ClientTimeout(total=10)  # 10 second timeout
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
                        
                        return checkpoints
                    else:
                        logger.error(f"ComfyUI returned status {response.status}")
                        return []
        except asyncio.TimeoutError:
            logger.error("Timeout connecting to ComfyUI")
            return []
        except aiohttp.ClientConnectorError as e:
            logger.error(f"Connection error to ComfyUI: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting checkpoints: {e}")
            return []

    @staticmethod
    async def get_available_loras():
        """Get available LoRA models from ComfyUI"""
        try:
            timeout = aiohttp.ClientTimeout(total=10)  # 10 second timeout
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"{COMFYUI_BASE_URL}/object_info") as response:
                    if response.status == 200:
                        data = await response.json()
                        loras = []
                        
                        # Extract LoRA models
                        if "LoraLoader" in data:
                            lora_loader = data["LoraLoader"]
                            if "input" in lora_loader and "required" in lora_loader["input"]:
                                if "lora_name" in lora_loader["input"]["required"]:
                                    loras = lora_loader["input"]["required"]["lora_name"][0]
                        
                        return loras
                    else:
                        logger.error(f"ComfyUI returned status {response.status}")
                        return []
        except asyncio.TimeoutError:
            logger.error("Timeout connecting to ComfyUI")
            return []
        except aiohttp.ClientConnectorError as e:
            logger.error(f"Connection error to ComfyUI: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting LoRAs: {e}")
            return []

    @staticmethod
    async def create_video_workflow(request: VideoGenerationRequest):
        """Create ComfyUI workflow for video generation"""
        
        # Set frames based on duration type
        if request.duration_type == "short":
            frames = min(request.frames, 30)  # TikTok short
        elif request.duration_type == "medium":
            frames = min(request.frames, 120)  # Medium video
        else:
            frames = min(request.frames, 600)  # Long video
        
        # Basic video generation workflow
        workflow = {
            "3": {
                "inputs": {
                    "seed": 156680208700286,
                    "steps": 20,
                    "cfg": 8.0,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler",
                "_meta": {
                    "title": "KSampler"
                }
            },
            "4": {
                "inputs": {
                    "ckpt_name": request.checkpoint
                },
                "class_type": "CheckpointLoaderSimple",
                "_meta": {
                    "title": "Load Checkpoint"
                }
            },
            "5": {
                "inputs": {
                    "width": request.width,
                    "height": request.height,
                    "batch_size": frames
                },
                "class_type": "EmptyLatentImage",
                "_meta": {
                    "title": "Empty Latent Image"
                }
            },
            "6": {
                "inputs": {
                    "text": request.prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "CLIP Text Encode (Prompt)"
                }
            },
            "7": {
                "inputs": {
                    "text": "blurry, low quality, distorted",
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "CLIP Text Encode (Negative)"
                }
            },
            "8": {
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                },
                "class_type": "VAEDecode",
                "_meta": {
                    "title": "VAE Decode"
                }
            },
            "9": {
                "inputs": {
                    "filename_prefix": "ComfyUI_video",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage",
                "_meta": {
                    "title": "Save Image"
                }
            }
        }
        
        # Add LoRA if specified
        if request.lora:
            workflow["10"] = {
                "inputs": {
                    "lora_name": request.lora,
                    "strength_model": 1.0,
                    "strength_clip": 1.0,
                    "model": ["4", 0],
                    "clip": ["4", 1]
                },
                "class_type": "LoraLoader",
                "_meta": {
                    "title": "Load LoRA"
                }
            }
            # Update model and clip references
            workflow["3"]["inputs"]["model"] = ["10", 0]
            workflow["6"]["inputs"]["clip"] = ["10", 1]
            workflow["7"]["inputs"]["clip"] = ["10", 1]
        
        return workflow

    @staticmethod
    async def queue_prompt(workflow):
        """Queue a prompt in ComfyUI"""
        try:
            prompt_data = {
                "prompt": workflow,
                "client_id": str(uuid.uuid4())
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{COMFYUI_BASE_URL}/prompt", json=prompt_data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("prompt_id"), prompt_data["client_id"]
                    else:
                        return None, None
        except Exception as e:
            logger.error(f"Error queuing prompt: {e}")
            return None, None

    @staticmethod
    async def get_queue_status():
        """Get ComfyUI queue status"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{COMFYUI_BASE_URL}/queue") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return None
        except Exception as e:
            logger.error(f"Error getting queue status: {e}")
            return None

    @staticmethod
    async def get_images(filename, subfolder="", folder_type="output"):
        """Get generated images from ComfyUI"""
        try:
            params = {
                "filename": filename,
                "subfolder": subfolder,
                "type": folder_type
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{COMFYUI_BASE_URL}/view", params=params) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        return base64.b64encode(image_data).decode('utf-8')
                    else:
                        return None
        except Exception as e:
            logger.error(f"Error getting images: {e}")
            return None

# API Routes
@api_router.get("/")
async def root():
    return {"message": "ComfyUI Video Generator API"}

@api_router.get("/comfyui/config")
async def get_comfyui_config():
    """Get current ComfyUI configuration"""
    return {
        "base_url": COMFYUI_BASE_URL,
        "ws_url": COMFYUI_WS_URL
    }

@api_router.post("/comfyui/config")
async def set_comfyui_config(config: dict):
    """Set ComfyUI configuration"""
    global COMFYUI_BASE_URL, COMFYUI_WS_URL
    
    if 'base_url' in config:
        COMFYUI_BASE_URL = config['base_url']
        COMFYUI_WS_URL = config['base_url'].replace('http://', 'ws://').replace('https://', 'wss://') + '/ws'
    
    return {
        "success": True,
        "base_url": COMFYUI_BASE_URL,
        "ws_url": COMFYUI_WS_URL
    }

@api_router.get("/comfyui/status")
async def get_comfyui_status():
    """Check ComfyUI connection status"""
    try:
        timeout = aiohttp.ClientTimeout(total=5)  # 5 second timeout
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"{COMFYUI_BASE_URL}/system_stats") as response:
                if response.status == 200:
                    data = await response.json()
                    return {"status": "connected", "data": data}
                else:
                    return {"status": "disconnected", "error": f"HTTP {response.status}"}
    except asyncio.TimeoutError:
        return {"status": "error", "message": "Connection timeout"}
    except aiohttp.ClientConnectorError as e:
        return {"status": "error", "message": f"Connection refused: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@api_router.get("/comfyui/checkpoints")
async def get_checkpoints():
    """Get available checkpoints"""
    checkpoints = await ComfyUIService.get_available_checkpoints()
    return {"checkpoints": checkpoints}

@api_router.get("/comfyui/loras")
async def get_loras():
    """Get available LoRA models"""
    loras = await ComfyUIService.get_available_loras()
    return {"loras": loras}

@api_router.post("/generate/video")
async def generate_video(request: VideoGenerationRequest):
    """Generate video using ComfyUI"""
    try:
        # Create video generation record
        video_gen = VideoGeneration(
            prompt=request.prompt,
            checkpoint=request.checkpoint,
            lora=request.lora,
            width=request.width,
            height=request.height,
            frames=request.frames,
            duration_type=request.duration_type
        )
        
        # Save to database
        await db.video_generations.insert_one(video_gen.dict())
        
        # Create workflow
        workflow = await ComfyUIService.create_video_workflow(request)
        
        # Queue prompt
        prompt_id, client_id = await ComfyUIService.queue_prompt(workflow)
        
        if prompt_id:
            # Update record with prompt_id
            await db.video_generations.update_one(
                {"id": video_gen.id},
                {"$set": {"comfyui_prompt_id": prompt_id, "status": "processing"}}
            )
            
            return {
                "success": True,
                "video_id": video_gen.id,
                "prompt_id": prompt_id,
                "message": "Video generation started"
            }
        else:
            # Update record with error
            await db.video_generations.update_one(
                {"id": video_gen.id},
                {"$set": {"status": "failed", "error_message": "Failed to queue prompt"}}
            )
            
            raise HTTPException(status_code=500, detail="Failed to queue prompt in ComfyUI")
            
    except Exception as e:
        logger.error(f"Error generating video: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/generate/status/{video_id}")
async def get_video_status(video_id: str):
    """Get video generation status"""
    try:
        # Get from database
        video_gen = await db.video_generations.find_one({"id": video_id})
        
        if not video_gen:
            raise HTTPException(status_code=404, detail="Video generation not found")
        
        # Check ComfyUI queue status if still processing
        if video_gen["status"] == "processing":
            queue_status = await ComfyUIService.get_queue_status()
            if queue_status:
                # Check if prompt is still in queue
                running = queue_status.get("queue_running", [])
                pending = queue_status.get("queue_pending", [])
                
                prompt_id = video_gen.get("comfyui_prompt_id")
                
                # Check if completed
                if not any(item[1] == prompt_id for item in running + pending):
                    # Prompt completed, update status
                    await db.video_generations.update_one(
                        {"id": video_id},
                        {"$set": {"status": "completed", "completed_at": datetime.utcnow()}}
                    )
                    video_gen["status"] = "completed"
        
        return VideoGeneration(**video_gen)
        
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except Exception as e:
        logger.error(f"Error getting video status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/generate/history")
async def get_generation_history():
    """Get generation history"""
    try:
        generations = await db.video_generations.find().sort("created_at", -1).limit(50).to_list(50)
        return [VideoGeneration(**gen) for gen in generations]
    except Exception as e:
        logger.error(f"Error getting generation history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/comfyui/queue")
async def get_queue():
    """Get ComfyUI queue status"""
    queue_status = await ComfyUIService.get_queue_status()
    return queue_status or {"queue_running": [], "queue_pending": []}

# Original status routes
@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)