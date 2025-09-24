#!/bin/bash

echo "🎮 Setting up AI Fight Club..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env and add your API keys!"
else
    echo "✅ .env file already exists"
fi

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the game:"
echo "1. Edit .env and add your API keys"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python main.py"
echo ""
echo "Have fun! 🤖🥊"
