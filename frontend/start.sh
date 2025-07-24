#!/bin/bash

# Helper script to start React frontend with proper environment setup

echo "🚀 Starting Pathways Agent React Frontend..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found. Make sure you're in the frontend-react directory."
    exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules not found. Running npm install..."
    npm install
fi

# Unset problematic HOST variable
if [ ! -z "$HOST" ] && [ "$HOST" != "localhost" ]; then
    echo "⚠️  Unsetting HOST environment variable (was: $HOST)"
    unset HOST
fi

# Check if port 3000 is available
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 3000 is already in use"
    echo "💡 You may need to stop the existing process or use a different port"
    echo "   To kill the process: kill -9 \$(lsof -ti:3000)"
fi

echo "📦 Starting React development server..."
echo "🌐 Frontend will be available at: http://localhost:3000"
echo "🔗 Backend should be running at: http://localhost:8000"
echo "💡 Press Ctrl+C to stop the server"
echo "=================================================="

# Start the React app with proper environment
HOST=localhost PORT=3000 BROWSER=none npm start 