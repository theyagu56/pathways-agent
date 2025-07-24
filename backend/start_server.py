#!/usr/bin/env python3
"""
Helper script to start the FastAPI server with better error handling
"""

import os
import sys
import json
from pathlib import Path

def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check if we're in the right place
    if not (current_dir / "main.py").exists():
        print("❌ main.py not found in current directory")
        print("💡 Make sure you're in the backend-fastapi directory")
        return False
    
    # Check for providers.json in various locations
    possible_paths = [
        Path("../shared-data/providers.json"),
        Path("./shared-data/providers.json"),
        Path("../../shared-data/providers.json"),
        Path("/Users/thiyagarajankamalakannan/Projects/CursorPathwayAgent/pathways-ai/shared-data/providers.json")
    ]
    
    providers_found = False
    for path in possible_paths:
        if path.exists():
            print(f"✅ Found providers.json at: {path}")
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    print(f"   📊 Contains {len(data)} providers")
                providers_found = True
                break
            except Exception as e:
                print(f"   ❌ Error reading file: {e}")
        else:
            print(f"❌ Not found: {path}")
    
    if not providers_found:
        print("❌ No valid providers.json file found!")
        return False
    
    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OpenAI API Key: {'*' * (len(api_key) - 4) + api_key[-4:]}")
    else:
        print("⚠️  OpenAI API Key not set (will use fallback specialties)")
    
    return True

def start_server():
    """Start the FastAPI server"""
    if not check_environment():
        print("❌ Environment check failed. Please fix the issues above.")
        sys.exit(1)
    
    print("\n🚀 Starting FastAPI server...")
    print("=" * 50)
    
    try:
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except ImportError:
        print("❌ uvicorn not installed. Please run: pip install uvicorn")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server() 