# Voice-Enabled Healthcare Intake System

## 🎤 Overview

This enhancement adds voice-to-text capabilities to the healthcare triage application, allowing users to:

- **Record audio** directly in the browser
- **Upload audio files** for processing
- **Use text input** as a fallback
- **Auto-extract** symptoms, zip codes, and specialty recommendations
- **Seamlessly integrate** with the existing provider matching system

## 🚀 Features

### Voice Processing Pipeline
1. **Audio Input**: Record via microphone or upload audio files
2. **Transcription**: Convert speech to text using Whisper (local) or Azure Speech Services
3. **Information Extraction**: Parse symptoms, location, and insurance details
4. **LLM Analysis**: Get specialty recommendations based on symptoms
5. **Provider Matching**: Find and rank healthcare providers

### Input Methods
- 🎤 **Voice Recording**: Real-time audio recording in the browser
- 📁 **File Upload**: Support for various audio formats (WAV, MP3, M4A, etc.)
- ✏️ **Text Input**: Manual text entry as fallback

### Processing Options
- **Local Processing**: Uses OpenAI Whisper for offline transcription
- **Azure Integration**: Optional Azure Speech Services for enhanced accuracy
- **Hybrid Approach**: Automatic fallback between services

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the `backend` directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Azure Speech Services (Optional)
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here
USE_AZURE_SPEECH=false

# Application Configuration
ENVIRONMENT=local
LOG_LEVEL=INFO
```

### 3. Azure Speech Services Setup (Optional)

1. Create an Azure Speech Services resource in the Azure portal
2. Get your subscription key and region
3. Set the environment variables:
   ```env
   AZURE_SPEECH_KEY=your_key_here
   AZURE_SPEECH_REGION=your_region_here
   USE_AZURE_SPEECH=true
   ```

### 4. Start the Backend

```bash
cd backend
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Start the Frontend

```bash
cd frontend
npm start
```

## 📡 API Endpoints

### Voice Processing Endpoints

#### POST `/api/voice/upload-audio`
Upload and process audio files for complete healthcare intake.

**Request:**
- `audio_file`: Audio file (WAV, MP3, M4A, etc.)
- `insurance`: Insurance provider name

**Response:**
```json
{
  "success": true,
  "voice_processing": {
    "transcription": "I have a severe headache and live in 75024",
    "confidence": 0.95,
    "processing_method": "whisper"
  },
  "extracted_info": {
    "symptoms": "I have a severe headache and live in 75024",
    "zip_code": "75024",
    "insurance": "Cigna"
  },
  "specialty_recommendations": ["Neurology", "Primary Care"],
  "providers": [...],
  "total_providers_found": 5
}
```

#### POST `/api/voice/process-text`
Process text input for healthcare intake.

**Request:**
- `text_input`: Text description of symptoms
- `insurance`: Insurance provider name

#### GET `/api/voice/health`
Get health status of voice processing services.

#### POST `/api/voice/test-audio`
Test audio transcription without full processing.

## 🎯 Usage Examples

### Voice Recording
1. Navigate to "Voice Intake" in the application
2. Select your insurance provider
3. Click "Start Recording" and speak your symptoms
4. Include your zip code in the recording
5. Click "Stop Recording" when done
6. Click "Process Audio" to get results

### Audio File Upload
1. Select "Upload Audio" mode
2. Choose an audio file from your device
3. Select insurance provider
4. Click "Process Audio"

### Text Input
1. Select "Text Input" mode
2. Type your symptoms and zip code
3. Select insurance provider
4. Click "Process Text"

## 🔧 Technical Details

### Audio Processing
- **Supported Formats**: WAV, MP3, M4A, FLAC, OGG
- **Sample Rate**: Automatically converted to 16kHz for optimal processing
- **Channels**: Converted to mono if stereo
- **File Size**: Limited to 10MB by default

### Transcription Services
- **Whisper (Local)**: OpenAI's Whisper model for offline processing
- **Azure Speech Services**: Microsoft's cloud-based speech recognition
- **Fallback**: Automatic fallback to Whisper if Azure fails

### Information Extraction
- **Zip Code Detection**: Regex pattern matching for 5-digit codes
- **Symptom Extraction**: Full transcription used as symptom description
- **Specialty Matching**: LLM-based specialty recommendation

### Provider Matching
- **Specialty Filtering**: Providers filtered by recommended specialties
- **Distance Calculation**: Based on zip code proximity
- **Insurance Matching**: Provider availability and insurance acceptance
- **Ranking**: Multi-factor scoring system

## 🚀 Deployment to Azure

### Phase 1: Local Development ✅
- Voice processing works entirely locally
- Whisper model runs on local machine
- No external dependencies for basic functionality

### Phase 2: Azure Integration (Future)
1. **Azure Speech Services**: Enhanced transcription accuracy
2. **Azure OpenAI**: LLM processing in the cloud
3. **Azure Storage**: Audio file storage and processing
4. **Azure App Service**: Host the FastAPI backend
5. **Azure Static Web Apps**: Host the React frontend

### Azure Configuration
```env
# Production Azure Settings
AZURE_SPEECH_KEY=your_production_key
AZURE_SPEECH_REGION=your_production_region
USE_AZURE_SPEECH=true
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_STORAGE_CONNECTION_STRING=your_storage_connection_string
```

## 🔍 Troubleshooting

### Common Issues

#### Audio Recording Not Working
- Check browser permissions for microphone access
- Ensure HTTPS is used in production (required for getUserMedia)
- Try a different browser (Chrome recommended)

#### Transcription Errors
- Check audio file format and size
- Verify Whisper model is downloaded
- Check Azure Speech Services configuration

#### Provider Matching Issues
- Verify providers.json file is accessible
- Check specialty service initialization
- Review LLM API key configuration

### Debug Mode
Enable debug logging by setting:
```env
LOG_LEVEL=DEBUG
```

### Health Check
Test voice services health:
```bash
curl http://localhost:8000/api/voice/health
```

## 📊 Performance Considerations

### Local Processing
- **Whisper Model Size**: Base model (~1GB) provides good accuracy
- **Memory Usage**: ~2GB RAM recommended for voice processing
- **Processing Time**: 2-5 seconds for typical audio clips

### Azure Processing
- **Latency**: 1-3 seconds for cloud transcription
- **Cost**: Pay-per-use pricing model
- **Availability**: 99.9% SLA for Azure Speech Services

## 🔒 Security & Privacy

### Data Handling
- Audio files are processed in memory and not stored
- Temporary files are automatically cleaned up
- No audio data is logged or persisted

### Privacy Compliance
- HIPAA-compliant data handling
- No PII extraction or storage
- Secure transmission of audio data

## 🎯 Future Enhancements

### Planned Features
- **Real-time Transcription**: Live transcription during recording
- **Multi-language Support**: International language processing
- **Voice Commands**: Navigation and control via voice
- **Advanced NLP**: Symptom severity assessment
- **Integration APIs**: EHR system integration

### Performance Optimizations
- **Streaming Processing**: Real-time audio streaming
- **Model Optimization**: Quantized Whisper models
- **Caching**: Transcription result caching
- **Load Balancing**: Multiple processing instances

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review application logs
3. Test with the health check endpoint
4. Verify environment configuration

---

**Note**: This voice integration is designed to work locally for development and can be easily deployed to Azure for production use. 