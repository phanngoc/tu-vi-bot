#!/bin/bash

# Tử Vi Bot Start Script

echo "🔮 Starting Tử Vi Bot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found! Please run setup.py first."
    exit 1
fi

# Check if OpenAI API key is set
if grep -q "your_openai_api_key_here" .env; then
    echo "⚠️  Please add your OpenAI API key to .env file first!"
    exit 1
fi

# Function to start backend
start_backend() {
    echo "🚀 Starting Backend..."
    python app.py &
    BACKEND_PID=$!
    echo "✅ Backend started with PID: $BACKEND_PID"
}

# Function to start frontend
start_frontend() {
    echo "🎨 Starting Frontend..."
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    echo "✅ Frontend started with PID: $FRONTEND_PID"
    cd ..
}

# Start both services
start_backend
sleep 2
start_frontend

echo ""
echo "🎉 Tử Vi Bot is running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user to stop
trap 'echo "🛑 Stopping services..."; kill $BACKEND_PID $FRONTEND_PID; exit' INT
wait
