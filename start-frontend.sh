#!/bin/bash

# Tu Vi Bot - Frontend Development Startup Script
echo "🚀 Starting Tu Vi Bot Frontend..."

# Change to frontend directory
cd frontend

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Check if package.json exists
if [ ! -f package.json ]; then
    echo "❌ package.json not found in frontend directory."
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d node_modules ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
else
    echo "📦 Dependencies already installed, skipping npm install"
fi

# Start Next.js development server
echo "🌟 Starting Next.js development server..."
echo "Frontend will be available at: http://localhost:3000"
echo "Features:"
echo "  - Hot reload enabled"
echo "  - TypeScript support"
echo "  - TailwindCSS styling"
echo "  - Chat bot interface at /chat-bot"
echo ""
echo "Press Ctrl+C to stop the server"
echo "----------------------------------------"

npm run dev