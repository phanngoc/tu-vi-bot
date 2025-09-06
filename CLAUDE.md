# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Backend (Python Flask)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask application
python app.py
```

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev     # Development server
npm run build   # Production build
npm start       # Start production server
npm run lint    # Run ESLint
```

## Architecture Overview

This is a Vietnamese astrology (Tử Vi) chatbot application with a Python Flask backend and Next.js React frontend.

### Backend Structure
- **app.py**: Main Flask application with API endpoints
  - `/api/reply`: Chat endpoint for AI responses
  - `/api/export-tu-vi`: Generate horoscope charts
- **chat.py**: Core AI logic using LlamaIndex and OpenAI
  - Handles Vietnamese lunar calendar calculations
  - Uses RAG (Retrieval Augmented Generation) with ChromaDB vector storage
  - Integrates with OpenAI GPT-4o-mini for responses
- **models.py**: SQLAlchemy database models
  - SQLite database (`tuvi.db`) for storing requests, users, zodiac data
  - Models: Request, User, Zodiac, Star, CanChi, MasterData
- **retrieve_chroma.py**: ChromaDB vector store operations
- **batch_index.py**, **save_chunk.py**, **seed.py**: Data processing utilities

### Frontend Structure (Next.js 14 + TypeScript)
- **App Router**: Uses Next.js 14 app directory structure
- **Components**: React components in `/src/components/`
- **Pages**: 
  - Chat interface at `/chat-bot`
  - Public layout wrapper
- **Styling**: TailwindCSS for styling
- **TypeScript**: Full TypeScript support with strict configuration

### Key Dependencies
- **Backend**: Flask, LlamaIndex, OpenAI, ChromaDB, SQLAlchemy, BeautifulSoup4
- **Frontend**: Next.js 14, React 18, TailwindCSS, TypeScript
- **AI/ML**: OpenAI GPT-4o-mini, text-embedding-3-small embeddings
- **Database**: SQLite with SQLAlchemy ORM

### Data Flow
1. User sends message via frontend chat interface
2. Frontend calls `/api/reply` endpoint
3. Backend extracts birth info using OpenAI function calling
4. Lunar calendar conversion and star positioning calculations
5. RAG query against Vietnamese astrology knowledge base in ChromaDB
6. Structured response generation using Pydantic models
7. Response returned as JSON to frontend

### Environment Setup
Create `.env` file in root directory:
```
OPENAI_API_KEY=your_openai_api_key
```

### Database
- Uses SQLite database (`tuvi.db`) created automatically
- Contains Vietnamese astrology reference data (stars, zodiac signs, etc.)
- Stores user requests and generated horoscope data

### Vector Storage
- ChromaDB persistent storage in `./chroma_db/` directory
- Contains Vietnamese astrology knowledge for RAG retrieval
- Uses OpenAI embeddings for semantic search