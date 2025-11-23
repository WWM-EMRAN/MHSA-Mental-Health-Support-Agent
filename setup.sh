#!/bin/bash
# MHSA Setup Script
# Quick setup for Mental Health Support Agent

set -e  # Exit on error

echo "============================================"
echo "MHSA - Mental Health Support Agent"
echo "Setup Script"
echo "============================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version found"

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip -q
echo "✓ pip upgraded"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your OpenAI API key"
    echo "   Open .env and set: OPENAI_API_KEY=your_key_here"
else
    echo "✓ .env file already exists"
fi

# Initialize database
echo ""
echo "Initializing database..."
python3 -c "from src.database import DatabaseConnection; db = DatabaseConnection(); db.connect(); db.create_tables(); db.close()"
echo "✓ Database initialized"

# Run tests
echo ""
echo "Running tests..."
python3 -m pytest tests/ -q
echo "✓ All tests passed"

# Setup complete
echo ""
echo "============================================"
echo "Setup Complete! ✓"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the demo: python demo.py"
echo "4. Run the application: python main.py"
echo ""
echo "⚠️  Remember: MHSA is not a replacement for professional help"
echo "If you're in crisis, call 988 or your local emergency services"
echo ""
