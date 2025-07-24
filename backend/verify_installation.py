#!/usr/bin/env python3
"""
Pathways-Agent Installation Verification Script
Checks if all dependencies are properly installed and working
"""

import sys
import subprocess
import importlib
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def check_system_dependencies():
    """Check system dependencies like FFmpeg"""
    print("\n🎵 Checking system dependencies...")
    
    # Check FFmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg - OK")
            return True
        else:
            print("❌ FFmpeg - Not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ FFmpeg - Not found. Install with: brew install ffmpeg (macOS) or sudo apt install ffmpeg (Ubuntu)")
        return False

def check_python_packages():
    """Check Python package dependencies"""
    print("\n📦 Checking Python packages...")
    
    required_packages = [
        # Core FastAPI Framework
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'uvicorn'),
        ('python-dotenv', 'dotenv'),
        ('python-multipart', 'multipart'),
        
        # HTTP Client
        ('httpx', 'httpx'),
        ('requests', 'requests'),
        
        # AI and LLM Integration
        ('openai', 'openai'),
        ('langchain', 'langchain'),
        ('langchain_openai', 'langchain_openai'),
        ('langchain_community', 'langchain_community'),
        
        # Vector Database
        ('faiss', 'faiss'),
        
        # Voice and Audio Processing
        ('whisper', 'whisper'),
        ('pydub', 'pydub'),
        ('librosa', 'librosa'),
        ('soundfile', 'soundfile'),
        ('numpy', 'numpy'),
        
        # Azure Integration
        ('azure.cognitiveservices.speech', 'azure_speech'),
        ('azure.storage.blob', 'azure_storage'),
        
        # Data Processing and Utilities
        ('pydantic', 'pydantic'),
        ('typing_extensions', 'typing_extensions'),
    ]
    
    all_ok = True
    for package_name, import_name in required_packages:
        try:
            if '.' in import_name:
                # Handle nested imports like azure.cognitiveservices.speech
                module_parts = import_name.split('.')
                module = importlib.import_module(module_parts[0])
                for part in module_parts[1:]:
                    module = getattr(module, part)
            else:
                module = importlib.import_module(import_name)
            
            # Get version if available
            try:
                version = getattr(module, '__version__', 'unknown')
                print(f"✅ {package_name} - {version}")
            except:
                print(f"✅ {package_name} - OK")
                
        except ImportError as e:
            print(f"❌ {package_name} - Missing: {e}")
            all_ok = False
        except Exception as e:
            print(f"⚠️  {package_name} - Warning: {e}")
    
    return all_ok

def check_environment_variables():
    """Check if required environment variables are set"""
    print("\n🔑 Checking environment variables...")
    
    import os
    from dotenv import load_dotenv
    
    # Load .env file if it exists
    env_file = Path('.env')
    if env_file.exists():
        load_dotenv()
        print("✅ .env file found and loaded")
    else:
        print("⚠️  .env file not found")
    
    # Check required variables
    required_vars = ['OPENAI_API_KEY']
    optional_vars = [
        'AZURE_SPEECH_KEY', 'AZURE_SPEECH_REGION', 'USE_AZURE_SPEECH',
        'AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_ENDPOINT', 'USE_AZURE_OPENAI',
        'OPENAI_MODEL', 'LOG_LEVEL'
    ]
    
    all_required_ok = True
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} - Set")
        else:
            print(f"❌ {var} - Missing (Required)")
            all_required_ok = False
    
    print("\nOptional variables:")
    for var in optional_vars:
        if os.getenv(var):
            print(f"✅ {var} - Set")
        else:
            print(f"⚪ {var} - Not set (Optional)")
    
    return all_required_ok

def test_audio_processing():
    """Test audio processing capabilities"""
    print("\n🎤 Testing audio processing...")
    
    try:
        from pydub import AudioSegment
        import tempfile
        import os
        
        # Create a simple test audio
        test_audio = AudioSegment.silent(duration=1000)  # 1 second of silence
        temp_file = tempfile.mktemp(suffix=".wav")
        test_audio.export(temp_file, format="wav")
        
        # Test audio loading
        loaded_audio = AudioSegment.from_file(temp_file)
        print("✅ Audio processing - OK")
        
        # Clean up
        os.remove(temp_file)
        return True
        
    except Exception as e:
        print(f"❌ Audio processing - Failed: {e}")
        return False

def test_whisper_model():
    """Test Whisper model loading"""
    print("\n🤖 Testing Whisper model...")
    
    try:
        import whisper
        model = whisper.load_model("tiny")  # Use tiny model for quick test
        print("✅ Whisper model - OK")
        return True
    except Exception as e:
        print(f"❌ Whisper model - Failed: {e}")
        return False

def test_openai_connection():
    """Test OpenAI API connection"""
    print("\n🧠 Testing OpenAI connection...")
    
    import os
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OpenAI API key not set - Skipping test")
        return True
    
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Simple test call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print("✅ OpenAI connection - OK")
        return True
    except Exception as e:
        print(f"❌ OpenAI connection - Failed: {e}")
        return False

def main():
    """Run all verification checks"""
    print("🔍 Pathways-Agent Installation Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("System Dependencies", check_system_dependencies),
        ("Python Packages", check_python_packages),
        ("Environment Variables", check_environment_variables),
        ("Audio Processing", test_audio_processing),
        ("Whisper Model", test_whisper_model),
        ("OpenAI Connection", test_openai_connection),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} - Error: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Your installation is ready.")
        print("\nNext steps:")
        print("1. Start the backend: python -m uvicorn main:app --reload")
        print("2. Start the frontend: cd ../frontend-react && npm start")
        print("3. Open http://localhost:3000 in your browser")
    else:
        print(f"\n⚠️  {total - passed} check(s) failed. Please review the issues above.")
        print("\nTroubleshooting:")
        print("1. Check the SETUP.md file for detailed instructions")
        print("2. Ensure all system dependencies are installed")
        print("3. Verify your .env file configuration")
        print("4. Check the logs for detailed error information")

if __name__ == "__main__":
    main() 