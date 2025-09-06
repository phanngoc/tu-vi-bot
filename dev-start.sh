#!/bin/bash

# Tu Vi Bot - Combined Development Startup Script
# This script starts both frontend and backend services concurrently

echo "🌟 Tu Vi Bot - Full Stack Development Startup"
echo "============================================="

# Function to cleanup background processes on script exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    jobs -p | xargs -r kill
    echo "✅ All services stopped"
    exit 0
}

# Trap Ctrl+C and cleanup
trap cleanup SIGINT SIGTERM

# Check if required commands exist
check_dependencies() {
    echo "🔍 Checking dependencies..."
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is not installed"
        exit 1
    fi
    
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js is not installed"
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        echo "❌ npm is not installed"
        exit 1
    fi
    
    echo "✅ All dependencies found"
}

# Setup environment
setup_environment() {
    echo "⚙️  Setting up environment..."
    
    # Check/create .env file
    if [ ! -f .env ]; then
        echo "⚠️  Creating .env file..."
        cat > .env << EOL
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Flask Configuration
FLASK_DEBUG=True
FLASK_ENV=development
EOL
        echo "📝 Please update .env file with your OpenAI API key"
    fi
    
    # Install Python dependencies
    if [ -f requirements.txt ]; then
        echo "📦 Installing Python dependencies..."
        pip install -r requirements.txt > /dev/null 2>&1
    fi
    
    # Install Node.js dependencies
    if [ -f frontend/package.json ]; then
        echo "📦 Installing Node.js dependencies..."
        cd frontend && npm install > /dev/null 2>&1 && cd ..
    fi
    
    echo "✅ Environment setup complete"
}

# Start backend service
start_backend() {
    echo "🚀 Starting Backend (Flask)..."
    python app.py &
    BACKEND_PID=$!
    echo "   Backend PID: $BACKEND_PID"
    echo "   Backend URL: http://127.0.0.1:5000"
}

# Start frontend service
start_frontend() {
    echo "🚀 Starting Frontend (Next.js)..."
    cd frontend && npm run dev &
    FRONTEND_PID=$!
    echo "   Frontend PID: $FRONTEND_PID"  
    echo "   Frontend URL: http://localhost:3000"
    cd ..
}

# Main execution
main() {
    check_dependencies
    setup_environment
    
    echo ""
    echo "🌟 Starting services..."
    echo "========================"
    
    start_backend
    sleep 3
    start_frontend
    
    echo ""
    echo "🎉 Both services are starting up!"
    echo "📱 Frontend: http://localhost:3000"
    echo "🔧 Backend:  http://127.0.0.1:5000"
    echo ""
    echo "Available API endpoints:"
    echo "  POST /api/reply      - Chat with AI"
    echo "  GET  /api/export-tu-vi - Generate horoscope"
    echo ""
    echo "Press Ctrl+C to stop all services"
    echo "=================================="
    
    # Wait for background processes
    wait
}

# Run main function
main