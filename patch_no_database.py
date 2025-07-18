#!/usr/bin/env python3
"""
Patch per far funzionare l'app senza MongoDB
"""

import os
from pathlib import Path

def patch_no_database():
    """Patch per rimuovere temporaneamente MongoDB"""
    
    print("=" * 60)
    print("🔧 PATCH: Rimozione temporanea MongoDB")
    print("=" * 60)
    
    # Leggi server.py
    server_file = Path("backend/server.py")
    if not server_file.exists():
        print("❌ File server.py non trovato")
        return
    
    content = server_file.read_text()
    
    # Patch 1: Rimuovi connessione MongoDB
    content = content.replace(
        "client = AsyncIOMotorClient(mongo_url)",
        "# client = AsyncIOMotorClient(mongo_url)  # DISABLED"
    )
    
    content = content.replace(
        "db = client[os.environ['DB_NAME']]",
        "# db = client[os.environ['DB_NAME']]  # DISABLED"
    )
    
    # Patch 2: Sostituisci operazioni database con memoria
    content = content.replace(
        "await db.video_generations.insert_one(video_gen.dict())",
        "# await db.video_generations.insert_one(video_gen.dict())  # DISABLED\n        print(f'Video generation created: {video_gen.id}')"
    )
    
    content = content.replace(
        "await db.video_generations.update_one(",
        "# await db.video_generations.update_one(  # DISABLED\n        print(f'Video generation updated: {video_gen.id}')\n        # Original code:"
    )
    
    content = content.replace(
        'await db.video_generations.find_one({"id": video_id})',
        '# await db.video_generations.find_one({"id": video_id})  # DISABLED\n        None  # Return None for now'
    )
    
    content = content.replace(
        "await db.video_generations.find().sort(\"created_at\", -1).limit(50).to_list(50)",
        "# await db.video_generations.find().sort(\"created_at\", -1).limit(50).to_list(50)  # DISABLED\n        []  # Return empty list for now"
    )
    
    # Patch 3: Correggi Pydantic deprecation
    content = content.replace(
        "video_gen.dict()",
        "video_gen.model_dump()"
    )
    
    content = content.replace(
        "status_obj.dict()",
        "status_obj.model_dump()"
    )
    
    # Salva il file patchato
    server_file.write_text(content)
    
    print("✅ Patch applicata a server.py")
    print("⚠️  MongoDB temporaneamente disabilitato")
    print("📊 Cronologia generazioni non sarà salvata")
    print("🎬 Ma la generazione video funzionerà!")
    
    print("\n🚀 Riavvia il server:")
    print("   1. Ferma il server (Ctrl+C)")
    print("   2. Riavvia: python server.py")
    
    print("=" * 60)

if __name__ == "__main__":
    patch_no_database()