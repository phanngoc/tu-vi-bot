#!/bin/bash

# Tu Vi Bot - Backend Development Startup Script
echo "🚀 Starting Tu Vi Bot Backend..."


# Check if database exists, create if not
if [ ! -f tuvi.db ]; then
    echo "🗄️  Creating database..."
    python -c "from models import Base, engine; Base.metadata.create_all(engine); print('Database created successfully')"
fi

# Start Flask application
echo "🌟 Starting Flask development server..."
echo "Backend will be available at: http://127.0.0.1:5000"
echo "API endpoints:"
echo "  - POST /api/reply - Chat with AI"
echo "  - GET  /api/export-tu-vi - Generate horoscope"
echo ""
echo "Press Ctrl+C to stop the server"
echo "----------------------------------------"

python app.py