#!/bin/bash
# Startup script for Investment Research Orchestrator

set -e

echo "=========================================="
echo "Investment Research Orchestrator"
echo "=========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your OPENAI_API_KEY before running!"
    echo ""
    exit 1
fi

# Check if OPENAI_API_KEY is set
if ! grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
    echo "⚠️  Warning: OPENAI_API_KEY not set in .env file"
    echo "Please edit .env and add your OpenAI API key"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Run the service
echo "🚀 Starting Investment Research Orchestrator..."
echo "📍 Service will be available at: http://localhost:8000"
echo "📚 API Documentation at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the service"
echo ""

cd src
uvicorn orchestrator:app --host 0.0.0.0 --port 8000 --reload
