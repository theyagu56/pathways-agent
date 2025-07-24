# Pathways-Agent Setup Guide

This guide provides comprehensive setup instructions for the Pathways-Agent application, including all system dependencies and troubleshooting steps.

## 🖥️ System Requirements

### Operating System
- **macOS**: 10.15+ (Catalina or later)
- **Linux**: Ubuntu 18.04+, CentOS 7+, or similar
- **Windows**: Windows 10+ (with WSL2 recommended)

### Hardware Requirements
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: 2GB free space
- **CPU**: Multi-core processor (2+ cores recommended)

## 📋 Prerequisites

### 1. Python Environment
- **Python**: 3.8+ (3.9+ recommended)
- **pip**: Latest version
- **virtualenv** or **venv**: For environment isolation

### 2. Node.js Environment
- **Node.js**: 16+ (18+ recommended)
- **npm**: Latest version

### 3. System Dependencies

#### FFmpeg (Required for Audio Processing)
**macOS:**
```bash
# Using Homebrew
brew install ffmpeg

# Verify installation
ffmpeg -version
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

**CentOS/RHEL:**
```bash
sudo yum install epel-release
sudo yum install ffmpeg

# Verify installation
ffmpeg -version
```

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
# Add to PATH environment variable
```

#### Additional System Libraries (Linux)
```bash
# Ubuntu/Debian
sudo apt install build-essential python3-dev libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel portaudio-devel
```

## 🚀 Installation Steps

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd pathways-ai
```

### Step 2: Backend Setup

#### 2.1 Create Virtual Environment
```bash
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 2.2 Install Python Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

#### 2.3 Environment Configuration
Create a `.env` file in `backend/`:
```env
# Required: OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Azure Speech Services
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here
USE_AZURE_SPEECH=false

# Optional: Azure OpenAI (alternative to OpenAI)
AZURE_OPENAI_API_KEY=your_azure_openai_key_here
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint_here
AZURE_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2023-05-15
USE_AZURE_OPENAI=false

# Optional: Model Configuration
OPENAI_MODEL=gpt-3.5-turbo

# Optional: Logging
LOG_LEVEL=INFO
```

#### 2.4 Verify Backend Installation
```bash
# Test the installation
python -c "import fastapi, openai, whisper, pydub, numpy, soundfile; print('✅ All dependencies installed successfully')"

# Start the server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 3: Frontend Setup

#### 3.1 Install Node.js Dependencies
```bash
cd frontend
npm install
```

#### 3.2 Verify Frontend Installation
```bash
# Test the installation
npm run build

# Start the development server
npm start
```

## 🔧 Configuration

### API Keys Setup

#### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Navigate to API Keys section
4. Create a new API key
5. Add to your `.env` file

#### Azure Speech Services (Optional)
1. Visit [Azure Portal](https://portal.azure.com/)
2. Create a Speech Service resource
3. Get the key and region from the resource
4. Add to your `.env` file

### Audio Processing Configuration

#### Supported Audio Formats
- **Input**: WAV, MP3, M4A, FLAC, OGG
- **Processing**: Automatically converted to WAV
- **Quality**: 16kHz, mono (optimized for Whisper)

#### Audio File Size Limits
- **Maximum file size**: 25MB
- **Recommended duration**: 30 seconds - 5 minutes
- **Optimal quality**: 16-bit, 16kHz

## 🧪 Testing the Installation

### Backend Testing
```bash
cd backend

# Run the test suite
python test_voice_integration.py

# Test individual endpoints
curl http://localhost:8000/api/voice/health
curl http://localhost:8000/api/specialties
```

### Frontend Testing
```bash
cd frontend

# Run tests
npm test

# Build for production
npm run build
```

### Integration Testing
1. Start both backend and frontend servers
2. Open http://localhost:3000
3. Navigate to Voice Intake
4. Test voice recording and processing

## 🐛 Troubleshooting

### Common Issues

#### 1. FFmpeg Not Found
**Error**: `[Errno 2] No such file or directory: 'ffmpeg'`

**Solution**:
```bash
# Verify FFmpeg installation
ffmpeg -version

# If not found, install using package manager
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: choco install ffmpeg
```

#### 2. Audio Processing Errors
**Error**: `Audio preprocessing failed`

**Solution**:
```bash
# Install additional audio libraries
# Ubuntu/Debian:
sudo apt install libasound2-dev portaudio19-dev

# macOS:
brew install portaudio

# Verify pydub installation
python -c "from pydub import AudioSegment; print('Pydub OK')"
```

#### 3. Whisper Model Loading Issues
**Error**: `Failed to load Whisper model`

**Solution**:
```bash
# Clear Whisper cache
rm -rf ~/.cache/whisper

# Reinstall Whisper
pip uninstall openai-whisper
pip install openai-whisper

# Test model loading
python -c "import whisper; model = whisper.load_model('base'); print('Whisper OK')"
```

#### 4. Port Already in Use
**Error**: `[Errno 48] Address already in use`

**Solution**:
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or use a different port
python -m uvicorn main:app --port 8001
```

#### 5. Node.js Dependencies Issues
**Error**: `npm install` fails

**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# If still failing, try using yarn
npm install -g yarn
yarn install
```

### Performance Optimization

#### 1. Whisper Model Optimization
```bash
# Use smaller model for faster processing
# In voice_service.py, change:
self.whisper_model = whisper.load_model("tiny")  # Instead of "base"
```

#### 2. Audio Quality Optimization
```python
# In voice_service.py, adjust audio preprocessing:
audio = audio.set_frame_rate(8000)  # Lower sample rate for speed
```

#### 3. Memory Optimization
```bash
# Set environment variables for better memory management
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
```

## 📊 System Monitoring

### Log Files
- **Backend logs**: `backend/logs/`
- **Error logs**: `backend/logs/pathways-ai_errors_*.log`
- **Application logs**: `backend/logs/pathways-ai_*.log`

### Health Checks
```bash
# Backend health
curl http://localhost:8000/api/voice/health

# Frontend health
curl http://localhost:3000
```

### Performance Metrics
- **Voice transcription**: ~2-3 seconds for 30-second audio
- **Information extraction**: ~1-2 seconds
- **Provider matching**: ~1 second
- **Total response time**: ~4-6 seconds

## 🔒 Security Considerations

### API Key Security
- Never commit API keys to version control
- Use environment variables for all sensitive data
- Rotate API keys regularly
- Use least-privilege access for API keys

### Network Security
- Use HTTPS in production
- Configure CORS properly
- Implement rate limiting
- Use secure headers

### Data Privacy
- Audio files are processed locally when possible
- Temporary files are automatically cleaned up
- No audio data is stored permanently
- Implement data retention policies

## 📚 Additional Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Azure Speech Services](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/)
- [Whisper Documentation](https://github.com/openai/whisper)

### Support
- Create an issue in the GitHub repository
- Check the logs for detailed error information
- Review the API documentation at `/docs`

---

**Pathways-Agent Setup Complete!** 🎉

Your application should now be running at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs 