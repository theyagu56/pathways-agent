# Pathways Agent - Provider Matching Engine

This project enhances the existing Pathways Agent monorepo with a Provider Matching Engine that uses AI to recommend healthcare providers based on injury descriptions, location, and insurance.

## 🏗️ Architecture

- **FastAPI Backend** (`backend-fastapi/`): AI-powered provider matching service
- **React Frontend** (`frontend-react/`): Modern web interface with Tailwind CSS
- **Shared Data** (`shared-data/`): Provider database and configuration

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key

### 1. Backend Setup

```bash
cd pathways-ai/backend-fastapi

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# Run the FastAPI server
python main.py
```

The backend will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
cd pathways-ai/frontend-react

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in `backend-fastapi/`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Provider Data

The system uses `shared-data/providers.json` which contains 100+ test providers with:
- Name and specialty
- ZIP code location
- Insurance acceptance
- Ratings and availability

## 📋 API Endpoints

### POST /api/match-providers

Matches providers based on injury description, location, and insurance.

**Request Body:**
```json
{
  "injury_description": "I have a sprained ankle from playing basketball",
  "zip_code": "10001",
  "insurance": "Blue Cross"
}
```

**Response:**
```json
[
  {
    "name": "Dr. Sarah Johnson",
    "specialty": "Orthopedics",
    "distance": 2.5,
    "availability": "2024-01-15",
    "ranking_reason": "Specialty match, Insurance accepted"
  }
]
```

## 🧠 AI Features

The system uses GPT-4 to:
1. **Analyze injury descriptions** and recommend appropriate medical specialties
2. **Rank providers** based on:
   - Specialty match (50% weight)
   - Insurance compatibility (30% weight)
   - Geographic proximity (20% weight)

## 🎨 Frontend Features

- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Form Validation**: Required fields and proper input handling
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Responsive Cards**: Provider results displayed in attractive cards

## 🔒 CORS Configuration

The backend is configured to accept requests from `http://localhost:3000` for development.

## 📁 Project Structure

```
pathways-ai/
├── backend-fastapi/          # FastAPI provider matching service
│   ├── main.py              # Main application
│   └── requirements.txt     # Python dependencies
├── frontend-react/          # React frontend
│   ├── src/
│   │   ├── pages/
│   │   │   └── provider-matching.tsx
│   │   ├── App.tsx
│   │   └── index.tsx
│   └── package.json
└── shared-data/
    └── providers.json       # Provider database
```

## 🧪 Testing

### Backend Testing

```bash
cd pathways-ai/backend-fastapi
python -m pytest
```

### Frontend Testing

```bash
cd pathways-ai/frontend-react
npm test
```

## 🚀 Deployment

### Backend Deployment

The FastAPI app can be deployed using:
- Docker
- Heroku
- AWS Lambda
- Any Python hosting platform

### Frontend Deployment

The React app can be built and deployed:
```bash
cd pathways-ai/frontend-react
npm run build
```

## 🔄 Integration with Existing Project

This enhancement:
- ✅ Preserves existing Flutter modules
- ✅ Maintains existing folder structure
- ✅ Adds new functionality without breaking changes
- ✅ Uses clean separation between AI logic and business logic

## 📞 Support

For issues or questions:
1. Check the API documentation at `http://localhost:8000/docs`
2. Review the FastAPI logs for backend issues
3. Check browser console for frontend issues

## 🔮 Future Enhancements

- Real-time provider availability updates
- Integration with actual provider databases
- Advanced filtering and sorting options
- Appointment scheduling integration
- User authentication and profiles
- Provider reviews and ratings 